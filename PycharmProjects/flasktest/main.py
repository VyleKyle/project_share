from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():

    # Mission: Display spotify embed of current song
    #     -> Init spotify on script start
    #     -> Grab current song
    #     -> song.external_urls.spotify = "http://open.spotify..."
    #     -> http get open.spotify.com/oembed?url= {url}
    #     -> parse into custom html iframe
    #     -> insert iframe into render template? learn flask

    return render_template("main.html")

if __name__ == '__main__':
    app.run()
