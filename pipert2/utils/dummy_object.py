class Dummy(object):
    """An object that have any attribute
    Useful for being a default value in unset parameter.

    """

    def do(self, *args, **kw): return self
    def __getattr__(self, _): return self.do
    def __call__(self, *args, **kwargs): return self.do
