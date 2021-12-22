import zerorpc

from demo.const import RPC_ENDPOINT

if __name__ == '__main__':
    client = zerorpc.Client()
    client.connect(RPC_ENDPOINT)
    client.kill()
