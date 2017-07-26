import os
import json
import random
import requests

from random import randint

from flask import Flask
from flask import request
from flask import send_from_directory
from flask import jsonify

app = Flask(__name__)

code = "1"

dashInfo ={"status_wallet": {"onchain": 100000, "twentyone_balance": 25000, "flushing": 10000},"status_account":{"address": "13cnTxA9KC43iWF5umzuNtCPfiF8Lk54Kz"},"status_mining":{"hashrate": "75GH/S"}}       

@app.route('/dashboard', methods=['GET'])
def dashboard():  
        if request.args.get("code") != code:
            return custom_401()
        return json.dumps(dashInfo, default=lambda o: o.__dict__, sort_keys=True, indent=4)

@app.route('/mine', methods=['GET'])
def mine():
        if request.args.get("code") != code:
            return custom_401()
        os.system('21 mine')  
        dashInfo["status_wallet"]["twentyone_balance"] += 25000
        return json.dumps(dashInfo, default=lambda o: o.__dict__, sort_keys=True, indent=4) 

@app.route('/flush', methods=['GET'])
def flush():
       	if request.args.get("code") != code:
            return custom_401()
        dashInfo["status_wallet"]["flushing"] += dashInfo["status_wallet"]["twentyone_balance"]
        dashInfo["status_wallet"]["twentyone_balance"] = 0
        return json.dumps(dashInfo, default=lambda o: o.__dict__, sort_keys=True, indent=4)

@app.route('/send', methods=['POST'])
def send():
    print("hello")
    if request.json["code"] != code:
            return custom_401()
    print(request.json)
    address = request.json["address"]
    print(address)
    amount = request.json["amount"]
    print(amount)
    if dashInfo["status_wallet"]["onchain"] > amount:
         dashInfo["status_wallet"]["onchain"] -= amount
    return "Success!"

@app.errorhandler(401)
def custom_401():
    return jsonify(error=401, text=str("Unauthorized")), 401

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3456)
