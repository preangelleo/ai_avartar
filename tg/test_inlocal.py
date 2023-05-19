from moralis import evm_api


api_key = "oYa3si8DJ41gaQWoggoNEfEQ5lrmuRTTodYUi7NpMiu8q73cfeo5XwHGS5CVuxLX"

params = {
    "transaction_hash": "0xd119eaf8c4e8abf89dae770e11b962f8034c0b10ba2c5f6164bd7b780695c564",
    "chain": "eth",
}

result = evm_api.transaction.get_transaction(
    api_key=api_key,
    params=params,
)

print(result)