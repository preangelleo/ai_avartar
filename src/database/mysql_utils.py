from typing import Optional

from src.database.mysql import User, PlanCredit, ServiceType, ChannelType
from src.utils.param_singleton import Params
from datetime import datetime


from sqlalchemy.orm import joinedload


def get_user_or_create(user_from_id: str) -> Optional[User]:
    with Params().Session() as session:
        user = session.query(User).filter_by(user_from_id=user_from_id).first()
        if not user:
            user = User(user_from_id=user_from_id)
            session.add(user)
            session.commit()
        return user


def find_plan_credit_for_user(user: User, service_type: ServiceType) -> Optional[PlanCredit]:
    with Params().Session() as session:
        plan_credit = session.query(PlanCredit).filter_by(user_id=user.id, service_type=service_type.value).first()
        return plan_credit


def init_table_if_needed(user_from_id: str):
    with Params().Session() as session:
        user = session.query(User).filter_by(user_from_id=user_from_id).first()
        if user is None:
            # If user does not exist, create a new user
            user = User(user_from_id=user_from_id)
            session.add(user)
            # After adding a new User, you need to commit to get the id of the new User
            session.commit()

            # create a plan credit for the user with conversation type and credit as 500
            plan_credit = PlanCredit(
                user_id=user.id,
                service_type=ServiceType.CONVERSATION.value,
                credit_count=500,  # TODO: figure out a initial credit count
                chat_type=ChannelType.PUBLIC.value,
            )
            session.add(plan_credit)
            session.commit()
        else:
            print(f"User {user_from_id} already exists.")


def check_user_eligible_for_conversation(user_from_id: str, is_private: bool, usage: bool) -> bool:
    # we are going to always check subscript first
    # if user has active subscription, then we don't need to check credits
    # if user has credit and usage if true, then we need to reduce the credit by 1

    chat_type = ChannelType.UNIVERSAL if is_private else ChannelType.PUBLIC

    with Params().Session() as session:
        user = (
            session.query(User)
            .options(joinedload(User.subscriptions), joinedload(User.plan_credits))
            .filter_by(user_from_id=user_from_id)
            .first()
        )
        if user is None:
            return False

        # Check active subscriptions
        for sub in user.subscriptions:
            if sub.service_type == ServiceType.CONVERSATION and sub.start_date <= datetime.now() <= sub.end_date:
                return True

        # Check available credits
        for credit in user.plan_credits:
            if (
                credit.service_type == ServiceType.CONVERSATION
                and credit.credit_count > 0
                and credit.chat_type == chat_type
            ):
                if usage:
                    # the credit can only go as low as 0
                    credit.credit_count -= 1
                    session.add(credit)
                    session.commit()
                return True

        return False


def find_user_with_eligible_plan(user_from_id: str) -> Optional[User]:
    with Params().Session() as session:
        user = (
            session.query(User)
            .options(joinedload(User.subscriptions), joinedload(User.plan_credits))
            .filter_by(user_from_id=user_from_id)
            .first()
        )
        return user
