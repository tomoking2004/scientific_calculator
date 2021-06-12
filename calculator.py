# coding: utf-8
import operator
import math
from functions import *

TEST = False

class Operator:
    """自作演算子"""

    def __init__(self, name, func, type) -> None:
        """
        <type>
        0: const (pi, e)
        1: unary (x!)
        2: unary (absx, sinx)
        3: binary (xCy, x^y)
        4: binary (log{x,y})
        5: args (lcm{x,y,z})
        """
        self.name = name
        self.func = func
        self.type = type

    def __call__(self, *args) -> str:
        """関数を実行する"""
        if self.type in [0]:
            return str(self.func)
        if self.type in [1,2]:
            return str(self.func(args[0]))
        if self.type in [3,4]:
            return str(self.func(args[0], args[1]))
        if self.type in [5]:
            return str(self.func(args))


# オペレーターリスト
oprs = [
    Operator('+', operator.__add__, 3),
    Operator('-', operator.__sub__, 3),
    Operator('*', operator.__mul__, 3),
    Operator('/', operator.__truediv__, 3),
    Operator('//', operator.__floordiv__, 3),
    Operator('%', operator.__mod__, 3),
    Operator('**', operator.__pow__, 3),
    Operator('^', operator.pow, 3),
    Operator('exp', math.exp, 2),
    Operator('sqrt', math.sqrt, 2),
    Operator('abs', operator.__abs__, 2),
    Operator('sin', math.sin, 2),
    Operator('cos', math.cos, 2),
    Operator('tan', math.tan, 2),
    Operator('asin', math.asin, 2),
    Operator('acos', math.acos, 2),
    Operator('atan', math.atan, 2),
    Operator('log', log, 4),
    Operator('sum', sum, 5),
    Operator('prod', product, 5),
    Operator('lcm', lcm, 5),
    Operator('gcd', gcd, 5),
    Operator('P', permutation, 3),
    Operator('C', combination, 3),
    Operator('!', math.factorial, 1),
    Operator('pi', math.pi, 0),
    Operator('e', math.e, 0),
]

# オペレーター辞書
opr_dic = dict([(opr.name, opr) for opr in oprs])

# 演算優先度
priority = [['pi','e'],
            ['!'],
            ['exp','sqrt','abs','sin','cos','tan','asin','acos','atan','log','sum','prod','lcm','gcd','P','C'],
            ['**','^'],
            ['*','/','//','%'],
            ['+','-']]


def is_number(string: str) -> bool:
    """数字の真偽を返す"""
    try: 
        float(string)
        return True
    except:
        return False


def analysis_formula(formula: str) -> list:
    """文字列を解析してリストに変換する"""
    # 空白の除去
    f = formula.replace(' ', '')
    # 解析
    ls = []; i2 = 0
    for i in range(len(f)):
        if i<i2: continue
        # 意味の分割
        for j in range(len(f)):
            if j<i: continue
            if is_number(f[i:j+1]) and (f[i] not in '+-' or len(ls)==0 or ls[-1]=='('): #数字(先頭のみ符号を許可)
                i2 = j+1
            if f[i:j+1] in opr_dic or f[i:j+1] in '(){},': #演算子or括弧
                i2 = j+1
        if i==i2: raise Exception("'{}'という演算子は存在しません。".format(f[i]))
        # 演算子の補完
        s = f[i:i2]
        if s in '+-' and (len(ls)==0 or ls[-1]=='('): #符号付き非数字(先頭のみ符号を許可)
            ls += [s+'1', '*']
            continue
        if is_number(s) or s=='(' or s in opr_dic and opr_dic[s].type in [0,2,4,5]: #左に略表記可能
            if len(ls)!=0 and (is_number(ls[-1]) or ls[-1] in ')}' or
             ls[-1] in opr_dic and opr_dic[ls[-1]].type in [0,1]): #右に略表記可能
                ls.append('*')
        ls.append(s)
    return ls


def find_brackets(formula: list, b1='(', b2=')') -> tuple:
    """優先する次元の低い括弧のペアの位置を返す"""
    n = 0; i1 = -1; i2 = -1
    for i, c in enumerate(formula):
        if c in b1:
            if n==0: i1 = i
            n += 1
        if c in b2:
            n -= 1
            if n<=0: i2 = i; break
    if n!=0:
        raise Exception("括弧のペアが見つかりません。")
    return i1, i2


def find_operator(formula: list) -> int:
    """優先する演算子の位置を返す"""
    for p in priority:
        for i, s in enumerate(formula):
            if s in p: return i
    return -1


def brain(f: list) -> str:
    """演算装置"""

    # 括弧で分岐する
    while True:
        i1, i2 = find_brackets(f)
        if i1==-1 or i2==-1: break #分岐終了
        f = f[:i1] + [brain(f[i1+1:i2])] + f[i2+1:]
    if TEST: #途中式を出力
        print(f, end='')

    # 演算子で演算する
    while True:
        i = find_operator(f)
        if i==-1: break #演算終了
        opr = opr_dic[f[i]]
        if opr.type==0:
            f = f[:i] + [opr()] + f[i+1:]
        if opr.type==1:
            f = f[:i-1] + [opr(float(f[i-1]))] + f[i+1:]
        if opr.type==2:
            f = f[:i] + [opr(float(f[i+1]))] + f[i+2:]
        if opr.type==3:
            f = f[:i-1] + [opr(float(f[i-1]), float(f[i+1]))] + f[i+2:]
        if opr.type==4:
            f = f[:i] + [opr(float(f[i+2]), float(f[i+4]))] + f[i+6:]
        if opr.type==5:
            i1, i2 = find_brackets(f, b1='{', b2='}')
            args = [float(s) for s in f[i1+1:i2] if s!=',']
            f = f[:i] + [opr(*args)] + f[i2+1:]
    if len(f)!=1:
        raise Exception("演算子が不足しています。")
    if TEST: #途中式の答えを出力
        print(' = {}'.format(f[0]))
    
    return f[0]


def calculator(formula: str) -> str:
    """文字列関数電卓"""

    # 正規化する
    f = analysis_formula(formula)

    if TEST: #正規化された式を出力
        print('f = {}'.format(f))

    return brain(f)


if __name__ == "__main__":

    f = input()
    print(calculator(f))
