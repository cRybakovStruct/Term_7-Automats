import datetime
import os.path


class LexicalAnalyzer():

    def __init__(self):
        self.index = 0
        self.input_string = ''
        self.lexems = []
        self.buff = ''
        self.math_symbols = '()&|^<>'
        self.variables = {}

    def writeToLog(self, msg):
        fout = open(
            './LexicalAnalyzer.log', 'ta')
        fout.write(str(msg)+'\n')
        print(msg)
        fout.close()

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
        self.writeToLog(
            f'\tSyntax analyzer started at [{datetime.datetime.now()}]')
        self.input_string = s_input
        self.q_0()
        self.writeToLog(self.lexems)
        if not self.replaceVariables():
            self.writeToLog('Не удалось найти значения некоторых переменных')
        self.lexems.append({'not_terminal': '$'})
        return self.lexems

    def getch(self):
        try:
            res = self.input_string[self.index]
            self.index += 1
            return res
        except:
            return None

    def q_0(self):
        self.writeToLog('This is q_0')
        symbol = self.getch()

        # if we catched the end of string
        if not symbol:
            return False

        # skip all spaces
        if symbol.isspace():
            self.writeToLog('\tGo\tfrom\tq_0 \tto\tq_0 \twith\t"space"')
            return self.q_0()

        # read start of number
        elif symbol in '01':
            self.buff += symbol
            self.writeToLog(f'\tGo\tfrom\tq_0 \tto\tq_1 \twith\t{symbol}')
            return self.q_1()

        # read symbols from set: (, ), |, ^, &, <, >
        elif symbol in self.math_symbols:
            self.buff += symbol
            self.index += 1
            self.writeToLog(f'\tGo\tfrom\tq_0 \tto\tq_res \twith\t{symbol}')
            return self.q_res({'operation': symbol})

        # unsexpected symbols
        elif symbol in '23456789':
            self.buff += symbol
            self.writeToLog(f'\tGo\tfrom\tq_0 \tto\tq_err \twith\t{symbol}')
            return self.q_err(f'Получено: {symbol} в лексеме {self.buff}, в то время как цифра не должна превышать 4')

        # read start of variable name
        elif symbol.isalpha:
            self.buff += symbol
            self.writeToLog(f'\tGo\tfrom\tq_0 \tto\tq_2 \twith\t{symbol}')
            return self.q_2()

    def q_1(self):
        self.writeToLog('This is q_1')
        symbol = self.getch()

        # if we catched end of string it means that we finish read the number
        if not symbol:
            self.index += 1
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\tq_res \twith\tEnd of string')
            return self.q_res({'number': int(self.buff, 2)})

        # if we catched space or (, ), +, -, *, / it means that we finish read the number
        elif (symbol.isspace() or symbol in self.math_symbols):
            self.writeToLog(f'\tGo\tfrom\tq_1 \tto\tq_res \twith\t{symbol}')
            return self.q_res({'number': int(self.buff, 2)})

        # read next digit for number
        elif symbol in '01':
            self.buff += symbol
            self.writeToLog(f'\tGo\tfrom\tq_1 \tto\tq_1 \twith\t{symbol}')
            return self.q_1()

        # unexpected sumbols
        elif (symbol.isalpha or symbol in '23456789'):
            self.buff += symbol
            self.writeToLog(f'\tGo\tfrom\tq_1 \tto\tq_err \twith\t{symbol}')
            return self.q_err(f'Ожидается цифра или знак арифметической операции, в то время как получено: {symbol} в лексеме {self.buff}')

    def q_2(self):
        self.writeToLog('This is q_2')
        symbol = self.getch()

        # if we catched end of string it means that we finish read the variable
        if not symbol:
            self.index += 1
            self.writeToLog(
                f'\tGo\tfrom\tq_2 \tto\tq_res \twith\tEnd of string')
            return self.q_res({'variable': self.buff})

        # if we catched space or (, ), &, ^, |, <, >  it means that we finish read the name of variable
        elif (symbol.isspace() or symbol in self.math_symbols):
            self.writeToLog(f'\tGo\tfrom\tq_2 \tto\tq_res \twith\t{symbol}')
            return self.q_res({'variable': self.buff})

        # read next symbol for name of variable
        elif symbol.isalnum:
            self.buff += symbol
            self.writeToLog(f'\tGo\tfrom\tq_2 \tto\tq_2 \twith\t{symbol}')
            return self.q_2()

    def q_err(self, msg: str):
        self.writeToLog('This is q_err')
        self.writeToLog(f'\tError: {msg}')
        raise IncorrectLexic('Incorrect input string')

    def q_res(self, lexem):
        self.writeToLog('This is q_res')
        self.writeToLog(f'\tPushing: {lexem}')
        self.lexems.append(lexem)
        self.index -= 1
        self.buff = ''
        return self.q_0()


class SyntaxAnalyzer():
    def __init__(self):
        self.index = 0
        self.stack = []

    def writeToLog(self, msg):
        fout = open(
            './SyntaxAnalyzer.log', 'ta')
        fout.write(str(msg)+'\n')
        print(msg)
        fout.close()

    def myOutput(self, msg):
        fout = open(
            './Var10_output.log', 'ta')
        fout.write(str(msg)+'\n')
        fout.close()

    def getLexemData(self):
        try:
            lexem = self.main_stack[self.index]
            lexem_type = list(lexem)[0]
            lexem_value = lexem[lexem_type]
        except:
            lexem_type = ''
            lexem_value = None
        return (lexem_type, lexem_value)

    def getLexemValues(self):
        res = []
        for lexem in self.main_stack:
            res.append(str(lexem[list(lexem)[0]]))
        return ' '.join(res)

    def syntaxAnalyzer(self, main_stack):
        self.writeToLog(
            f'Syntax analyzer started at [{datetime.datetime.now()}]')
        self.myOutput(
            f'Syntax analyzer started at [{datetime.datetime.now()}]')
        self.main_stack = main_stack
        self.q_1()
        res = str(bin(self.stack[0])).split('b')[1]
        self.myOutput(f'Result: {res}')
        self.writeToLog(res)
        return res

    def q_1(self):
        self.writeToLog('This is q_1')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.myOutput('\t' + str(self.getLexemValues()) + '\n')
        self.index = 0
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == 'S':
            self.writeToLog('Finish!')
            return

        if lexem_value == '>':
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\ts_7 \twith:\t{lexem_value}')
            self.q_7()
        elif lexem_value == '<':
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\ts_6 \twith:\t{lexem_value}')
            self.q_6()
        elif lexem_value == '(':
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\ts_9 \twith:\t{lexem_value}')
            self.q_9()
        elif lexem_value == 'E':
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\ts_2 \twith:\t{lexem_value}')
            self.q_2()
        elif lexem_value == 'T':
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\ts_3 \twith:\t{lexem_value}')
            self.q_3()
        elif lexem_value == 'K':
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\ts_4 \twith:\t{lexem_value}')
            self.q_4()
        elif lexem_value == 'L':
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\ts_5 \twith:\t{lexem_value}')
            self.q_5()
        elif lexem_type == 'number':
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\ts_8 \twith:\t{lexem_value}')
            self.q_8()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_1 \tto\ts_err \twith:\t{lexem_value}')
            self.q_err()

    def q_2(self):
        self.writeToLog('This is q_2')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '|':
            self.writeToLog(
                f'\tGo\tfrom\tq_2 \tto\ts_11 \twith:\t{lexem_value}')
            self.q_11()
        elif lexem_value == '$':
            self.writeToLog(
                f'\tGo\tfrom\tq_2 \tto\ts_10 \twith:\t{lexem_value}')
            self.q_10()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_2 \tto\ts_err \twith:\t{lexem_value}')
            self.q_err()

    def q_3(self):
        self.writeToLog('This is q_3')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '|':
            self.writeToLog(
                f'\tGo\tfrom\tq_3 \tto\tr_3 \twith:\t{lexem_value}')
            self.r_3()
        elif lexem_value == '^':
            self.writeToLog(
                f'\tGo\tfrom\tq_3 \tto\ts_12 \twith:\t{lexem_value}')
            self.q_12()
        elif lexem_value == ')':
            self.writeToLog(
                f'\tGo\tfrom\tq_3 \tto\tr_3 \twith:\t{lexem_value}')
            self.r_3()
        elif lexem_value == '$':
            self.writeToLog(
                f'\tGo\tfrom\tq_3 \tto\tr_3 \twith:\t{lexem_value}')
            self.r_3()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_3 \tto\ts_err \twith:\t{lexem_value}')
            self.q_err()

    def q_4(self):
        self.writeToLog('This is q_4')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '|':
            self.writeToLog(
                f'\tGo\tfrom\tq_4 \tto\tr_5 \twith:\t{lexem_value}')
            self.r_5()
        elif lexem_value == '&':
            self.writeToLog(
                f'\tGo\tfrom\tq_4 \tto\tq_13 \twith:\t{lexem_value}')
            self.q_13()
        elif lexem_value == '^':
            self.writeToLog(
                f'\tGo\tfrom\tq_4 \tto\tr_5 \twith:\t{lexem_value}')
            self.r_5()
        elif lexem_value == ')':
            self.writeToLog(
                f'\tGo\tfrom\tq_4 \tto\tr_5 \twith:\t{lexem_value}')
            self.r_5()
        elif lexem_value == '$':
            self.writeToLog(
                f'\tGo\tfrom\tq_4 \tto\tr_5 \twith:\t{lexem_value}')
            self.r_5()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_4 \tto\tr_err \twith:\t{lexem_value}')
            self.q_err()

    def q_5(self):
        self.writeToLog('This is q_5')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.writeToLog(f'\tGo\tfrom\tq_5 \tto\tr_7 \twith:\t{lexem_value}')
        self.r_7()

    def q_6(self):
        self.writeToLog('This is q_6')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '>':
            self.writeToLog(
                f'\tGo\tfrom\tq_6 \tto\tq_7 \twith:\t{lexem_value}')
            self.q_7()
        elif lexem_value == '<':
            self.writeToLog(
                f'\tGo\tfrom\tq_6 \tto\tq_6 \twith:\t{lexem_value}')
            self.q_6()
        elif lexem_value == '(':
            self.writeToLog(
                f'\tGo\tfrom\tq_6 \tto\tq_9 \twith:\t{lexem_value}')
            self.q_9()
        elif lexem_value == 'L':
            self.writeToLog(
                f'\tGo\tfrom\tq_6 \tto\tq_14 \twith:\t{lexem_value}')
            self.q_14()
        elif lexem_type == 'number':
            self.writeToLog(
                f'\tGo\tfrom\tq_6 \tto\tq_8 \twith:\t{lexem_value}')
            self.q_8()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_6 \tto\tq_err \twith:\t{lexem_value}')
            self.q_err()

    def q_7(self):
        self.writeToLog('This is q_7')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '>':
            self.writeToLog(
                f'\tGo\tfrom\tq_7 \tto\tq_7 \twith:\t{lexem_value}')
            self.q_7()
        elif lexem_value == '<':
            self.writeToLog(
                f'\tGo\tfrom\tq_7 \tto\tq_6 \twith:\t{lexem_value}')
            self.q_6()
        elif lexem_value == '(':
            self.writeToLog(
                f'\tGo\tfrom\tq_7 \tto\tq_9 \twith:\t{lexem_value}')
            self.q_9()
        elif lexem_value == 'L':
            self.writeToLog(
                f'\tGo\tfrom\tq_7 \tto\tq_15 \twith:\t{lexem_value}')
            self.q_15()
        elif lexem_type == 'number':
            self.writeToLog(
                f'\tGo\tfrom\tq_7 \tto\tq_8 \twith:\t{lexem_value}')
            self.q_8()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_7 \tto\tq_err \twith:\t{lexem_value}')
            self.q_err()

    def q_8(self):
        self.writeToLog('This is q_8')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.writeToLog(f'\tGo\tfrom\tq_8 \tto\tr_10 \twith:\t{lexem_value}')
        self.r_10()

    def q_9(self):
        self.writeToLog('This is q_9')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '>':
            self.writeToLog(
                f'\tGo\tfrom\tq_9 \tto\tq_7 \twith:\t{lexem_value}')
            self.q_7()
        elif lexem_value == '<':
            self.writeToLog(
                f'\tGo\tfrom\tq_9 \tto\tq_6 \twith:\t{lexem_value}')
            self.q_6()
        elif lexem_value == '(':
            self.writeToLog(
                f'\tGo\tfrom\tq_9 \tto\tq_9 \twith:\t{lexem_value}')
            self.q_9()
        elif lexem_value == 'E':
            self.writeToLog(
                f'\tGo\tfrom\tq_9 \tto\tq_16 \twith:\t{lexem_value}')
            self.q_16()
        elif lexem_value == 'T':
            self.writeToLog(
                f'\tGo\tfrom\tq_9 \tto\tq_3 \twith:\t{lexem_value}')
            self.q_3()
        elif lexem_value == 'K':
            self.writeToLog(
                f'\tGo\tfrom\tq_9 \tto\tq_4 \twith:\t{lexem_value}')
            self.q_4()
        elif lexem_value == 'L':
            self.writeToLog(
                f'\tGo\tfrom\tq_9 \tto\tq_5 \twith:\t{lexem_value}')
            self.q_5()
        elif lexem_type == 'number':
            self.writeToLog(
                f'\tGo\tfrom\tq_9 \tto\tq_8 \twith:\t{lexem_value}')
            self.q_8()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_9 \tto\tq_err \twith:\t{lexem_value}')
            self.q_err()

    def q_10(self):
        self.writeToLog('This is q_10')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.writeToLog(f'\tGo\tfrom\tq_10 \tto\tr_1 \twith:\t{lexem_value}')
        self.r_1()

    def q_11(self):
        self.writeToLog('This is q_11')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '>':
            self.writeToLog(
                f'\tGo\tfrom\tq_11 \tto\tq_7 \twith:\t{lexem_value}')
            self.q_7()
        elif lexem_value == '<':
            self.writeToLog(
                f'\tGo\tfrom\tq_11 \tto\tq_6 \twith:\t{lexem_value}')
            self.q_6()
        elif lexem_value == '(':
            self.writeToLog(
                f'\tGo\tfrom\tq_11 \tto\tq_9 \twith:\t{lexem_value}')
            self.q_9()
        elif lexem_value == 'T':
            self.writeToLog(
                f'\tGo\tfrom\tq_11 \tto\tq_17 \twith:\t{lexem_value}')
            self.q_17()
        elif lexem_value == 'K':
            self.writeToLog(
                f'\tGo\tfrom\tq_11 \tto\tq_4 \twith:\t{lexem_value}')
            self.q_4()
        elif lexem_value == 'L':
            self.writeToLog(
                f'\tGo\tfrom\tq_11 \tto\tq_5 \twith:\t{lexem_value}')
            self.q_5()
        elif lexem_type == 'number':
            self.writeToLog(
                f'\tGo\tfrom\tq_11 \tto\tq_8 \twith:\t{lexem_value}')
            self.q_8()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_11 \tto\tq_err \twith:\t{lexem_value}')
            self.q_err()

    def q_12(self):
        self.writeToLog('This is q_12')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '>':
            self.writeToLog(
                f'\tGo\tfrom\tq_12 \tto\tq_7 \twith:\t{lexem_value}')
            self.q_7()
        elif lexem_value == '<':
            self.writeToLog(
                f'\tGo\tfrom\tq_12 \tto\tq_6 \twith:\t{lexem_value}')
            self.q_6()
        elif lexem_value == '(':
            self.writeToLog(
                f'\tGo\tfrom\tq_12 \tto\tq_9 \twith:\t{lexem_value}')
            self.q_9()
        elif lexem_value == 'K':
            self.writeToLog(
                f'\tGo\tfrom\tq_12 \tto\tq_18 \twith:\t{lexem_value}')
            self.q_18()
        elif lexem_value == 'L':
            self.writeToLog(
                f'\tGo\tfrom\tq_12 \tto\tq_5 \twith:\t{lexem_value}')
            self.q_5()
        elif lexem_type == 'number':
            self.writeToLog(
                f'\tGo\tfrom\tq_12 \tto\tq_8 \twith:\t{lexem_value}')
            self.q_8()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_12 \tto\tq_err \twith:\t{lexem_value}')
            self.q_err()

    def q_13(self):
        self.writeToLog('This is q_13')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '>':
            self.writeToLog(
                f'\tGo\tfrom\tq_13 \tto\tq_7 \twith:\t{lexem_value}')
            self.q_7()
        elif lexem_value == '<':
            self.writeToLog(
                f'\tGo\tfrom\tq_13 \tto\tq_6 \twith:\t{lexem_value}')
            self.q_6()
        elif lexem_value == '(':
            self.writeToLog(
                f'\tGo\tfrom\tq_13 \tto\tq_9 \twith:\t{lexem_value}')
            self.q_9()
        elif lexem_value == 'L':
            self.writeToLog(
                f'\tGo\tfrom\tq_13 \tto\tq_19 \twith:\t{lexem_value}')
            self.q_19()
        elif lexem_type == 'number':
            self.writeToLog(
                f'\tGo\tfrom\tq_13 \tto\tq_8 \twith:\t{lexem_value}')
            self.q_8()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_13 \tto\tq_err \twith:\t{lexem_value}')
            self.q_err()

    def q_14(self):
        self.writeToLog('This is q_14')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.writeToLog(f'\tGo\tfrom\tq_14 \tto\tr_8 \twith:\t{lexem_value}')
        self.r_8()

    def q_15(self):
        self.writeToLog('This is q_15')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.writeToLog(f'\tGo\tfrom\tq_15 \tto\tr_9 \twith:\t{lexem_value}')
        self.r_9()

    def q_16(self):
        self.writeToLog('This is q_16')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '|':
            self.writeToLog(
                f'\tGo\tfrom\tq_16 \tto\tq_11 \twith:\t{lexem_value}')
            self.q_11()
        elif lexem_value == ')':
            self.writeToLog(
                f'\tGo\tfrom\tq_16 \tto\tq_16 \twith:\t{lexem_value}')
            self.q_20()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_16 \tto\tq_err \twith:\t{lexem_value}')
            self.q_err()

    def q_17(self):
        self.writeToLog('This is q_17')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '|':
            self.writeToLog(
                f'\tGo\tfrom\tq_17 \tto\tr_2 \twith:\t{lexem_value}')
            self.r_2()
        elif lexem_value == '^':
            self.writeToLog(
                f'\tGo\tfrom\tq_17 \tto\tq_12 \twith:\t{lexem_value}')
            self.q_12()
        elif lexem_value == ')':
            self.writeToLog(
                f'\tGo\tfrom\tq_17 \tto\tr_2 \twith:\t{lexem_value}')
            self.r_2()
        elif lexem_value == '$':
            self.writeToLog(
                f'\tGo\tfrom\tq_17 \tto\tr_2 \twith:\t{lexem_value}')
            self.r_2()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_17 \tto\tq_err \twith:\t{lexem_value}')
            self.q_err()

    def q_18(self):
        self.writeToLog('This is q_18')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '|':
            self.writeToLog(
                f'\tGo\tfrom\tq_18 \tto\tr_4 \twith:\t{lexem_value}')
            self.r_4()
        elif lexem_value == '&':
            self.writeToLog(
                f'\tGo\tfrom\tq_18 \tto\tq_13 \twith:\t{lexem_value}')
            self.q_13()
        elif lexem_value == '^':
            self.writeToLog(
                f'\tGo\tfrom\tq_18 \tto\tr_10 \twith:\t{lexem_value}')
            self.r_10()
        elif lexem_value == ')':
            self.writeToLog(
                f'\tGo\tfrom\tq_18 \tto\tr_4 \twith:\t{lexem_value}')
            self.r_4()
        elif lexem_value == '$':
            self.writeToLog(
                f'\tGo\tfrom\tq_18 \tto\tr_4 \twith:\t{lexem_value}')
            self.r_4()
        else:
            self.writeToLog(
                f'\tGo\tfrom\tq_18 \tto\tr_err \twith:\t{lexem_value}')
            self.q_err()

    def q_19(self):
        self.writeToLog('This is q_19')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.writeToLog(f'\tGo\tfrom\tq_19 \tto\tr_6 \twith:\t{lexem_value}')
        self.r_6()

    def q_20(self):
        self.writeToLog('This is q_20')
        self.writeToLog(f'\tStack:\t{self.getLexemValues()}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.writeToLog(f'\tGo\tfrom\tq_20 \tto\tr_11 \twith:\t{lexem_value}')
        self.r_11()

    def q_err(self):
        self.writeToLog('This is q_err')
        raise IncorrectSyntax('Incorrect or unexpected lexem')

    def r_1(self):
        self.writeToLog('This is r_1')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()
        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-1]
        self.main_stack.append({'not_terminal': 'S'})
        self.main_stack += tmp
        self.writeToLog(f'\tGo\tfrom\tr_1 \tto\ts_0 \tpack 1:\t"S->E$"')
        self.myOutput('Reduce 1: S -> E$')
        self.q_1()

    def r_2(self):
        self.writeToLog('This is r_2')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()
        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'E'})
        self.main_stack += tmp
        self.writeToLog(f'\tGo\tfrom\tr_2 \tto\ts_0 \tpack 2:\t"E->E|T"')
        new_res = self.stack[-2] | self.stack[-1]
        self.writeToLog(
            f'\tCount:\t{self.stack[-2]} | {self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-2]
        self.stack.append(new_res)
        self.myOutput('Reduce 2: E -> E | T')
        self.q_1()

    def r_3(self):
        self.writeToLog('This is r_3')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()
        self.main_stack[self.index] = {'not_terminal': 'E'}
        self.writeToLog(f'\tGo\tfrom\tr_3 \tto\ts_0 \tpack 3:\t"E->T"')
        self.myOutput('Reduce 3: E -> T')
        self.q_1()

    def r_4(self):
        self.writeToLog('This is r_4')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()
        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'T'})
        self.main_stack += tmp
        self.writeToLog(f'\tGo\tfrom\tr_4 \tto\ts_0 \tpack 4:\t"T->T^K"')
        new_res = self.stack[-2] ^ self.stack[-1]
        self.writeToLog(
            f'\tCount:\t{self.stack[-2]} ^ {self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-2]
        self.stack.append(new_res)
        self.myOutput('Reduce 4: T -> T ^ K')
        self.q_1()

    def r_5(self):
        self.writeToLog('This is r_5')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()
        self.main_stack[self.index] = {'not_terminal': 'T'}
        self.writeToLog(f'\tGo\tfrom\tr_5 \tto\ts_0 \tpack 5:\t"T->K"')
        self.myOutput('Reduce 5: T -> K')
        self.q_1()

    def r_6(self):
        self.writeToLog('This is r_6')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'K'})
        self.main_stack += tmp
        self.writeToLog(f'\tGo\tfrom\tr_6 \tto\ts_0 \tpack 6:\t"K->K&L"')
        new_res = self.stack[-2] & self.stack[-1]
        self.writeToLog(
            f'\tCount:\t{self.stack[-2]} & {self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-2]
        self.stack.append(new_res)
        self.myOutput('Reduce 6: K -> K & L')
        self.q_1()

    def r_7(self):
        self.writeToLog('This is r_7')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()
        self.main_stack[self.index] = {'not_terminal': 'K'}
        self.writeToLog(f'\tGo\tfrom\tr_7 \tto\ts_0 \tpack 7:\t"K->L"')
        self.myOutput('Reduce 7: K -> L')
        self.q_1()

    def r_8(self):
        self.writeToLog('This is r_8')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-1]
        self.main_stack.append({'not_terminal': 'L'})
        self.main_stack += tmp
        self.writeToLog(f'\tGo\tfrom\tr_1 \tto\ts_0 \tpack 1:\t"L-> <L"')
        new_res = self.stack[-1] << 1
        self.writeToLog(
            f'\tCount:\t>{self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-1]
        self.stack.append(new_res)
        self.myOutput('Reduce 8: L -> <L')
        self.q_1()

    def r_9(self):
        self.writeToLog('This is r_9')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-1]
        self.main_stack.append({'not_terminal': 'L'})
        self.main_stack += tmp
        self.writeToLog(f'\tGo\tfrom\tr_1 \tto\ts_0 \tpack 1:\t"L-> >L"')
        new_res = self.stack[-1] >> 1
        self.writeToLog(
            f'\tCount:\t>{self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-1]
        self.stack.append(new_res)
        self.myOutput('Reduce 9: L -> >L')
        self.q_1()

    def r_10(self):
        self.writeToLog('This is r_10')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()
        self.stack.append(lexem_value)
        self.main_stack[self.index] = {'not_terminal': 'L'}
        self.writeToLog(f'\tGo\tfrom\tr_9 \tto\ts_0 \tpack 9:\t"L->num"')
        self.myOutput('Reduce 10: L -> num')
        self.q_1()

    def r_11(self):
        self.writeToLog('This is r_11')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()
        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'L'})
        self.main_stack += tmp
        self.writeToLog(f'\tGo\tfrom\tr_11 \tto\ts_0 \tpack 11:\t"L->(E)"')
        self.myOutput('Reduce 11: L -> (E)')
        self.q_1()


class AnalyserError(Exception):
    '''Some error in some analyser'''

    def __init__(self, message):
        self.message = message


class IncorrectLexic(AnalyserError):
    '''Incorrect input string'''

    def __init__(self, message):
        self.message = message


class IncorrectSyntax(AnalyserError):
    '''Incorrect or unexpected lexem'''

    def __init__(self, message):
        self.message = message


def parseVariables(variables):
    res_variables = {}

    for variable in variables:

        tmp = variable.split('=')

        la1 = LexicalAnalyzer()
        variable_name = list(la1.lexicalAnalyzer(tmp[0])[0].values())[0]

        la2 = LexicalAnalyzer()
        sa = SyntaxAnalyzer()
        variable_value = int(sa.syntaxAnalyzer(la2.lexicalAnalyzer(tmp[1])), 2)

        if (variable_name is not None) and (variable_value is not None):
            res_variables[variable_name] = variable_value

    return res_variables


try:
    # a = ['a=3+1', 'b=1*2']

    la1 = LexicalAnalyzer()
    # variables = parseVariables(a)
    # la1.setVariables(variables)
    stack = la1.lexicalAnalyzer('1&>0|1&0|(1&1)')
    print(stack)
    sa1 = SyntaxAnalyzer()
    sa1.syntaxAnalyzer(stack)
except IncorrectLexic as err:
    print(err.message)
except IncorrectSyntax as err:
    print(err.message)
except AnalyserError as err:
    print(err.message)
except ZeroDivisionError:
    print('Was zero-dividing')
