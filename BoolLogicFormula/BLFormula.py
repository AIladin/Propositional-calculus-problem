from BoolLogicFormula.Operator import *
from BoolLogicFormula.CheckCorrectness import check_correctness, WrongExpression
from itertools import product
# TODO sync with checkCorrectness tokens
bin_tokens = {'->': "imp", }

un_tokens = {"!": "obj", }


@Operator
def imp(arg1, arg2):

    assert type(arg1) == type(arg2) == bool, 'Implication wrong argument'

    if not arg1 or arg2:
        return True
    else:
        return False


@Operator
def obj(arg):
    assert type(arg) == bool, 'Implication wrong argument'
    return not arg


class BLFormula:
    def __init__(self, formula, variable_symbol='x', max_var_count=100):
        self.var_s = variable_symbol
        self.len = self._init_len(formula, max_var_count)

        self.f = self._prepare(formula)

    def _init_len(self, formula, max_var_count):
        for i in range(max_var_count):
            if formula.find(self.var_s+str(i)) == -1:
                return i

    def _check_correctness(self, formula):
        check_correctness(formula)
        if not formula:
            raise WrongExpression(formula)
        temp = formula
        for i in range(self.len):
            temp = temp.replace(self.var_s + str(i), '')
        for key, value in bin_tokens.items():
            temp = temp.replace(key, '')
        for key, value in un_tokens.items():
            temp = temp.replace(key, '')
        temp = temp.replace('(', '')
        temp = temp.replace(')', '')
        if len(temp) != 0:
            raise WrongExpression

    def _prepare(self, formula):
        formula = formula.replace(' ', '')
        for i in range(self.len):
            formula = formula.replace(self.var_s + str(i), '('+self.var_s + str(i)+')')
        self._check_correctness(formula)
        for key, value in bin_tokens.items():
            formula = formula.replace(key, '| '+value+' |')
        for key, value in un_tokens.items():
            formula = formula.replace(key, value+' |')
        return formula

    def is_tautology(self):
        pr = product([True, False], repeat=self.len)
        for t in pr:
            if not self(*t):
                return False
        return True

    def __repr__(self):
        return "Formula: {}\n var symbol: {}\n len: {}".format(self.f, self.var_s, self.len)

    def __call__(self, *args):
        if len(args) != self.len:
            raise TypeError("Formula takes {} positional argument but {} were given".format(self.len, len(args)))
        temp = self.f
        for i in range(self.len):
            temp = temp.replace(self.var_s+str(i), str(args[i]))
        return eval(temp)


if __name__ == '__main__':
    '''
    print(True | imp | True) = True
    print(True | imp | False) = False
    print(False | imp | True) = True
    print(False | imp | False) = True
    print(obj | True) = False
    print(obj | False) = True
    '''
    f = BLFormula('(x0 -> (!x0))')
    print(f.is_tautology())
