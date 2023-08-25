import datetime

from flask import Flask, request, jsonify
import hashlib
import hmac

from src.database.mysql_utils import (
    find_plan_credit_for_user,
    get_user_or_create,
    find_subscription_for_user,
    find_active_subscription_for_user,
)
from src.payments.constant import PLAN_CONFIG, CREDIT_BASED_PLAN, SUBSCRIPTION_BASED_PLAN
from src.utils.logging_util import logging
from src.utils.param_singleton import Params
from src.database.mysql import Transaction, PlanCredit, ChannelType, User, Subscription

app = Flask(__name__)


@app.route('/webhook/fanbook/v1/payments', methods=['POST', 'GET'])
def handle_payment():
    # 1. Validate the signature

    # 2. deduplicate the request
    data = request.json
    external_txn_id = data['orderNo']
    product_identifier = data['product']['identifier']
    user_id = data['userId']
    if external_txn_id_exists(external_txn_id):
        logging.info(f'handle_payment(): external_txn_id: {external_txn_id} already exists, skipped')
        return '', 200

    # 3. Save the transaction to the database
    user = get_user_or_create(user_id)
    with Params().Session() as session:
        try:
            if product_identifier in CREDIT_BASED_PLAN:
                handle_credit_based_plan(user, product_identifier, external_txn_id, session)
            else:
                handle_subscription_based_plan(user, product_identifier, external_txn_id, session)
        except Exception as e:
            session.rollback()
            logging.error(f'handle_payment(): {e}, rollback session')
        session.commit()
    logging.info(f'handle_payment(): {request.json}')
    return '', 200


def external_txn_id_exists(external_txn_id) -> bool:
    # Assuming the `external_txn_id` is a column in the `OwnerParameter` table
    with Params().Session() as session:
        query_result = session.query(Transaction).filter(Transaction.external_txn_id == external_txn_id).first()
        return query_result is not None


def handle_credit_based_plan(user, product_identifier, external_txn_id, session):
    logging.info(
        f'handle_credit_based_plan(): user: {user},'
        f' product_identifier: {product_identifier},'
        f' external_txn_id: {external_txn_id}'
    )
    plan_config = PLAN_CONFIG[product_identifier]
    conversation_credit = plan_config['conversation_credit']
    drawing_credit = plan_config['drawing_credit']
    plan_credit = find_plan_credit_for_user(user=user, chat_type=ChannelType.UNIVERSAL, session=session)
    if plan_credit is None:
        logging.info(f'handle_credit_based_plan(): plan_credit is None, creating a new one')
        plan_credit = PlanCredit(
            user_id=user.user_from_id,
            conversation_credit_count=conversation_credit,
            drawing_credit_count=drawing_credit,
            chat_type=ChannelType.UNIVERSAL.value,
        )
        session.add(plan_credit)
        session.flush()
        logging.info(f'handle_credit_based_plan(): plan_credit.id: {plan_credit.id}')
    else:
        logging.info(
            f'handle_credit_based_plan(): ' f'plan_credit is not None, updating the existing one, id: {plan_credit.id}'
        )
        plan_credit.conversation_credit_count += conversation_credit
        plan_credit.drawing_credit_count += drawing_credit

    transaction = Transaction(
        plan_credit_id=plan_credit.id,
        external_txn_id=external_txn_id,
        user_id=user.user_from_id,
    )
    session.add(transaction)
    session.flush()


def handle_subscription_based_plan(user, product_identifier, external_txn_id, session):
    logging.info(
        f'handle_subscription_based_plan(): user: {user},'
        f' product_identifier: {product_identifier},'
        f' external_txn_id: {external_txn_id}'
    )
    plan_config = PLAN_CONFIG[product_identifier]
    duration_days = plan_config['plan_duration_days']
    active_subscription = find_active_subscription_for_user(user=user, session=session)
    if active_subscription is None:
        logging.info(f'handle_subscription_based_plan(): active_subscription is None, creating a new one')
        datetime_time_now = datetime.datetime.now()
        active_subscription = Subscription(
            user_id=user.user_from_id,
            start_date=datetime.datetime.now(),
            end_date=datetime_time_now + datetime.timedelta(days=duration_days),
        )
        session.add(active_subscription)
        session.flush()
        logging.info(f'handle_subscription_based_plan(): subscription.id: {active_subscription.id}')
    else:
        logging.info(
            f'handle_subscription_based_plan(): '
            'active_subscription is not None, updating the existing one, id: '
            f'{active_subscription.id}'
        )

        active_subscription.end_date += datetime.timedelta(days=duration_days)

    transaction = Transaction(
        subscription_id=active_subscription.id,
        external_txn_id=external_txn_id,
        user_id=user.user_from_id,
    )
    session.add(transaction)
    session.flush()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
