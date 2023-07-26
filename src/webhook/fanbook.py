from flask import Flask, request, jsonify
import hashlib
import hmac

app = Flask(__name__)


@app.route('/webhook/fanbook/v1/payments', methods=['POST'])
def handle_payment():
    # 1. Validate the signature
    signature = request.headers.get('X-Signature')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 403

    # 2. Extract information from the payload
    payload = request.json
    email = payload.get('email')
    plan = payload.get('plan')

    # 3. Check what plan the user has paid for
    # This part will depend on your application's business logic
    if plan not in ['plan1', 'plan2', 'plan3']:
        return jsonify({'error': 'Invalid plan'}), 400

    # 4. Update the database
    users[email] = plan  # Replace this with actual DB interaction

    return jsonify({'status': 'success'}), 200


def verify_signature(payload, signature):
    return True


if __name__ == '__main__':
    app.run(debug=True)
