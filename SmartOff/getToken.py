import requests
import json

def sendReq():
	headers = {
	    'Accept': 'application/json',
	}

	data = [
	  ('grant_type', 'client_credentials'),
	  ('scope', 'paymentapi'),
	]

	response = requests.post('https://hack.softheon.io/oauth2/connect/token', headers=headers, data=data, auth=('107b54ff-7cc6-412b-9e64-2e454c082d2c', 'a3aff187-12ae-44a0-927d-54abff5a545f'))
	result =  json.loads(response.text)
	print(result["token_type"])
	token_type = result["token_type"]
	access_token = result["access_token"]
	auth = token_type+ "  "+ access_token

	print(auth)


	headers = {
	    'Content-Type': 'application/json',
	    'Authorization': auth,
	}

	data = '{    "cardNumber": "4111113956134018",   "securityCode": "123",   "expirationMonth": 11,    "expirationYear": 2019,    "cardHolderName": "John Doe",    "billingAddress": {        "address1": "1500 Stony Brook Road",        "city": "Stony Brook",       "state": "NY",        "zipCode": "11790"    },   "email": "jdoe@example.com",    "referenceId": "credit_card_example",}'

	response = requests.post('https://hack.softheon.io/api/payments/v1/creditcards', headers=headers, data=data)

	


	result =  json.loads(response.text)
	print(result)

	token_auth = result["token"]
	#import requests

	headers = {
	    'Content-Type': 'application/json',
	    'Authorization': auth,
	}

	data = '{  "paymentAmount": 100.32,   "description": "Payment of balance due",   "referenceId": "example_payment",    "paymentMethod": {        "paymentToken":  '+token_auth+',      "type": "Credit Card"    }}'

	response = requests.post('https://hack.softheon.io/api/payments/v1/payments', headers=headers, data=data)

	result =  json.loads(response.text)

	print(result["result"]["status"])

sendReq()
