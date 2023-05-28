from src.utils.param_singleton import Params

# TODO(kezhang@): implement this im params
FANBOOK_BOT_NAME = Params().FANBOOK_BOT_NAME

BASE_URL = 'https://a1.fanbook.mobi/api'
GET_USER_TOKEN_TIMEOUT_COUNT = 3
FANBOOK_GET_ME_URL = f'{BASE_URL}/bot/{Params().FANBOOK_BOT_TOKEN}/getMe'
FANBOOK_SEND_MSG_URL = (
    f'https://a1.fanbook.mobi/api/bot/{Params().FANBOOK_BOT_TOKEN}/sendMessage'  # noqa
)
FANBOOK_CLIENT_ID = 500838395682099200
DEVICE_ID = f'bot{FANBOOK_CLIENT_ID}'
FANBOOK_VERSION = '1.6.60'
HEAT_BEAT_INTERVAL = 20
