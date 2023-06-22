from prometheus_client import start_http_server
from sqlalchemy import func, and_
from datetime import datetime
import time
import schedule
from src.utils.param_singleton import Params
from database.mysql import ChatHistory
from src.utils.metrics import DAU_GAUGE


def get_dau():
    # Get current date
    today = datetime.now().date()

    # Define start and end of the day
    start_of_day = datetime(today.year, today.month, today.day, 0, 0, 0)
    end_of_day = datetime(today.year, today.month, today.day, 23, 59, 59)

    # Query unique users within this range
    with Params().Session() as session:
        unique_users = (
            session.query(func.count(ChatHistory.from_id.distinct()))
            .filter(and_(ChatHistory.update_time >= start_of_day, ChatHistory.update_time <= end_of_day))
            .scalar()
        )

    return unique_users


def update_dau_metric():
    DAU_GAUGE.set(get_dau())


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8001)

    # Update the DAU metric every 5 seconds
    schedule.every(60).seconds.do(update_dau_metric)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)
