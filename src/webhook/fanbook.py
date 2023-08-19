from flask import Flask, request, jsonify
import hashlib
import hmac

from src.database.mysql_utils import find_plan_credit_for_user, get_user_or_create
from src.payments.constant import PLAN_CONFIG
from src.utils.logging_util import logging
from src.utils.param_singleton import Params
from src.database.mysql import Transaction, ServiceType, PlanCredit, ChannelType, User, Subscription

app = Flask(__name__)


@app.route('/webhook/fanbook/v1/payments', methods=['POST', 'GET'])
def handle_payment():
    # 1. Validate the signature

    # 2. deduplicate the request
    data = request.json
    external_txn_id = data['orderNo']
    if external_txn_id_exists(external_txn_id):
        logging.info(f'handle_payment(): external_txn_id: {external_txn_id} already exists, skipped')
        return '', 200

    # 3. Save the transaction to the database
    product_identifier = data['product']['identifier']
    user_id = data['userId']
    user = get_user_or_create(user_id)
    plan_config = PLAN_CONFIG[product_identifier]
    for service_type, credit_count in plan_config.items():
        plan_credit = find_plan_credit_for_user(user, service_type)
        if plan_credit is None:
            plan_credit = PlanCredit(
                user_id=user.id,
                service_type=service_type.value,
                credit_count=credit_count,
                chat_type=ChannelType.UNIVERSAL.value,
            )
        else:
            plan_credit.credit_count += credit_count

        transaction = Transaction(
            plan_credit_id=plan_credit.id,
            external_txn_id=external_txn_id,
        )
        with Params().Session() as session:
            session.add(plan_credit)
            session.add(transaction)
            session.commit()

    logging.info(f'handle_payment(): {request.json}')
    return '', 200


def external_txn_id_exists(external_txn_id) -> bool:
    # Assuming the `external_txn_id` is a column in the `OwnerParameter` table
    with Params().Session() as session:
        query_result = session.query(Transaction).filter(external_txn_id == external_txn_id).first()
        return query_result is not None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
