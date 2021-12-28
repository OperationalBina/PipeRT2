import os
from dotenv import load_dotenv


def load_rpc_endpoint():
    load_dotenv()
    return os.getenv('RPC_ENDPOINT')
