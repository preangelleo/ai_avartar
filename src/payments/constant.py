CREDIT_PLAN_TIER_A = 'token_based_plan_a'
SUBSCRIPTION_PLAN = 'subscription_monthty_plan_B'

PLAN_CONFIG = {
    CREDIT_PLAN_TIER_A: {
        'conversation_credit': 100,
        'drawing_credit': 0,  # we do not differentiate between conversation and drawing credit
    },
    SUBSCRIPTION_PLAN: {
        'plan_duration_days': 30,
    },
}


CREDIT_BASED_PLAN = [CREDIT_PLAN_TIER_A]

SUBSCRIPTION_BASED_PLAN = [SUBSCRIPTION_PLAN]  # they have typo in the callback

PUBLIC_INIT_CHAT_CREDIT = 50
PUBLIC_INIT_DRAWING_CREDIT = 0


class ServiceType:
    conversation = 'conversation'
    drawing = 'drawing'
