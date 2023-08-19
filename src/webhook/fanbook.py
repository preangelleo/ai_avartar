from flask import Flask, request, jsonify
import hashlib
import hmac
from src.utils.logging_util import logging

app = Flask(__name__)


@app.route('/webhook/fanbook/v1/payments', methods=['POST', 'GET'])
def handle_payment():
    # 1. Validate the signature

    # 2. deduplicate the request

    logging.info(f'handle_payment(): {request.json}')
    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
