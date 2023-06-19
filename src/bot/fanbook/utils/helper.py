from sqlalchemy import func
from src.bot.fanbook.utils.constants import LIMIT_USER_LIST_COUNT
from database.mysql import ChatHistory
from src.utils.param_singleton import Params


def user_over_limit() -> bool:
    with Params().Session() as session:
        count = session.query(func.count(ChatHistory.from_id.distinct())).scalar()
        return count >= LIMIT_USER_LIST_COUNT


def user_id_exists(user_id: str):
    with Params().Session() as session:
        return session.query(ChatHistory.from_id).filter(ChatHistory.from_id == user_id).scalar() is not None
