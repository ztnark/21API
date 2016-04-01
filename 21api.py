import os
import json
import random
import requests

from random import randint

from flask import Flask
from flask import request
from flask import send_from_directory
from flask import jsonify
from two1.lib.wallet import Wallet

app = Flask(__name__)



from two1.commands import status
from two1.commands import log
from two1.lib.server import rest_client
from two1.commands.config import Config
from two1.commands.config import TWO1_HOST

conf = Config()
host = TWO1_HOST
wallet = Wallet()
code = "<add-authorization-code-here>"
        
@app.route('/dashboard', methods=['GET'])
def dashboard():  
        if request.args.get("code") != code:
            return custom_401()
        client = rest_client.TwentyOneRestClient(host, conf.machine_auth, conf.username)
        status_mining = status.status_mining(conf, client)
        status_wallet = status.status_wallet(conf, client)  
        status_account = status.status_account(conf)  
        status_earnings = client.get_earnings()
        dashInfo = {"status_mining":status_mining, "status_wallet": status_wallet['wallet'], "status_account": status_account, "status_earnings": status_earnings}      
        return json.dumps(dashInfo, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        
@app.route('/mine', methods=['GET'])
def mine():
        if request.args.get("code") != code:
            return custom_401()
        os.system('21 mine')  
        client = rest_client.TwentyOneRestClient(host, conf.machine_auth, conf.username)
        status_mining = status.status_mining(conf, client)  
        status_wallet = status.status_wallet(conf, client)
        status_account = status.status_account(conf)
        status_earnings = client.get_earnings() 
        dashInfo = {"status_mining":status_mining, "status_wallet": status_wallet['wallet'], "status_account": status_account, "status_earnings": status_earnings}          
        return json.dumps(dashInfo, default=lambda o: o.__dict__, sort_keys=True, indent=4) 

@app.route('/flush', methods=['GET'])
def flush():
        if request.args.get("code") != code:
            return custom_401()
        os.system('21 flush')  
        client = rest_client.TwentyOneRestClient(host, conf.machine_auth, conf.username)
        status_mining = status.status_mining(conf, client)
        status_wallet = status.status_wallet(conf, client)
        status_account = status.status_account(conf)
        status_earnings = client.get_earnings()
        dashInfo = {"status_mining":status_mining, "status_wallet": status_wallet['wallet'], "status_account": status_account, "status_earnings": status_earnings}
        return json.dumps(dashInfo, default=lambda o: o.__dict__, sort_keys=True, indent=4)

@app.route('/send', methods=['POST'])
def send():
    if request.json["code"] != code:
            return custom_401()
    address = request.json["address"]
    print(address)
    amount = request.json["amount"]
    print(amount)
    if wallet.confirmed_balance() > 1:
         txid = wallet.send_to(address, amount)
    print(wallet.confirmed_balance())
    return "Success!"

@app.errorhandler(401)
def custom_401():
    return jsonify(error=401, text=str("Unauthorized")), 401

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3456)