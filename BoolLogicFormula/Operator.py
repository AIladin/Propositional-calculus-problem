from functools import partial


class Operator(object):
    """
    'cheat' implementation of custom operators
    """
    def __init__(self, func):
        self.func = func

    def __or__(self, other):
        return self.func(other)

    def __ror__(self, other):
        return Operator(partial(self.func, other))

    def __call__(self, v1, v2):
        return self.func(v1, v2)


if __name__ == '__main__':
    a = Operator(lambda x, y: x+y)
    b = Operator(lambda x: x+1)
    print(1 | a | 2)
    print(2 | a | (b | 2))
