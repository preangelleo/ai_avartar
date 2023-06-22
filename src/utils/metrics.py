from prometheus_client import Counter, Gauge, Histogram

INF = float('inf')

IGNORED_MSG_COUNTER = Counter('ignored_msg_total', 'Num Ignored Msg')
PRIVATE_MSG_COUNTER = Counter('private_msg_total', 'Private Msg')

NON_LEGIT_USER_COUNTER = Counter('non_legit_total', 'Num non-legit Msg', ['reason'])

HANDLE_SINGLE_MSG_COUNTER = Counter('handle_single_msg_total', 'Handle single msg', ['branch'])


MSG_TEXT_LEN_METRICS = Histogram(
    'msg_text_len',
    'Length of current incoming message',
    ['branch'],
    buckets=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 50, 100, 200, 500, INF),
)
REPLY_TEXT_LEN_METRICS = Histogram(
    'reply_text_len', 'Length of reply message', ['branch'], buckets=(20, 30, 40, 50, 75, 100, 150, 200, 300, 500, INF)
)

OPENAI_LATENCY_METRICS = Histogram(
    'openai_latency_sec',
    'Latency of Open AI',
    ['msg_len', 'branch'],
    buckets=(1.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15, 17.5, 20, INF),
)
HANDLE_SINGLE_MSG_LATENCY_METRICS = Histogram(
    'handle_single_msg_latency_sec',
    'Latency of whole handle_single_msg',
    ['msg_len', 'branch'],
    buckets=(1.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15, 17.5, 20, INF),
)
SEND_MSG_LATENCY_METRICS = Histogram('send_msg_latency_sec', 'Latency of send_msg', ['msg_len'])

SUCCESS_REPLY_COUNTER = Counter('success_reply_total', 'Total Number of Successful Reply', ['branch'])
ERROR_COUNTER = Counter('error_total', 'Total Number of Error', ['reason', 'branch'])
NEW_USER_COUNTER = Counter('new_user_total', 'Number of New User')
TOTAL_USERS_GAUGE = Gauge('total_unique_users', 'Total unique users')
OPENAI_TOKEN_USED_COUNTER = Counter('openai_tokens_used', 'Number of tokens used by the OpenAI API')
DAU_GAUGE = Gauge('daily_active_users', 'Daily Active Users')
