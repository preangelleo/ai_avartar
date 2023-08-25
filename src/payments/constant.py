CREDIT_PLAN_TIER_A = 'token_based_plan_a'
SUBSCRIPTION_PLAN = 'subscription_monthty_plan_B'

PLAN_CONFIG = {
    CREDIT_PLAN_TIER_A: {
        'conversation_credit': 100,
        'drawing_credit': 10,
    },
    SUBSCRIPTION_PLAN: {
        'plan_duration_days': 30,
    },
}


CREDIT_BASED_PLAN = [CREDIT_PLAN_TIER_A]

SUBSCRIPTION_BASED_PLAN = [SUBSCRIPTION_PLAN]  # they have typo in the callback
