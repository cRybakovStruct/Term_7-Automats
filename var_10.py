class LexicalAnalyzer():

    def __init__(self):
        self.index = 0
        self.input_string = ''
        self.lexems = []
        self.buff = ''
        self.math_symbols = '()&|^<>'
        self.variables = {}

    def setVariables(self, variables):
        self.variables = variables

    def replaceVariables(self):
        for i, lexem in enumerate(self.lexems):
            try:
                self.lexems[i] = {
                    'number': self.variables[self.lexems[i]['variable']]}
            except:
                pass

        for lexem in self.lexems:
            try:
                _ = lexem['variable']
                return False
            except:
                pass

        return True

    def lexicalAnalyzer(self, s_input: str):
        '''
            The function parses the incoming string to list of lexems
            Params
            ------
                input : str
                string with expression for analysis
            Returns
            ------
                result : list
                list of lexems'''
        self.input_string = s_input
        self.q_0()
        print(self.lexems)
        if not self.replaceVariables():
            print('Не удалось найти значения некоторых переменных')
        print(self.lexems)

    def getch(self):
        try:
            res = self.input_string[self.index]
            self.index += 1
            return res
        except:
            return None

    def q_0(self):
        print('q_0')
        symbol = self.getch()

        # if we catched the end of string
        if not symbol:
            return False

        # skip all spaces
        if symbol.isspace():
            return self.q_0()

        # read start of number
        elif symbol in '01':
            self.buff += symbol
            return self.q_1()

        # read symbols from set: (, ), +, -, *, /
        elif symbol in self.math_symbols:
            self.buff += symbol
            self.index += 1
            return self.q_res({'operation': symbol})

        # unsexpected symbols
        elif symbol in '23456789':
            self.buff += symbol
            return self.q_eror(f'Получено: {symbol} в лексеме {self.buff}, в то время как цифра не должна превышать 4')

        # read start of variable name
        elif symbol.isalpha:
            self.buff += symbol
            return self.q_2()

    def q_1(self):
        print('q_1')
        symbol = self.getch()

        # if we catched end of string it means that we finish read the number
        if not symbol:
            self.index += 1
            return self.q_res({'number': int(self.buff)})

        # if we catched space or (, ), +, -, *, / it means that we finish read the number
        elif (symbol.isspace() or symbol in self.math_symbols):
            return self.q_res({'number': int(self.buff)})

        # read next digit for number
        elif symbol in '01':
            self.buff += symbol
            return self.q_1()

        # unexpected sumbols
        elif (symbol.isalpha or symbol in '23456789'):
            self.buff += symbol
            return self.q_eror(f'Ожидается цифра или знак арифметической операции, в то время как получено: {symbol} в лексеме {self.buff}')

    def q_2(self):
        print('q_2')
        symbol = self.getch()

        # if we catched end of string it means that we finish read the variable
        if not symbol:
            self.index += 1
            return self.q_res({'variable': self.buff})

        # if we catched space or (, ), +, -, *, /  it means that we finish read the name of variable
        elif (symbol.isspace() or symbol in self.math_symbols):
            return self.q_res({'variable': self.buff})

        # read next symbol for name of variable
        elif symbol.isalnum:
            self.buff += symbol
            return self.q_2()

    def q_eror(self, msg: str):
        print(f'Error: {msg}')
        return None

    def q_res(self, lexem):
        print(f'Pushing: {lexem}')
        self.lexems.append(lexem)
        self.index -= 1
        self.buff = ''
        return self.q_0()


la = LexicalAnalyzer()
la.setVariables({'var1': '11'})
la.lexicalAnalyzer('(1 & 10 | 00 ^ 1) > var1 < 10')
