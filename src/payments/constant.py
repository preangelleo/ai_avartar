from src.database.mysql import ServiceType

PLAN_CONFIG = {
    'token_based_plan_a': {
        ServiceType.CONVERSATION: 100,
        ServiceType.DRAWING: 10,
    }
}
