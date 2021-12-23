import zerorpc
from const import RPC_ENDPOINT

if __name__ == '__main__':
    client = zerorpc.Client()
    client.connect(RPC_ENDPOINT)
    print(client.stop3())
