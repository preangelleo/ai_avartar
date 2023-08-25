import logging
from typing import Optional
from sqlalchemy import and_

from src.payments.constant import PUBLIC_INIT_CHAT_CREDIT, PUBLIC_INIT_DRAWING_CREDIT, ServiceType
from src.database.mysql import User, PlanCredit, ChannelType, Subscription
from src.utils.param_singleton import Params
from datetime import datetime
from sqlalchemy.orm import Session


from sqlalchemy.orm import joinedload


def get_user_or_create(user_from_id: str) -> Optional[User]:
    with Params().Session() as session:
        user = session.query(User).filter_by(user_from_id=user_from_id).first()
        if not user:
            user = User(user_from_id=user_from_id)
            session.add(user)
            session.commit()
        return user


def find_plan_credit_for_user(user: User, chat_type: ChannelType, session: Session) -> Optional[PlanCredit]:
    plan_credit = session.query(PlanCredit).filter_by(user_id=user.user_from_id, chat_type=chat_type.value).first()
    return plan_credit


def find_active_subscription_for_user(user: User, time_to_check: datetime, session: Session) -> Optional[Subscription]:
    active_subscription = (
        session.query(Subscription)
        .filter(
            and_(
                Subscription.user_id == user.user_from_id,
                Subscription.start_date <= time_to_check,
                (Subscription.end_date >= time_to_check),
            )
        )
        .first()
    )

    return active_subscription


def init_credit_table_if_needed(user_from_id: str):
    user: User = get_user_or_create(user_from_id)

    with Params().Session() as session:
        plan_credit = find_plan_credit_for_user(user=user, chat_type=ChannelType.PUBLIC, session=session)
        if plan_credit is None:
            # create a plan credit for the user with conversation type and credit as 500
            plan_credit = PlanCredit(
                user_id=user.user_from_id,
                conversation_credit_count=PUBLIC_INIT_CHAT_CREDIT,
                drawing_credit_count=PUBLIC_INIT_DRAWING_CREDIT,
                chat_type=ChannelType.PUBLIC.value,
            )
            session.add(plan_credit)
            session.commit()
        else:
            print(f"User {user_from_id} already exists.")


def check_plan_credit_enough_for_service(
    plan_credit: PlanCredit, service_type: ServiceType, reduce_plan_credit: bool, session: Session
) -> bool:
    if service_type == ServiceType.conversation:
        if plan_credit.conversation_credit_count > 0:
            if reduce_plan_credit:
                plan_credit.conversation_credit_count -= 1
                session.add(plan_credit)
                session.commit()
            return True
        else:
            return False
    else:
        if plan_credit.drawing_credit_count > 0:
            if reduce_plan_credit:
                plan_credit.drawing_credit_count -= 1
                session.add(plan_credit)
                session.commit()
            return True
        else:
            return False


def check_user_eligible_for_service(
    user_from_id: str, is_private: bool, service_type: ServiceType, reduce_plan_credit: bool
) -> bool:
    user: User = get_user_or_create(user_from_id)
    with Params().Session() as session:
        # we are going to always check subscript first
        active_subscription = find_active_subscription_for_user(
            user=user, time_to_check=datetime.now(), session=session
        )

        if active_subscription is not None:
            logging.info(f"active subscription found for user {user_from_id}, ")
            return True

        # if no active subscription, then we check the plan credit for universal usage
        universal_plan_credit = find_plan_credit_for_user(user=user, chat_type=ChannelType.UNIVERSAL, session=session)
        if universal_plan_credit is not None:
            if check_plan_credit_enough_for_service(
                plan_credit=universal_plan_credit,
                service_type=service_type,
                reduce_plan_credit=reduce_plan_credit,
                session=session,
            ):
                logging.info(f"universal credit is enough for user {user_from_id}, " f"service type {service_type}")
                return True
            else:
                if is_private:
                    logging.info(f"user does not have enough credit for private chat")
                    return False
                else:
                    public_plan_credit = find_plan_credit_for_user(
                        user=user, chat_type=ChannelType.PUBLIC, session=session
                    )
                    if public_plan_credit is not None:
                        if check_plan_credit_enough_for_service(
                            plan_credit=public_plan_credit,
                            service_type=service_type,
                            reduce_plan_credit=reduce_plan_credit,
                            session=session,
                        ):
                            logging.info(
                                f"public credit is enough for user {user_from_id}, " f"service type {service_type}"
                            )
                            return True
                        else:
                            logging.info(
                                f"public credit is not enough for user {user_from_id}," f"service type {service_type}"
                            )
                            return False
                    else:
                        logging.info(
                            f"cannot find public plan credit for user {user_from_id}," f"service type {service_type}"
                        )
                        return False
