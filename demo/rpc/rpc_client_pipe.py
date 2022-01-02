import zerorpc
from utlis import load_rpc_endpoint

if __name__ == '__main__':
    client = zerorpc.Client()
    client.connect(load_rpc_endpoint())
    client.start()
