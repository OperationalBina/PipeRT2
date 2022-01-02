import zerorpc
from utlis import load_rpc_endpoint


class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name


if __name__ == '__main__':
    server = zerorpc.Server(HelloRPC())
    server.bind(load_rpc_endpoint())
    server.run()
