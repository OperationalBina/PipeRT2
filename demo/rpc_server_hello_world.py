import zerorpc


class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name


if __name__ == '__main__':
    server = zerorpc.Server(HelloRPC())
    server.bind("tcp://127.0.0.1:4242")
    server.run()
