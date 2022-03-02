import os


def load_rpc_endpoint():
    return os.getenv('RPC_ENDPOINT', '0.0.0.0')
