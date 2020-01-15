import datetime
import os.path
import logging
import inspect

filename = '.'.join(os.path.basename(__file__).split('.')[:-1])
logging.basicConfig(filename=f'{filename}.log',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(message)s')


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


def laDecorator(func):
    def wrapper(self, *argv, **kwargv):

        if self.symbol != '':
            logging.info(
                f'\tGo from {inspect.stack()[1][3]}\tto\t{func.__name__} \twith:\t{self.symbol}')

        # logging.info(f'\tThis is {func.__name__}')
        self.getch()

        return func(self, *argv, **kwargv)
    return wrapper


def saWalk(func):
    def wrapper(self):

        logging.debug(
            f'\t\tGo from {inspect.stack()[1][3]}\tto\t{func.__name__} \twith "{self.lexem_value}"\n')

        logging.debug(f'\tThis is {func.__name__}')
        logging.debug(f'\t\tStack:\t{self.getLexemValues()}')
        self.index += 1
        self.lexem_type, self.lexem_value = self.getLexemData()

        func(self)
    return wrapper


def saReduce(func):
    def wrapper(self):

        reduce_number = (func.__name__).split('_')[1]
        logging.debug(
            f'\t\tGo from {inspect.stack()[1][3]}\tto\t{func.__name__} \twith "{self.lexem_value}"\n')

        logging.debug(f'\tThis is {func.__name__}')
        self.index -= 1
        self.lexem_type, self.lexem_value = self.getLexemData()
        logging.debug(
            f'\t\tGo\tfrom\t{func.__name__} \tto\ts_0 \tpack {reduce_number}:\t"{func.__doc__}"\n')

        func(self)
    return wrapper


class LexicalAnalyzer():

    def __init__(self):
        self.index = 0
        self.symbol = ''
        self.input_string = ''
        self.lexems = []
        self.buff = ''
        self.math_symbols = '+*-() '
        self.variables = {}

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
        logging.info(
            f'Lexical analyzer started at [{datetime.datetime.now()}]')
        self.input_string = s_input
        self.q_0()
        self.lexems.append({'not_terminal': '$'})
        logging.info(f'\n\t{self.lexems}\n')
        return self.lexems

    def getch(self):
        try:
            self.symbol = self.input_string[self.index]
            self.index += 1
        except:
            self.symbol = None

    @laDecorator
    def q_0(self):

        if not self.symbol:
            return False

        elif self.symbol in self.math_symbols:
            self.buff += self.symbol
            self.index += 1
            return self.q_res({'operation': self.symbol})

        elif self.symbol.isdigit():
            self.buff += self.symbol
            return self.q_2()

        else:
            return self.q_err()

    @laDecorator
    def q_2(self):
        if not self.symbol:
            self.index += 1
            return self.q_res({'number': int(self.buff)})

        if self.symbol.isdigit():
            self.buff += self.symbol
            return self.q_2()

        elif self.symbol in self.math_symbols:
            return self.q_res({'number': int(self.buff)})

        else:
            return self.q_err()

    def q_err(self):
        logging.info('Error: Incorrect input string')
        raise IncorrectLexic('Incorrect input string')

    def q_res(self, lexem):
        logging.info(f'\tPushing: {lexem}')
        self.lexems.append(lexem)
        self.index -= 1
        self.buff = ''
        self.symbol = ''
        return self.q_0()


class SyntaxAnalyzer():
    def __init__(self):
        self.index = 0
        self.stack = []
        self.msg = ''

    def getLexemData(self):
        try:
            lexem = self.main_stack[self.index]
            self.lexem_type = list(lexem)[0]
            self.lexem_value = lexem[self.lexem_type]
        except:
            self.lexem_type = ''
            self.lexem_value = None
        return (self.lexem_type, self.lexem_value)

    def getLexemValues(self):
        res = []
        for lexem in self.main_stack:
            res.append(str(lexem[list(lexem)[0]]))
        return ' '.join(res)

    def syntaxAnalyzer(self, main_stack):
        logging.info(
            f'Syntax analyzer started at [{datetime.datetime.now()}]')
        self.main_stack = main_stack
        self.q_0()
        res = self.stack[0]

        logging.info(f'Result: {res}')
        return res

    def q_0(self):
        logging.debug('\tThis is q_0')
        logging.info(f'\t\tStack:\t{self.getLexemValues()}')
        self.index = 0
        self.lexem_type, self.lexem_value = self.getLexemData()

        if self.lexem_value == 'S':
            logging.info('Finish!')
            return

        if self.lexem_value == '(':
            self.q_4()
        elif self.lexem_value == 'E':
            self.q_1()
        elif self.lexem_value == 'T':
            self.q_2()
        elif self.lexem_value == 'F':
            self.q_3()
        elif self.lexem_type == 'number':
            self.q_5()
        else:
            self.q_err()

    @saWalk
    def q_1(self):
        if self.lexem_value == '+':
            self.q_7()
        elif self.lexem_value == '-':
            self.q_8()
        elif self.lexem_value == '$':
            self.q_6()
        else:
            self.q_err()

    @saWalk
    def q_2(self):
        if self.lexem_value == '*':
            self.q_9()
        elif self.lexem_value == ')':
            self.r_4()
        elif self.lexem_value == '+':
            self.r_4()
        elif self.lexem_value == '-':
            self.r_4()
        elif self.lexem_value == '$':
            self.r_4()
        else:
            self.q_err()

    @saWalk
    def q_3(self):
        self.r_6()

    @saWalk
    def q_4(self):
        if self.lexem_value == '(':
            self.q_4()
        elif self.lexem_value == 'E':
            self.q_10()
        elif self.lexem_value == 'T':
            self.q_2()
        elif self.lexem_value == 'F':
            self.q_3()
        elif self.lexem_type == 'number':
            self.q_5()
        else:
            self.q_err()

    @saWalk
    def q_5(self):
        self.r_8()

    @saWalk
    def q_6(self):
        self.r_1()

    @saWalk
    def q_7(self):
        if self.lexem_value == '(':
            self.q_4()
        elif self.lexem_value == 'T':
            self.q_11()
        elif self.lexem_value == 'F':
            self.q_3()
        elif self.lexem_type == 'number':
            self.q_5()
        else:
            self.q_err()

    @saWalk
    def q_8(self):
        if self.lexem_value == '(':
            self.q_4()
        elif self.lexem_value == 'T':
            self.q_12()
        elif self.lexem_value == 'F':
            self.q_3()
        elif self.lexem_type == 'number':
            self.q_5()
        else:
            self.q_err()

    @saWalk
    def q_9(self):
        if self.lexem_value == '(':
            self.q_4()
        elif self.lexem_value == 'F':
            self.q_13()
        elif self.lexem_type == 'number':
            self.q_5()
        else:
            self.q_err()

    @saWalk
    def q_10(self):
        if self.lexem_value == ')':
            self.q_14()
        elif self.lexem_value == '+':
            self.q_7()
        elif self.lexem_value == '-':
            self.q_8()
        else:
            self.q_err()

    @saWalk
    def q_11(self):
        if self.lexem_value == '*':
            self.q_9()
        elif self.lexem_value == ')':
            self.r_2()
        elif self.lexem_value == '+':
            self.r_2()
        elif self.lexem_value == '-':
            self.r_2()
        elif self.lexem_value == '$':
            self.r_2()
        else:
            self.q_err()

    @saWalk
    def q_12(self):
        if self.lexem_value == '*':
            self.q_9()
        elif self.lexem_value == ')':
            self.r_3()
        elif self.lexem_value == '+':
            self.r_3()
        elif self.lexem_value == '-':
            self.r_3()
        elif self.lexem_value == '$':
            self.r_3()
        else:
            self.q_err()

    @saWalk
    def q_13(self):
        self.r_5()

    @saWalk
    def q_14(self):
        self.r_7()

    def q_err(self):
        logging.debug(
            f'\t\tGo from {inspect.stack()[1][3]}\tto\tq_err \twith "{self.lexem_value}"\n')
        logging.debug('This is q_err')
        raise IncorrectSyntax('Incorrect or unexpected lexem')

    @saReduce
    def r_1(self):
        '''S -> E$'''

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-1]
        self.main_stack.append({'not_terminal': 'S'})
        self.main_stack += tmp
        logging.info('\tReduce 1: S -> E$')
        logging.debug('')
        self.q_0()

    @saReduce
    def r_2(self):
        '''E -> E + T'''

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'E'})
        self.main_stack += tmp
        new_res = sum(self.stack[-2], self.stack[-1])
        logging.info('\tReduce 2: E -> E + T')
        logging.debug('')
        logging.debug(
            f'\tCount:\t{self.stack[-2]} + {self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-2]
        self.stack.append(new_res)

        self.q_0()

    @saReduce
    def r_3(self):
        '''E -> E - T'''

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'E'})
        self.main_stack += tmp
        new_res = sub(self.stack[-2], self.stack[-1])
        logging.info('\tReduce 3: E -> E - T')
        logging.debug('')
        logging.debug(
            f'\tCount:\t{self.stack[-2]} - {self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-2]
        self.stack.append(new_res)

        self.q_0()

    @saReduce
    def r_4(self):
        '''E -> T'''

        self.main_stack[self.index] = {'not_terminal': 'E'}
        logging.info('\tReduce 4: E -> T')

        self.q_0()

    @saReduce
    def r_5(self):
        '''T -> T * F'''

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'T'})
        self.main_stack += tmp
        new_res = mul(self.stack[-2], self.stack[-1])
        logging.info('\tReduce 3: T -> T * F')
        logging.debug('')
        logging.debug(
            f'\tCount:\t{self.stack[-2]} * {self.stack[-1]} = {new_res}')
        self.stack = self.stack[:-2]
        self.stack.append(new_res)

        self.q_0()

    @saReduce
    def r_6(self):
        '''T -> F'''

        self.main_stack[self.index] = {'not_terminal': 'T'}
        logging.info('\tReduce 6: T -> F')
        logging.debug('')
        self.q_0()

    @saReduce
    def r_7(self):
        '''F -> (E)'''

        tmp = self.main_stack[self.index+1:]
        self.main_stack = self.main_stack[:self.index-2]
        self.main_stack.append({'not_terminal': 'F'})
        self.main_stack += tmp
        logging.info('\tReduce 7: F -> (E)')
        logging.debug('')
        self.q_0()

    @saReduce
    def r_8(self):
        '''F -> num'''

        self.stack.append(self.lexem_value)
        self.main_stack[self.index] = {'not_terminal': 'F'}
        logging.info('\tReduce 8: F -> num')
        logging.debug('')
        self.q_0()


def sum(value1, value2):
    result = 0
    i=0
    while (value1>0) or (value2>0):
        v1 = value1 % 10
        value1 = int(value1 / 10)
        v2 = value2 % 10
        value2 = int(value2 / 10)
        res = (v1+v2)%10
        result += 10**i*res
        i+=1
    result+=value1*10**i
    result+=value2*10**i
    return result

def mul(value1, value2):
    result = 0
    i=0
    while (value1>0) or (value2>0):
        v1 = value1 % 10
        value1 = int(value1 / 10)
        v2 = value2 % 10
        value2 = int(value2 / 10)
        res = (v1*v2)%10
        result += 10**i*res
        i+=1
    result+=value1*10**i
    result+=value2*10**i
    return result

def sub(value1, value2):
    result = 0
    i=0
    while (value1>0) or (value2>0):
        v1 = value1 % 10
        value1 = int(value1 / 10)
        v2 = value2 % 10
        value2 = int(value2 / 10)
        res = v1-v2
        if res<0:
            res = 10 + res
        result += 10**i*res
        i+=1
    result+=value1*10**i
    result+=value2*10**i
    return result

try:
    la = LexicalAnalyzer()

    # examples:

    stack = la.lexicalAnalyzer('4*4') # 6
    # stack = la1.lexicalAnalyzer('13*13') # 19
    # stack = la1.lexicalAnalyzer('3*13') # 9
    # stack = la1.lexicalAnalyzer('3*3') # 9

    # stack = la1.lexicalAnalyzer('9+1') # 0
    # stack = la1.lexicalAnalyzer('10+2') # 12
    # stack = la1.lexicalAnalyzer('3+3') # 6
    # stack = la1.lexicalAnalyzer('9+8') # 7

    # stack = la1.lexicalAnalyzer('5-3') # 2
    # stack = la1.lexicalAnalyzer('4-6') # 8
    # stack = la1.lexicalAnalyzer('15-3') # 12
    # stack = la1.lexicalAnalyzer('5-13') # 92

    print(stack)
    sa = SyntaxAnalyzer()
    print(sa.syntaxAnalyzer(stack))
except IncorrectLexic as err:
    print(err.message)
except IncorrectSyntax as err:
    print(err.message)
except AnalyserError as err:
    print(err.message)
except ZeroDivisionError:
    print('Was zero-dividing')
