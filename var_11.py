import datetime
import os.path
import numpy as np


class LexicalAnalyzer():

    def __init__(self):
        self.index = 0
        self.input_string = ''
        self.lexems = []
        self.buff = ''
        self.math_symbols = '()*+#'
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
        func_name = 'q_0'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        # if we catched the end of string
        if not symbol:
            return

        # skip all spaces
        if symbol.isspace():
            self.q_0()

        elif symbol == '-':
            self.buff += symbol
            self.q_27()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_2()

        # read symbols from set: (, ), +, #, *
        elif symbol in self.math_symbols:
            self.buff += symbol
            self.index += 1
            self.q_res({'operation': symbol})

        # read start of variable name
        elif symbol.isalpha():
            self.buff += symbol
            self.q_1()

    def q_1(self):
        func_name = 'q_1'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if not symbol:
            self.index += 1
            self.q_res({'variable': self.buff})

        elif symbol.isalnum():
            self.buff += symbol
            self.q_1()

        elif symbol in self.math_symbols:
            # self.buff += symbol
            # self.index += 1
            self.q_res({'variable': self.buff})

        else:
            self.q_err()

    def q_2(self):
        func_name = 'q_2'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isdigit():
            self.buff += symbol
            self.q_2()

        elif symbol == ',':
            self.matrix = np.zeros((3, 3))
            # self.index += 1
            self.matrix[0, 0] = int(self.buff)
            self.buff = ''
            self.q_3()

        else:
            self.q_err()

    def q_3(self):
        func_name = 'q_3'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol == '-':
            self.buff += symbol
            self.q_19()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_4()

        elif symbol.isspace():
            self.q_3()

        else:
            self.q_err()

    def q_4(self):
        func_name = 'q_4'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isdigit():
            self.buff += symbol
            self.q_4()

        elif symbol == ',':

            # self.index += 1
            self.matrix[0, 1] = int(self.buff)
            self.buff = ''
            self.q_5()

        else:
            self.q_err()

    def q_5(self):
        func_name = 'q_5'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol == '-':
            self.buff += symbol
            self.q_20()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_6()

        elif symbol.isspace():
            self.q_5()

        else:
            self.q_err()

    def q_6(self):
        func_name = 'q_6'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isdigit():
            self.buff += symbol
            self.q_6()

        elif symbol == ',':

            # self.index += 1
            self.matrix[0, 2] = int(self.buff)
            self.buff = ''
            self.q_7()

        else:
            self.q_err()

    def q_7(self):
        func_name = 'q_7'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol == '-':
            self.buff += symbol
            self.q_21()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_8()

        elif symbol.isspace():
            self.q_7()

        else:
            self.q_err()

    def q_8(self):
        func_name = 'q_8'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isdigit():
            self.buff += symbol
            self.q_8()

        elif symbol == ',':

            # self.index += 1
            self.matrix[1, 0] = int(self.buff)
            self.buff = ''
            self.q_9()

        else:
            self.q_err()

    def q_9(self):
        func_name = 'q_9'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol == '-':
            self.buff += symbol
            self.q_22()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_10()

        elif symbol.isspace():
            self.q_9()

        else:
            self.q_err()

    def q_10(self):
        func_name = 'q_10'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isdigit():
            self.buff += symbol
            self.q_10()

        elif symbol == ',':

            # self.index += 1
            self.matrix[1, 1] = int(self.buff)
            self.buff = ''
            self.q_11()

        else:
            self.q_err()

    def q_11(self):
        func_name = 'q_11'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol == '-':
            self.buff += symbol
            self.q_23()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_12()

        elif symbol.isspace():
            self.q_11()

        else:
            self.q_err()

    def q_12(self):
        func_name = 'q_12'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isdigit():
            self.buff += symbol
            self.q_12()

        elif symbol == ',':

            # self.index += 1
            self.matrix[1, 2] = int(self.buff)
            self.buff = ''
            self.q_13()

        else:
            self.q_err()

    def q_13(self):
        func_name = 'q_31'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol == '-':
            self.buff += symbol
            self.q_24()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_14()

        elif symbol.isspace():
            self.q_13()

        else:
            self.q_err()

    def q_14(self):
        func_name = 'q_14'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isdigit():
            self.buff += symbol
            self.q_14()

        elif symbol == ',':

            # self.index += 1
            self.matrix[2, 0] = int(self.buff)
            self.buff = ''
            self.q_15()

        else:
            self.q_err()

    def q_15(self):
        func_name = 'q_15'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol == '-':
            self.buff += symbol
            self.q_25()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_16()

        elif symbol.isspace():
            self.q_15()

        else:
            self.q_err()

    def q_16(self):
        func_name = 'q_16'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isdigit():
            self.buff += symbol
            self.q_16()

        elif symbol == ',':

            # self.index += 1
            self.matrix[2, 1] = int(self.buff)
            self.buff = ''
            self.q_17()

        else:
            self.q_err()

    def q_17(self):
        func_name = 'q_17'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol == '-':
            self.buff += symbol
            self.q_27()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_18()

        elif symbol.isspace():
            self.q_17()

        else:
            self.q_err()

    def q_18(self):
        func_name = 'q_18'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if not symbol:
            self.index += 1
            self.matrix[2, 2] = int(self.buff)
            self.buff = ''
            self.q_res({'number': self.matrix})

        elif symbol.isdigit():
            self.buff += symbol
            self.q_18()

        elif (symbol in self.math_symbols or symbol.isspace()):

            # self.index += 1
            self.matrix[2, 2] = int(self.buff)
            self.buff = ''
            self.q_res({'number': self.matrix})

        else:
            self.q_err()

    def q_19(self):
        func_name = 'q_19'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isspace():
            self.q_19()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_4()

        else:
            self.q_err()

    def q_20(self):
        func_name = 'q_20'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isspace():
            self.q_20()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_6()

        else:
            self.q_err()

    def q_21(self):
        func_name = 'q_21'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isspace():
            self.q_21()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_8()

        else:
            self.q_err()

    def q_22(self):
        func_name = 'q_22'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isspace():
            self.q_22()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_10()

        else:
            self.q_err()

    def q_23(self):
        func_name = 'q_23'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isspace():
            self.q_23()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_12()

        else:
            self.q_err()

    def q_24(self):
        func_name = 'q_24'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isspace():
            self.q_24()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_14()

        else:
            self.q_err()

    def q_25(self):
        func_name = 'q_25'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isspace():
            self.q_25()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_16()

        else:
            self.q_err()

    def q_26(self):
        func_name = 'q_26'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isspace():
            self.q_26()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_18()

        else:
            self.q_err()

    def q_27(self):
        func_name = 'q_27'
        self.writeToLog(f'This is {func_name}')
        symbol = self.getch()

        if symbol.isspace():
            self.q_27()

        elif symbol.isdigit():
            self.buff += symbol
            self.q_2()

        else:
            self.q_err()

    def q_err(self):
        func_name = 'q_err'
        self.writeToLog(f'This is {func_name}')
        self.writeToLog('This is q_err')
        raise IncorrectLexic('Incorrect input string')

    def q_res(self, lexem):
        self.writeToLog(f'Pushing: {lexem}')
        self.lexems.append(lexem)
        self.index -= 1
        self.buff = ''
        self.q_0()


class SyntaxAnalyzer():
    def __init__(self, loglevel='Debug'):
        self.index = 0
        self.stack = []
        self.logfile = './Var11_output.log'
        self.loglevel = loglevel
        self.loglevels = {'Debug': 0, 'Info': 1}

    def clearLog(self):
        fout = open(self.logfile, 'w')
        fout.close()

    def writeToLog(self, msg, loglevel):
        print(msg)
        if self.loglevels[loglevel] >= self.loglevels[self.loglevel]:
            fout = open(self.logfile, 'ta')
            fout.write(str(msg)+'\n')
            fout.close()

    def Debug(self, msg):
        self.writeToLog(msg, 'Debug')

    def Info(self, msg):
        self.writeToLog(msg, 'Info')

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

    def dec_to_base(self, N):
        table = '01234'
        x, y = divmod(N, 5)
        return self.dec_to_base(x) + table[y] if x else table[y]

    def syntaxAnalyzer(self, main_stack):
        self.Info(
            f'Syntax analyzer started at [{datetime.datetime.now()}]')
        self.main_stack = main_stack
        self.q_0()
        res = self.stack[0]
        self.Info(f'Result: {res}')
        return res

    def q_0(self):
        func_name = 'q_0'
        self.Debug(f'this is {func_name}')
        self.Info(f'\tStack:\t{self.getLexemValues()}')
        self.index = 0
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == 'S':
            self.Debug('Finish!')
            return

        if lexem_value == '(':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_4 \twith\t{lexem_value}')
            self.q_4()

        elif lexem_value == 'E':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_1 \twith\t{lexem_value}')
            self.q_1()

        elif lexem_value == 'T':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_2 \twith\t{lexem_value}')
            self.q_2()

        elif lexem_value == 'F':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_3 \twith\t{lexem_value}')
            self.q_3()

        elif lexem_type == 'number':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_5 \twith\t{lexem_value}')
            self.q_5()

        else:
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_err \twith\t{lexem_value}')
            self.q_err()

    def q_1(self):
        func_name = 'q_1'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '+':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_7 \twith\t{lexem_value}')
            self.q_7()

        elif lexem_value == '#':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_8 \twith\t{lexem_value}')
            self.q_8()

        elif lexem_value == '$':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_6 \twith\t{lexem_value}')
            self.q_6()

        else:
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_err \twith\t{lexem_value}')
            self.q_err()

    def q_2(self):
        func_name = 'q_2'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '*':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_9 \twith\t{lexem_value}')
            self.q_9()

        elif lexem_value == ')':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_4 \twith\t{lexem_value}')
            self.r_4()

        elif lexem_value == '+':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_4 \twith\t{lexem_value}')
            self.r_4()

        elif lexem_value == '#':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_4 \twith\t{lexem_value}')
            self.r_4()

        elif lexem_value == '$':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_4 \twith\t{lexem_value}')
            self.r_4()

        else:
            self.q_err()

    def q_3(self):
        func_name = 'q_3'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.Debug(f'\tGo from\t{func_name} \tto\tr_6 \twith\t{lexem_value}')
        self.r_6()

    def q_4(self):
        func_name = 'q_4'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '(':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_4 \twith\t{lexem_value}')
            self.q_4()

        elif lexem_value == 'E':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_10 \twith\t{lexem_value}')
            self.q_10()

        elif lexem_value == 'T':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_2 \twith\t{lexem_value}')
            self.q_2()

        elif lexem_value == 'F':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_3 \twith\t{lexem_value}')
            self.q_3()

        elif lexem_type == 'number':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_5 \twith\t{lexem_value}')
            self.q_5()

        else:
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_err \twith\t{lexem_value}')
            self.q_err()

    def q_5(self):
        func_name = 'q_5'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.Debug(f'\tGo from\t{func_name} \tto\tt_8 \twith\t{lexem_value}')
        self.r_8()

    def q_6(self):
        func_name = 'q_6'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.Debug(f'\tGo from\t{func_name} \tto\tr_1 \twith\t{lexem_value}')
        self.r_1()

    def q_7(self):
        func_name = 'q_7'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '(':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_4 \twith\t{lexem_value}')
            self.q_4()

        elif lexem_value == 'T':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_11 \twith\t{lexem_value}')
            self.q_11()

        elif lexem_value == 'F':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_3 \twith\t{lexem_value}')
            self.q_3()

        elif lexem_type == 'number':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_5 \twith\t{lexem_value}')
            self.q_5()

        else:
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_err \twith\t{lexem_value}')
            self.q_err()

    def q_8(self):
        func_name = 'q_8'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '(':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_4 \twith\t{lexem_value}')
            self.q_4()

        elif lexem_value == 'T':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_12 \twith\t{lexem_value}')
            self.q_12()

        elif lexem_value == 'F':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_3 \twith\t{lexem_value}')
            self.q_3()

        elif lexem_type == 'number':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_5 \twith\t{lexem_value}')
            self.q_5()

        else:
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_err \twith\t{lexem_value}')
            self.q_err()

    def q_9(self):
        func_name = 'q_9'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '(':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_4 \twith\t{lexem_value}')
            self.q_4()

        elif lexem_value == 'F':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_13 \twith\t{lexem_value}')
            self.q_13()

        elif lexem_type == 'number':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_5 \twith\t{lexem_value}')
            self.q_5()

        else:
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_err \twith\t{lexem_value}')
            self.q_err()

    def q_10(self):
        func_name = 'q_10'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == ')':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_14 \twith\t{lexem_value}')
            self.q_14()

        elif lexem_value == '+':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_7 \twith\t{lexem_value}')
            self.q_7()

        elif lexem_value == '#':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_8 \twith\t{lexem_value}')
            self.q_8()

        else:
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_err \twith\t{lexem_value}')
            self.q_err()

    def q_11(self):
        func_name = 'q_11'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '*':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_9 \twith\t{lexem_value}')
            self.q_9()

        elif lexem_value == ')':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_2 \twith\t{lexem_value}')
            self.r_2()

        elif lexem_value == '+':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_2 \twith\t{lexem_value}')
            self.r_2()

        elif lexem_value == '#':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_2 \twith\t{lexem_value}')
            self.r_2()

        elif lexem_value == '$':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_2 \twith\t{lexem_value}')
            self.r_2()

        else:
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_err \twith\t{lexem_value}')
            self.q_err()

    def q_12(self):
        func_name = 'q_12'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        if lexem_value == '*':
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_9 \twith\t{lexem_value}')
            self.q_9()

        elif lexem_value == ')':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_3 \twith\t{lexem_value}')
            self.r_3()

        elif lexem_value == '+':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_3 \twith\t{lexem_value}')
            self.r_3()

        elif lexem_value == '#':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_3 \twith\t{lexem_value}')
            self.r_3()

        elif lexem_value == '$':
            self.Debug(
                f'\tGo from\t{func_name} \tto\tr_3 \twith\t{lexem_value}')
            self.r_3()

        else:
            self.Debug(
                f'\tGo from\t{func_name} \tto\ts_err \twith\t{lexem_value}')
            self.q_err()

    def q_13(self):
        func_name = 'q_13'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.Debug(f'\tGo from\t{func_name} \tto\tr_5 \twith\t{lexem_value}')
        self.r_5()

    def q_14(self):
        func_name = 'q_14'
        self.Debug(f'this is {func_name}')
        self.index += 1
        lexem_type, lexem_value = self.getLexemData()

        self.Debug(f'\tGo from\t{func_name} \tto\ts_t \twith\t{lexem_value}')
        self.r_7()

    def q_err(self):
        func_name = 'q_err'
        self.Debug(f'this is {func_name}')
        raise IncorrectSyntax('Incorrect or unexpected lexem')

    def r_1(self):
        func_name = 'r_1'
        self.Debug(f'this is {func_name}')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-1]
        self.main_stack.append({'not_terminal': 'S'})
        self.main_stack += tmp
        self.Info('Reduce 1: S -> E$')
        self.Debug(f'\tGo\tfrom\t{func_name} \tto\ts_0')

        self.q_0()

    def r_2(self):
        func_name = 'r_2'
        self.Debug(f'this is {func_name}')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'E'})
        self.main_stack += tmp
        self.Debug(f'\tGo\tfrom\t{func_name} \tto\ts_0')
        new_res = self.stack[-2] + self.stack[-1]
        self.Info('Reduce 2: E -> E + T')
        self.Debug(
            f'\tCount:\t{self.stack[-2]} + {self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-2]
        self.stack.append(new_res)

        self.q_0()

    def r_3(self):
        func_name = 'r_3'
        self.Debug(f'this is {func_name}')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'E'})
        self.main_stack += tmp
        self.Debug(f'\tGo\tfrom\t{func_name} \tto\ts_0')
        new_res = self.stack[-2] - self.stack[-1]
        self.Info('Reduce 3: E -> E # T')
        self.Debug(
            f'\tCount:\t{self.stack[-2]} # {self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-2]
        self.stack.append(new_res)

        self.q_0()

    def r_4(self):
        func_name = 'r_4'
        self.Debug(f'this is {func_name}')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        self.main_stack[self.index] = {'not_terminal': 'E'}
        self.Info('Reduce 4: E -> T')
        self.Debug(f'\tGo\tfrom\t{func_name} \tto\ts_0')

        self.q_0()

    def r_5(self):
        func_name = 'r_5'
        self.Debug(f'this is {func_name}')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'T'})
        self.main_stack += tmp
        self.Debug(f'\tGo\tfrom\t{func_name} \tto\ts_0')
        new_res = self.stack[-2].dot(self.stack[-1])
        self.Info('Reduce 3: T -> T * F')
        self.Debug(
            f'\tCount:\t{self.stack[-2]} * {self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-2]
        self.stack.append(new_res)

        self.q_0()

    def r_6(self):
        func_name = 'r_6'
        self.Debug(f'this is {func_name}')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        self.main_stack[self.index] = {'not_terminal': 'T'}
        self.Info('Reduce 6: T -> F')
        self.Debug(f'\tGo\tfrom\t{func_name} \tto\ts_0')

        self.q_0()

    def r_7(self):
        func_name = 'r_7'
        self.Debug(f'this is {func_name}')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'F'})
        self.main_stack += tmp
        self.Info('Reduce 7: F -> (E)')
        self.Debug(f'\tGo\tfrom\t{func_name} \tto\ts_0')

        self.q_0()

    def r_8(self):
        func_name = 'r_8'
        self.Debug(f'this is {func_name}')
        self.index -= 1
        lexem_type, lexem_value = self.getLexemData()

        self.stack.append(lexem_value)
        self.main_stack[self.index] = {'not_terminal': 'F'}
        self.Info('Reduce 8: F -> num')
        self.Debug(f'\tGo\tfrom\t{func_name} \tto\ts_0')
        self.q_0()

    # def r_9(self):
    #     func_name = 'r_9'
    #     self.Debug(f'this is {func_name}')
    #     self.index -= 1
    #     lexem_type, lexem_value = self.getLexemData()

    #     self.stack.append(lexem_value)
    #     self.main_stack[self.index] = {'not_terminal': 'K'}
    #     self.Info('Reduce 9: K -> num')
    #     self.Debug(f'\tGo\tfrom\t{func_name} \tto\ts_0')

    #     self.q_0()


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
        variable_value = la2.lexicalAnalyzer(tmp[1])

        sa = SyntaxAnalyzer()
        variable_value = sa.syntaxAnalyzer(variable_value)

        if (variable_name is not None) and (variable_value is not None):
            res_variables[variable_name] = variable_value

    return res_variables


try:
    a = ['a=(2,0,2,2,0,0,2,0,2)']

    la1 = LexicalAnalyzer()
    variables = parseVariables(a)
    la1.setVariables(variables)
    stack = la1.lexicalAnalyzer(
        '(1,1,0,0,0,1,1,0,1+a)*1,0,0,0,0,0,0,0,1')
    print(stack)
    sa1 = SyntaxAnalyzer(loglevel='Info')
    sa1.syntaxAnalyzer(stack)
except IncorrectLexic as err:
    print(err.message)
except IncorrectSyntax as err:
    print(err.message)
except AnalyserError as err:
    print(err.message)
except ZeroDivisionError:
    print('Was zero-dividing')
