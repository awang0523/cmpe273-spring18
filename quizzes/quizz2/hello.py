from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)
names = {}
uid = 1

@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"

@app.route('/users', methods=['POST'])
def new_users():
    global uid
    name = request.form["name"]
    names[uid] = name
    result = jsonify({'id': uid, 'name': name})
    uid = uid + 1
    return result, 201

@app.route('/users/<int:uid>', methods=['GET', 'DELETE'])
def user(uid):
    if request.method == 'GET':
        result = jsonify({'id': uid, 'name': names[uid]})
        return result
    elif request.method == 'DELETE':
        names.pop(uid, None)
        return '', 204