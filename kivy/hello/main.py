#!/usr/bin/python
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from credentials import client_id, dev_key
import plaid
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest as TokenRequest
from plaid.api import plaid_api
import requests
import webbrowser
import json

#   API responses are JSON objects, requiring parsing, ex:
#   json_string = json.dumps(response.to_dict(), default=str)

plaid_config = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': client_id,
        'secret': dev_key,
        }
    )

api_client = plaid.ApiClient(plaid_config)
client = plaid_api.PlaidApi(api_client)

exchange_request = TokenRequest(
    public_token=pt_response['public_token']
    )
exchange_response = client.item_public_token_exchange(exchange_request)
access_token = exchange_response['access_token']

class PlaidApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        auth_button = Button(text='Authenticate with Plaid')
        auth_button.bind(on_press=self.authenticate_with_plaid)
        self.transaction_label = Label(text='Transaction details will appear here')
        
        self.layout.add_widget(auth_button)
        self.layout.add_widget(self.transaction_label)
        return self.layout

    def authenticate_with_plaid(self, instance):
        
        response = client.LinkToken.create({
            'user': {
                'client_user_id': 'unique-user-id',
            },
            'client_name': 'Test',
            'products': ['transactions'],
            'country_codes': ['US'],
            'language': 'en',
            }
        )
        
        link_token = response['link_token']
        
        plaid_link_url = f"https://development.plaid.com/link/token?token={link_token}"
        webbrowser.open(plaid_link_url)
        self.label.text = 'Follow the browser'
        
        # This URL should be the link to initiate Plaid Link process
        # For simplicity, assume it's already configured to redirect appropriately
        #plaid_link_url = 'https://your-plaid-link-url.com'
        #webbrowser.open(plaid_link_url)
        # You would normally handle the redirect URI to capture the public token and exchange it for an access token
        # For example purposes, we'll assume you have the access token stored or you handle this part outside of Kivy
        #self.fetch_transactions('access_token')

    def fetch_transactions(self, access_token):
        # Fetch the most recent transaction
        headers = {'Authorization': f'Bearer {access_token}'}
        transactions_url = 'https://development.plaid.com/transactions/get'
        response = requests.post(transactions_url, json={
            'client_id': client_id,
            'secret': dev_key,
            'access_token': access_token,
            'start_date': '2020-01-01',
            'end_date': '2020-02-01'
        }, headers=headers)
        
        if response.status_code == 200:
            transactions = response.json()['transactions']
            # Display the most recent transaction
            if transactions:
                self.transaction_label.text = f"Most Recent Transaction: {transactions[0]['name']} for ${transactions[0]['amount']}"
            else:
                self.transaction_label.text = "No recent transactions found."
        else:
            self.transaction_label.text = "Failed to fetch transactions."

if __name__ == '__main__':
    PlaidApp().run()

