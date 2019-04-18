bin_tokens = {"conjuncture": '∧',
              "disjuncture": '∨',
              "implication": '->',
              "equivalence": '<->',
              "alternative": '+',
              'NAND': "NAND",
              'NOR': "NOR"}

un_tokens = {"objection": "!"}

parentheses = {'(', ')'}


class WrongExpression(Exception):
    """
    Wrong boolean expression exception
    """
    pass


def find_token(expression):
    """
    Finds main token in expression
    :param expression: boolean expression
    :return: indexes of token
    """
    if {expression[0], expression[-1]} != parentheses or ('()' in expression):
        raise WrongExpression
    beg = 0

    k = 0
    for i, ch in enumerate(expression):
        if ch == '(':
            k += 1
        elif ch == ')':
            k -= 1

        if k == 1 and i != 0:
            beg = i
            break

        if k < 0:
            raise WrongExpression

    try:
        end = expression[beg:].index('(')+beg
    except ValueError:
        raise WrongExpression(expression)

    if not beg:
        raise WrongExpression(expression)
    return beg, end


def fin_check(expresion):
    """
    If after all transformations left only token without variables
    :param expresion:
    :return:
    """
    for token in set(bin_tokens.values()).union(set(un_tokens.values())):
        if token in expresion:
            return False
    return True


def check_correctness(exp):
    """
    Gets boolean expression type '(((x1) -> ((x2) -> (x3))) -> (((x1) -> (x2)) -> ((x1) -> (x3))))'
    with all parentheses and logic operators from dict above.

    Deconstruct expression to analysis tree and check its correctness.
    Raise WrongExpression when unable to deconstruct.
    :param exp: string boolean expression
    :return:
    """
    def analise(expression):
        """

        :param expression: (((a)->(b))->(!(c)))
        :return:
        """
        if fin_check(expression):
            return

        # unary token
        if ('(' + un_tokens["objection"] + '(') == (expression[:2+len(un_tokens["objection"])]):
            left = expression[1+len(un_tokens["objection"]):-1]

            analise(left)
            return

        beg, end = find_token(expression)
        left = expression[1:beg+1]
        right = expression[end:-1]

        analise(left)
        analise(right)

    analise(exp)
    return


if __name__ == '__main__':
    t = '(((x1) -> ((x2) -> (x3))) -> (((x1) -> (x2)) -> ((x1) -> (x3))))'
    t1 = '(((!(x1)) → (!(x2))) → (((!(x1)) ∨ (x3)) ∨ ((x3) ∧ (!(x1)))))'
    print(check_correctness(t))
    print(check_correctness(t1))

