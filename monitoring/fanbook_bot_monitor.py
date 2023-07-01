from prometheus_client import start_http_server
from sqlalchemy import func, and_, text
from datetime import datetime
import time
import schedule
from src.utils.param_singleton import Params
from database.mysql import ChatHistory
from src.utils.metrics import DAU_GAUGE
from src.utils.metrics import HAU_GAUGE, TOTAL_USERS_GAUGE, MESSAGE_HISTOGRAM


FETCH_CHAT_MESSAGE_BATCH_SIZE = 100


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


def update_hau_metric():
    HAU_GAUGE.set(get_hau())


def update_total_users_metric():
    with Params().Session() as session:
        count = session.query(func.count(ChatHistory.from_id.distinct())).scalar()
        TOTAL_USERS_GAUGE.set(count)


def get_hau():
    # Get current date and hour
    now = datetime.now()

    # Define start and end of the hour
    start_of_hour = datetime(now.year, now.month, now.day, now.hour, 0, 0)
    end_of_hour = datetime(now.year, now.month, now.day, now.hour, 59, 59)

    # Query unique users within this range
    with Params().Session() as session:
        unique_users = (
            session.query(func.count(ChatHistory.from_id.distinct()))
            .filter(and_(ChatHistory.update_time >= start_of_hour, ChatHistory.update_time <= end_of_hour))
            .scalar()
        )

    return unique_users


def get_messages_data():
    query = text(
        """
        SELECT first_name, is_private, COUNT(*) AS num_msg
        FROM avatar_chat_history
        WHERE first_name != 'ChatGPT'
        GROUP BY first_name, is_private
        ORDER BY is_private DESC, num_msg DESC
    """
    )

    # Batch size
    batch_size = FETCH_CHAT_MESSAGE_BATCH_SIZE
    data = []

    # Execute the query
    with Params().engine.connect() as connection:
        result = connection.execute(query)

        # Fetch results in batches
        while True:
            batch = result.fetchmany(batch_size)
            if not batch:
                break

            for row in batch:
                # Process each row in the batch
                # For example, print it:
                data.append(row)
    return data


def update_message_counter_histogram():
    data = get_messages_data()
    for first_name, is_private, number_of_messages in data:
        is_private_str = 'true' if is_private == 1 else 'false'
        MESSAGE_HISTOGRAM.labels(is_private=is_private_str).observe(number_of_messages)


if __name__ == '__main__':
    start_http_server(8001)

    schedule.every(60).seconds.do(update_dau_metric)

    schedule.every(30).seconds.do(update_hau_metric)

    schedule.every(30).seconds.do(update_total_users_metric)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)
