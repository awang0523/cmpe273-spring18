from flask import Flask
from flask import request
from flask import jsonify
import datetime
import sqlite3

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

open('wallet.db', 'w').close()
conn = sqlite3.connect('wallet.db')

conn.execute('''CREATE TABLE WALLET
         (id INT PRIMARY KEY     NOT NULL,
         balance        INT    NOT NULL,
         coin_symbol    TEXT     NOT NULL)''')

conn.execute('''CREATE TABLE TXN
         (status   TEXT   NOT NULL,
         from_wallet INT     NOT NULL,
         to_wallet    INT    NOT NULL,
         amount      INT     NOT NULL,
         time_stamp   TEXT   NOT NULL,
         txn_hash   TEXT   NOT NULL)''')

@app.route('/wallets', methods=['POST'])
def new_wallet():
    id = request.form["id"]
    balance = request.form["balance"]
    coin_symbol = request.form["coin_symbol"]

    conn.execute("INSERT INTO WALLET (id, balance, coin_symbol) VALUES (?,?,?)" , (id,balance,coin_symbol) )
    conn.commit()
    result = jsonify({'id': id, 'balance': balance, 'coin_symbol': coin_symbol})
    return result, 201

@app.route('/wallets/<int:id>', methods=['GET', 'DELETE'])
def user(id):
    if request.method == 'GET':
        cursor = conn.execute("SELECT balance, coin_symbol from WALLET WHERE id = ?", (id,))
        for row in cursor:
            balance = row[0]
            coin_symbol = row[1]

        result = jsonify({'id': id, 'balance': balance, 'coin_symbol': coin_symbol})
        return result
    elif request.method == 'DELETE':
        conn.execute("DELETE from WALLET WHERE id = ?;", (id,))
        return '', 204

@app.route('/txns', methods=['POST'])
def new_txn():
    from_wallet = request.form["from_wallet"]
    to_wallet = request.form["to_wallet"]
    amount = request.form["amount"]
    txn_hash = request.form["txn_hash"]

    status = 'pending'
    time_stamp = str(datetime.datetime.now())

    conn.execute("INSERT INTO TXN (status, from_wallet, to_wallet, amount, time_stamp, txn_hash) VALUES (?,?,?,?,?,?)" , (status, from_wallet, to_wallet, amount, time_stamp, txn_hash))
    conn.commit()
    result = jsonify({'from_wallet':from_wallet, 'to_wallet':to_wallet, 'amount':amount, 'time_stamp':time_stamp, 'txn_hash':txn_hash})
    return result, 201

@app.route('/txns/<int:txn_hash>', methods=['GET'])
def txn(txn_hash):
    cursor = conn.execute("SELECT status, from_wallet, to_wallet, amount, time_stamp from TXN WHERE txn_hash = ?", (txn_hash,))
    for row in cursor:
        status = row[0]
        from_wallet = row[1]
        to_wallet = row[2]
        amount = row[3]
        time_stamp = row[4]

    result = jsonify({'status':status, 'from_wallet':from_wallet, 'to_wallet':to_wallet, 'amount':amount, 'time_stamp':time_stamp, 'txn_hash':txn_hash})
    return result

    