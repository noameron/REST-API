from flask import Flask, jsonify, request

from db import put_customer_id, get_customer_id

app = Flask(__name__)


@app.route('/customer_id', methods=['PUT'])
def add_customer_id():
    customer_id = request.json.get('customer_id')
    if not customer_id:
        return jsonify({'error': 'customer_id is required'}), 400
    if get_customer_id(customer_id):
        return jsonify({'error': 'customer_id already exists'}), 400
    put_customer_id(customer_id)
    return jsonify({'customer_id': customer_id}), 201


@app.route('/customer_id/<customer_id>', methods=['GET'])
def check_customer_id(customer_id):
    if not customer_id:
        return jsonify({'error': 'customer_id is required'}), 400
    if get_customer_id(customer_id):
        return jsonify({'customer_id': customer_id}), 200
    return jsonify({'error': 'customer_id does not exist'}), 404
