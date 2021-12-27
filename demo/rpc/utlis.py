import os
from dotenv import load_dotenv


def load_rpc_endpoint():
    load_dotenv('../config.env')
    return os.getenv('RPC_ENDPOINT')
