
import random
import math
from fractions import Fraction
import  os

from SuffixExpression import SuffixExpression

from BinaryTree  import BinaryTree



class Product:

    # 类变量定义
    problemArray = []            # 表达式列表表示
    exStr = ''            # 表达式字符串
    answer = 0                   # 答案
    answerStr = ''              # 答案字符串
    operRange = 10                # 操作数范围
    operCount = 3                 # 操作符个数
    expressionNum = 100                  #生成表达式的数目



    def __init__(self, operRange,expressionNum):           #类的构造函数
        self.operRange = operRange
        self.operCount = 3
        self.expressionNum = expressionNum
        self.problemArray = self.creQuestion()
        self.normalizeExpression(self.problemArray)



    def creQuestion(self):
        """
        表达式生成主函数
        """
        expNum = self.expressionNum
        expressionList = []
        i = 0

        while i < expNum:
            random_num_operation = random.randint(1,self.operCount)  #运算符的数目
            is_need_parenteses = random.randint(0, 1)    #是否需要加括号
            number_of_oprand = random_num_operation + 1  # 操作数比操作符的数目多1
            exp = []
            for j in range(random_num_operation + number_of_oprand):

                if j % 2 == 0:
                    # 随机生成操作数(含分数）
                    exp.append(self.getOperNum())


                    if j > 1 and exp[j - 1] == '÷' and exp[j] == '0':
                        while True:
                            exp[j - 1] = self.generateOperation()
                            if exp[j - 1] == '÷':
                                continue
                            else:
                                break
                else:
                    # 生成运算符
                    exp.append(self.generateOperation())

                if j > 3:
                    if exp[j-2] == '÷' :  #为了子表达式为真分数，÷左右又括号除外
                        if exp[j-1] > exp[j-3]:
                            t  = exp[j-1]
                            exp[j - 1] =  exp[j-3]
                            exp[j - 3] = t


                    elif exp[j-2] == '-' :
                        if exp[j-1] < exp[j-3]:
                            t  = exp[j-1]
                            exp[j - 1] =  exp[j-3]
                            exp[j - 3] = t




            # 判断是否要括号
            if is_need_parenteses and number_of_oprand != 2:
                expression = " ".join(self.generateParentheses(exp, number_of_oprand))
            else:
                expression = " ".join(exp)

            #判断是否有重复

            if self.expressionNum <= 500:
                if self.isRepeat(expressionList, expression) :
                   continue
                else:
                    result = self.calculate(expression)
                    if result == "False" :
                        pass
                    else:

                        expressionList.append(expression)
                        i = i + 1
            else:
                result = self.calculate(expression)
                if result == "False":
                    pass
                else:

                    expressionList.append(expression)
                    i = i + 1



        return expressionList

    def generateOperation(self):  #随机生成操作符
        operators = ['+', '-', '×', '÷']
        return operators[random.randint(0,len(operators) - 1)]



    def generateParentheses(self, exp, number_of_oprand):
        """
        生成括号表达式
        :param
            exp: 表达式
            number_of_oprand: 运算符数目
        :return: 括号表达式
        """
        expression = []
        num = number_of_oprand
        if exp:
            exp_length = len(exp)
            left_position = random.randint(0, int(num / 2))
            right_position = random.randint(left_position + 1, int(num / 2) + 1)
            mark = -1
            for i in range(exp_length):
                if exp[i] in ['+', '-', '×', '÷']:
                    expression.append(exp[i])
                else:
                    mark += 1
                    if mark == left_position:
                        expression.append('(')
                        expression.append(exp[i])
                    elif mark == right_position:
                        expression.append(exp[i])
                        expression.append(')')
                    else:
                        expression.append(exp[i])
        # 如果生成的括号表达式形如 (1 + 2 + 3) 则重新生成
        if expression[0] == '(' and expression[-1] == ')':
            expression = self.generateParentheses(exp, number_of_oprand)
            return expression
        return expression


    def getOperNum(self):
        # 随机生成操作数
        int_operands = [random.randint(1, self.operRange) for num in range(self.operCount + 1)]  # 随机生成操作数个数个整数
        int_operands = [str(num) for num in int_operands]  # 都统一成字符类型
        frc_operands = [self.generate_fraction(self.operRange) for num in
                        range(self.operCount + 1)]  # 随机生成操作数个数个分数
        operands = int_operands + frc_operands
        random.shuffle(operands)
        mark = random.randint(1, 30000)
        if mark in range(1, 10000):
            operands_list = operands
            result = random.choice(operands_list)
        elif mark in range(10001, 20000):
            operands_list = int_operands
            result = random.choice(operands_list)
        else:
            operands_list = frc_operands
            result = random.choice(operands_list)
        return str(result)  # 进一步确保返回字符型


    def generate_fraction(self, operRange): #生成的分数式带分数还是真分数
        if random.choice([True, False]):    #生成带分数
            whole_part = random.randint(1, self.operRange-1)
            denominator = random.randint(2, self.operRange)
            numerator = random.randint(1, denominator-1)
            fraction = f"{whole_part}'{numerator}/{denominator}"
        else:   #生成真分数
            denominator = random.randint(2, self.operRange)
            numerator = random.randint(1, denominator - 1)
            fraction = f"{numerator}/{denominator}"
        return fraction

    def DecToStr(self,operArray):
       #分数转化为字符串  带分数
        operNum1 = operArray[0]
        operNum2 = operArray[1]
        if operNum2 == 1:
            return operNum1
        if(operNum1 > operNum2):
            temp = int(operNum1/operNum2)
            operNum1 -= (temp*operNum2)
            return str(temp) + "'" + str(operNum1) + "/" + str(operNum2)
        else:
            return str(operNum1) + "/" + str(operNum2)

    def getRangeDec(self):                     #随机生成分数
        operRange=self.operRange
        while True:
            # 随机生成两个随机数
            operNum1 = self.getRandomNum(operRange)
            operNum2 = self.getRandomNum(operRange)
            # 判断operNum1是否为operNum2的倍数，若是则重新生成随机数
            if (operNum1%operNum2) == 0:
                continue
            # 若operNum1不是operNum2的倍数则已获取到符合要求的 operNum1和 operNum2，退出循环
            else:
                break
        # 将获取到的分子和分母进行化简并返回
        return self.stacdardDec(operNum1, operNum2)

    def stacdardDec(self,operNum1,operNum2):     # 化简分数  接收分子 分母参数
        num  = Fraction(operNum1, operNum2)
        Num1  = int(num.numerator)
        Num2  = int(num.denominator)
        return [Num1,Num2]

    def getFactorList(self, oper):   #获取正整数的公因子包括其本身
        l=[]
        for k in range(2, oper+1):
            if (oper % k) == 0:
                l.append(k)
        return l

    def getRandomNum(self, range):
        #获取随机数

        return random.randint(1, range)

    def getOperSymbol(self, operate):
        # 返回操作符符号
        operSignArray = ['+', '-', '×', '÷']  #对应operate 1，2，3，4
        return operSignArray[operate - 1]




    def normalizeExpression(self, exp_list):
        """
        规范化输出表达式
        :param exp_list: 表达式列表
        :return
        """
        if not exp_list:
            return

        if  os.path.exists("Exercises.txt"):
            with open("Exercises.txt", 'r+') as file:
                file.truncate(0)

        for i, exp in enumerate(exp_list):
            exp_str = "Question"+str(i+1) + ': '+ exp+" ="+"\n"
            with open('Exercises.txt', "a+",encoding='utf-8') as f:
                f.write(exp_str)



    def isRepeat(self, express_set, expression):
        """
        判断重复方法
        :param
            express_set: 表达式集合
            expression: 生成的表达式
        :return: True or False
        """
        suffixExpression = SuffixExpression(expression)
        target_exp_suffix = suffixExpression.re   # 后缀表达式列表
        binaryTree = BinaryTree()
        target_exp_binary_tree = binaryTree.generateBinaryTree(target_exp_suffix)
        for item in express_set:
            suffixExpression2 = SuffixExpression(item)
            source_exp_suffix = suffixExpression2.re
            source_exp_binary_tree = binaryTree.generateBinaryTree(source_exp_suffix)
            if binaryTree.treeIsSame(target_exp_binary_tree) == binaryTree.treeIsSame(source_exp_binary_tree):
                return True
        return False

    def calculate(self,expression):  # 计算单一表达式的值

        suffixExpression  = SuffixExpression(expression)
        exp_value = str(suffixExpression.suffixToValue())
        result = exp_value

        return result