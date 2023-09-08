CREDIT_PLAN_TIER_A = 'token_based_plan_a'
CREDIT_PLAN_TIER_B = 'token_based_plan_b'
SUBSCRIPTION_PLAN_TEST = 'subscription_monthty_plan_B'  # they have typo in the callback in test
SUBSCRIPTION_PLAN_PROD = 'subscription_monthly_plan_A'

PLAN_CONFIG = {
    CREDIT_PLAN_TIER_A: {
        'conversation_credit': 50,
        'drawing_credit': 0,  # we do not differentiate between conversation and drawing credit
    },
    CREDIT_PLAN_TIER_B: {
        'conversation_credit': 110,
        'drawing_credit': 0,  # we do not differentiate between conversation and drawing credit
    },
    SUBSCRIPTION_PLAN_TEST: {
        'plan_duration_days': 30,
    },
    SUBSCRIPTION_PLAN_PROD: {
        'plan_duration_days': 30,
    },
}


CREDIT_BASED_PLAN = [CREDIT_PLAN_TIER_A, CREDIT_PLAN_TIER_B]

SUBSCRIPTION_BASED_PLAN = [SUBSCRIPTION_PLAN_TEST, SUBSCRIPTION_PLAN_PROD]  # they have typo in the callback

PUBLIC_INIT_CHAT_CREDIT = 15
PUBLIC_INIT_DRAWING_CREDIT = 0


class ServiceType:
    conversation = 'conversation'
    drawing = 'drawing'
