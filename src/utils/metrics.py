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
    buckets=(1.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15, 17.5, 20, 25, 30, 40, 50, 60, 70, INF),
)
FUNCTION_CALL_LATENCY_METRICS = Histogram(
    'function_call_latency_sec',
    'Latency of a function call',
    ['function_name'],
    buckets=(1.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15, 17.5, 20, INF),
)
IMAGE_GENERATION_LATENCY_METRICS = Histogram(
    'image_generation_latency_sec',
    'Latency of whole image_generation',
    ['branch'],
    buckets=(1.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15, 17.5, 20, 25, 30, 40, 50, 60, 70, INF),
)
SEND_MSG_LATENCY_METRICS = Histogram('send_msg_latency_sec', 'Latency of send_msg', ['msg_len'])
SEND_IMAGE_LATENCY_METRICS = Histogram('send_img_latency_sec', 'Latency of send_img')

SUCCESS_REPLY_COUNTER = Counter('success_reply_total', 'Total Number of Successful Reply', ['branch'])

ERROR_COUNTER = Counter('error_total', 'Total Number of Error', ['reason', 'branch'])
TOTAL_USERS_GAUGE = Gauge('total_unique_users', 'Total unique users')
IMAGE_GENERATION_COUNTER = Counter('image_generated', 'Number image generated with given method.', ['method'])
OPENAI_PROMPT_TOKEN_USED_COUNTER = Counter(
    'openai_prompt_tokens_used', 'Number of prompt tokens used by the OpenAI API', ['branch']
)
OPENAI_COMPLETION_TOKEN_USED_COUNTER = Counter(
    'openai_completion_tokens_used', 'Number of completion tokens used by the OpenAI API', ['branch']
)
OPENAI_COST_USD_COUNTER = Counter('openai_cost_usd_used', 'Cost USD by the OpenAI API', ['branch'])
INITIAL_TEXT_REPLY_CRITIQUE_COUNTER = Counter('initial_text_reply_critique_counter', 'Critique Performed', ['reason'])

OPENAI_TOKEN_PER_CONVERSATION_HISTOGRAM = Histogram(
    'openai_tokens_per_conversation',
    'Number of tokens used per conversation',
    ['branch'],
    buckets=[1000.0] + list(range(2000, 4097, 100)) + [INF],
)
DAU_GAUGE = Gauge('daily_active_users', 'Daily Active Users')
HAU_GAUGE = Gauge('hourly_active_users', 'Hourly Active Users')
OPENAI_FINISH_REASON_COUNTER = Counter('openai_finish_reason_total', 'Total Number of Each Reasons', ['reason'])
