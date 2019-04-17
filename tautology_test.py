from BoolLogicFormula.BLFormula import BLFormula


if __name__ == '__main__':
    with open('TautologyTestCaseInput.txt', 'r') as inp:
        with open('TautologyTestCaseOutput.txt', 'w') as out:
            for line in inp.readlines():
                if line == '\n':
                    continue
                out.write('{} : {}\n'.format(line.strip('\n'), BLFormula(line.strip('\n')).is_tautology()))
