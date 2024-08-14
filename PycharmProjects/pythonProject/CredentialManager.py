from urllib.parse import urlencode, urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
import credentials
import requests
import time
import logging
import logging.handlers
import webbrowser

logfile = 'LOG'

logger = logging.getLogger("SpotifAI")
logConsole = logging.StreamHandler()
logFile = logging.FileHandler(logfile)
systemdHandler = logging.handlers.SysLogHandler(address="/dev/log")
formatter = logging.Formatter('| %(asctime)s |0| %(levelname)s |0| %(module)s |0| %(lineno)d |0| %(message)s |')
logger.setLevel(logging.DEBUG)
logFile.setFormatter(formatter)
logConsole.setFormatter(formatter)
systemdHandler.setFormatter(formatter)

if __name__ == "__main__":
    logger.addHandler(logConsole)
    logger.addHandler(logFile)
    logger.addHandler(systemdHandler)

authCode = ""
authRetrieved = False

# Prepare the authorization request handler
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse the URL and query string
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        global authCode
        global authRetrieved

        # extract the value of the code
        authCode = query_params.get("code")
        authRetrieved = True

        logger.debug("?")

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body>')
        self.wfile.write(b'Token has been created. You may close this tab.')
        self.wfile.write(b'</body></html>')

httpd = HTTPServer(("localhost", 10189), RequestHandler)

def get_authorization(scopes):

    global authCode
    global authRetrieved

    # Set up the OAuth2 credentials
    client_id = credentials.client_id
    client_secret = credentials.client_secret
    redirect_uri = credentials.redirect_uri

    # Build the authorization request
    auth_url = 'https://accounts.spotify.com/authorize'
    auth_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scopes
    }
    auth_request_url = auth_url + '?' + urlencode(auth_params)

    # Wait for the user to authorize
    webbrowser.open(auth_request_url)
    while not authRetrieved:
        httpd.handle_request()
    authRetrieved = False

    # Exchange the authorization code for an access token
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': authCode,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = token_response.json()

    token_response_data['expiration_date'] = str(token_response_data['expires_in'] + time.time())

    # Return the access and refresh tokens
    return token_response_data

def token_to_file(token_obj, token_file):
    with open(token_file, 'w') as file:
        logger.debug(token_obj)
        logger.debug(f"{token_obj['access_token']}\n{token_obj['refresh_token']}\n{token_obj['expiration_date']}\n{token_obj['scope']}")
        file.write(f"{token_obj['access_token']}\n{token_obj['refresh_token']}\n{token_obj['expiration_date']}\n{token_obj['scope']}")


    # Save the access and refresh tokens, along with the expiration time, to a file
    # logger.debug(token_obj)
    # logger.debug(token_obj['access_token'])
    # TOKEN = token_obj['access_token']
    # REFRESH = token_obj['refresh_token']
    # EXPIRATION = str(token_obj['expiration_date']) # listen i gotta leave for work but  the solution is data mishandling
    # logger.debug(TOKEN) # its been appending the fucking strings instead of appending the list
    # datatowrite = [TOKEN]
    # logger.debug(datatowrite)   # fuck i feel insane for these but i remember now
    # # datatowrite = [token_obj['access_token'], token_obj['refresh_token'], str(token_obj['expiration_date']), str(time.time())]
    # # datatowrite = [TOKEN, REFRESH, EXPIRATION, str(time.time())]
    # # datatowrite += token_obj['refresh_token']
    # # datatowrite += str(token_obj['expiration_date'])
    # # datatowrite += str(time.time())
    # with open(token_file, 'w') as f:
    #     logger.debug(datatowrite)
    #     f.writelines(datatowrite)
    #     logger.debug(datatowrite)

def token_from_file(token_file, refresh_period):
    # Load the access and refresh tokens, along with the expiration time, from the file
    with open(token_file, 'r') as f:
        access_token = f.readline()[:-1]
        refresh_token = f.readline()[:-1]
        expiration_date = f.readline()[:-1]
        scope = f.readline()


    output = {
        'access_token': access_token,
        'refresh_token': refresh_token, # Spotify will not always grant a refresh token. In this case, the variable will equal ''
        'expiration_date': expiration_date,
        'scope': scope
    }
    # Check if the access token is still valid and replaceable
    if expiration_date != '':
        if float(expiration_date) > time.time():
            if float(expiration_date) - time.time() < refresh_period:

                logger.debug("Refreshing token")

                # If the access token must be refreshed
                new_access_token = refresh_access_token(refresh_token, scope)

                new_access_token['refresh_token'] = refresh_token
                new_access_token['expiration_date'] = float(new_access_token['expires_in'] + time.time())

                token_to_file(new_access_token, token_file)

                output = new_access_token
        else:
            logger.fatal("Token on file expired!")
            logger.debug(f"Current time: {time.time()}, Exp. date: {expiration_date}, Est. remaining: {float(expiration_date) - time.time()}")
            new_token = get_authorization(scope)
            token_to_file(new_token, token_file)
            output = new_token
    else:
        logger.debug(output)

    # Return the token
    return output

def refresh_access_token(refresh_token, scope):
    # Exchange the refresh token for a new access token
    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret
    }
    token_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_response = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = token_response.json()

    return token_response_data

if __name__ == "__main__":
    debugtoke = get_authorization('user-read-playback-state')
    logger.debug(debugtoke)
    token_to_file(debugtoke, 't')
    logger.debug(token_from_file('t', 3600))