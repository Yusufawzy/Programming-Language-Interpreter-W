# Name: Yusuf Elnady
# W2 --https://www.radford.edu/~itec380/2020spring-ibarland/Homeworks/W2.html
# W4 --https://www.radford.edu/~itec380/2020spring-ibarland/Homeworks/W4.html
# Python 3.7 - PyCharm 2020.1 (Professional Edition)
from Scanner import *
from numbers import Number

'''
  Expr       ::= Num | Paren | BinOp | IfNeg | IfOdd | id |  LetExpr | FuncExpr | FuncApplyExpr
  Paren      ::= | Expr |
  BinOp      ::= # Expr Op Expr }
  Op         ::= order-up | ah-shrimp | barnacles  | fish-paste
  IfNeg      ::= sponge Expr bob Expr square Expr pants
  IfOdd      ::= ahoy Expr me Expr money Expr
  id         ::= String
  LetExpr    ::= sweet Id mother of Expr pearl Expr
  FuncExpr   ::= <^> Id * Expr                  interpretation: function-value; inspired by patrick star
  FuncApplyExpr ::= aye aye Expr captain Expr   interpretation: call the function (which is the captain of its argument)

 An Expr is:
  - a number
  - Paren  ([Expr])
  - Binop  ([Expr] [Op] [Expr])
  - IfNeg  ([Expr] [Expr] [Expr])
  - IfOdd  ([Expr] [Expr] [Expr])       #>>>W1
  - LetExpr([id] [Expr] [Expr])     #>>>W2
  - String                              #>>>W2 
  - FuncExpr([id] [Expr])
  - FuncApplyExpr ([Expr] [Expr])
'''

OP_FUNCS = {'order-up': lambda x, y: y + x, 'ah-shrimp': lambda x, y: x - y, 'barnacles!': lambda x, y: x * y,
            'fish-paste': lambda x, y: y * (x / y - x // y)}  # >>>W1

OPS = list(OP_FUNCS.keys())


# An Op is: (one-of OPS)

class Binop:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.op == other.op and self.right == other.right


class Paren:
    def __init__(self, e):
        self.e = e

    def __eq__(self, other):
        return self.e == other.e


class IfNeg:
    def __init__(self, test, then, els):
        self.test = test
        self.then = then
        self.els = els

    def __eq__(self, other):
        return self.test == other.test and self.then == other.then and self.els == other.els


# >>>W1
class IfOdd:
    def __init__(self, test, then, els):
        self.test = test
        self.then = then
        self.els = els

    def __eq__(self, other):
        return self.test == other.test and self.then == other.then and self.els == other.els


# >>>W2
class LetExpr:
    def __init__(self, id, rhs, body):
        self.id = id
        self.rhs = rhs
        self.body = body

    def __eq__(self, other):
        return self.id == other.id and self.rhs == other.rhs and self.body == other.body


# >>>W4
class FuncExpr:
    def __init__(self, param, body):
        self.param = param
        self.body = body

    def __eq__(self, other):
        return self.param == other.param and self.body == other.body


# >>>W4
class FuncApplyExpr:
    def __init__(self, arg, func):
        self.func = func
        self.arg = arg

    def __eq__(self, other):
        return self.func == other.func and self.arg == other.arg

    # (λ (x) (+ (* 3 x) 1)) written in W4: (^) x * ##x barnacles! 3} order-up 1}.


'''
Examples of Expr:
- 34
- Paren(34)
- Binop(3,"order-up",4)
- Binop(Paren(34),"order-up",Binop(3,"barnacles!",4))
- IfNeg(3,7,9)
- IfNeg(Paren(1),Binop(Paren(34),"order-up",Binop(3,"barnacles!",4)), IfNeg(0,7,9))
- IfOdd(22,IfOdd(3,1,2),IfOdd(100.3,9,44))
- IfOdd(3,1,Binop(3,"fish-paste",2))
- "x"
- "AnId0"
- "RESULT"
- LetExpr("x",5,Binop("x", "ah-shrimp" ,3))
- LetExpr("x",Binop(Binop(Paren(7),"order-up",8), "barnacles" ,3),Binop("x", "ah-shrimp" ,3))
'''


# exprToString : Expr -> string
# Return a string-representation of `e`.
def exprToString(e):
    if isinstance(e, Number):
        return str(e)
    elif isinstance(e, Paren):
        return "|" + exprToString(e.e) + "|"
    elif isinstance(e, Binop):
        return "#" + exprToString(e.left) + " " + e.op + " " + exprToString(e.right) + "}"
    elif isinstance(e, IfNeg):
        return "sponge " + exprToString(e.test) + " bob " + exprToString(e.then) + " square " + exprToString(
            e.els) + " pants"
    elif isinstance(e, IfOdd):  # >>>W1
        return "ahoy " + exprToString(e.test) + " me " + exprToString(e.then) + " money " + exprToString(e.els)
    elif isinstance(e, LetExpr):  # >>>W2
        return "sweet " + exprToString(e.id) + " mother of " + exprToString(e.rhs) + " pearl " + exprToString(e.body)
    elif isinstance(e, FuncExpr):  # >>>W4
        return "(^) " + exprToString(e.param) + " * " + exprToString(e.body)
    elif isinstance(e, FuncApplyExpr):  # >>>W4
        return "aye aye " + exprToString(e.arg) + " captain " + exprToString(e.func)
    elif isinstance(e, str):  # id # >>>W1
        return e
    else:
        raise TypeError('eval "unknown type of expr: ' + str(e))


# stringToExpr : string -> Expr
# given a string, return the parse-tree for this string `prog`
def stringToExpr(prog):
    return parse(Scanner(prog))


# parse : scanner -> Expr
# given a scanner, consume one W2 expression off the front of it
# returns the corresponding parse-tree.
def parse(s):
    # Recursive-descent parsing:
    if isinstance(peekHelper(s, False), Number):
        return pop(s)
    elif peek(s) == "|":
        _ = pop(s)
        the_inside_expr = parse(s)
        _ = pop(s)
        return Paren(the_inside_expr)
    elif peek(s) == "#":
        _ = pop(s)
        left = parse(s)
        op = pop(s)
        if op not in OPS:
            raise TypeError("parse --> Unknown op " + op)
        right = parse(s)
        _ = pop(s)
        return Binop(left, op, right)
    elif peek(s) == "sponge":
        _ = pop(s)
        test = parse(s)
        _ = pop(s)
        then = parse(s)
        _ = pop(s)
        els = parse(s)
        _ = pop(s)
        return IfNeg(test, then, els)
    elif peek(s) == "ahoy":  # >>>W1
        _ = pop(s)
        test = parse(s)
        _ = pop(s)
        then = parse(s)
        _ = pop(s)
        els = parse(s)
        return IfOdd(test, then, els)
    elif peek(s) == "sweet":  # >>>W2
        _ = pop(s)
        id = pop(s)
        _ = pop(s)
        _ = pop(s)
        rhs = parse(s)
        _ = pop(s)
        body = parse(s)
        return LetExpr(id, rhs, body)
    elif peek(s) == "(":  # >>>W4
        _ = pop(s)
        _ = pop(s)
        _ = pop(s)
        param = pop(s)
        _ = pop(s)
        body = parse(s)
        return FuncExpr(param, body)
    elif peek(s) == "aye":  # >>>W4
        _ = pop(s)
        _ = pop(s)
        arg = parse(s)
        _ = pop(s)
        func = parse(s)
        return FuncApplyExpr(arg, func)
    elif isinstance(peek(s), str):  # id #>>>W2
        return pop(s)
    else:
        raise TypeError("parse (format syntax error -- something has gone awry!, Encountered" + peek(s))


# eval : Expr -> Number
# Return the value which this Expr evaluates to.
def eval(e):
    if isinstance(e, Number):
        return e
    elif isinstance(e, Paren):
        return eval(e.e)
    elif isinstance(e, Binop):
        return evalBinOP(e.op, eval(e.left), eval(e.right))
    elif isinstance(e, IfNeg):
        return eval(e.then) if (eval(e.test) < 0) else eval(e.els)
    elif isinstance(e, IfOdd):  # >>>W1
        return eval(e.then) if (isinstance(eval(e.test), int) and eval(e.test) % 2 != 0) else eval(e.els)
    elif isinstance(e, LetExpr):  # >>>W2
        v0 = eval(e.rhs)
        e1 = substitute(v0, e.id, e.body)
        return eval(e1)
    elif isinstance(e, FuncExpr):  # >>>W4
        return e
    elif isinstance(e, FuncApplyExpr):  # >>>W4
        actualArg = eval(e.arg)
        functionValue = eval(e.func)
        e1 = substitute(actualArg, functionValue.param, functionValue.body)
        return eval(e1)
    else:
        raise TypeError('eval "unknown type of expr: ' + str(e))


# evalBinOP : op Number Number -> Number
# Evaluate the result of BinOp Expr, the binary operators.
def evalBinOP(op, left, right):
    if OP_FUNCS.get(op) is not None:
        return OP_FUNCS.get(op)(left, right)
    else:
        raise TypeError("evalBinOP --> Unimplemented op " + op + "; must be one of: " + str(OPS))


# substitute-> Number, id, Expr -> Expr
# return the tree `e` with any free occurrences of `idd` replaced with `v0`.
def substitute(v0, idd, e):  # >>>W2
    if isinstance(e, Number):
        return e
    elif isinstance(e, Paren):
        return Paren(substitute(v0, idd, e.e))
    elif isinstance(e, Binop):
        return Binop(substitute(v0, idd, e.left), e.op, substitute(v0, idd, e.right))
    elif isinstance(e, IfNeg):
        return IfNeg(substitute(v0, idd, e.test), substitute(v0, idd, e.then), substitute(v0, idd, e.els))
    elif isinstance(e, IfOdd):  # >>>W1
        return IfOdd(substitute(v0, idd, e.test), substitute(v0, idd, e.then), substitute(v0, idd, e.els))
    elif isinstance(e, str):  # >>>W2
        return v0 if idd == e else e
    elif isinstance(e, LetExpr):  # >>>W2
        return LetExpr(e.id, substitute(v0, idd, e.rhs),
                       e.body if (e.id == idd) else substitute(v0, idd, e.body))  # >>>W3
    elif isinstance(e, FuncExpr):  # >>>W4
        return FuncExpr(e.param, e.body if idd == e.param else substitute(v0, idd, e.body))
    elif isinstance(e, FuncApplyExpr):  # >>>W4
        return FuncApplyExpr(substitute(v0, idd, e.arg), substitute(v0, idd, e.func))
    else:
        raise TypeError('eval "unknown type of expr: ' + str(e))

# exprToString : Expr -> string
# stringToExpr : string -> Expr
# parse : scanner -> Expr
# eval : Expr -> Num
# substitute-> Number, id, Expr -> Expr


# idd = Scanner("hi23.4!blaha#b|c!d-e")
'''
while idd.data : 
    print(pop(idd)) 
'''

s2 =  "aye aye 3 captain sweet makeAdder           mother of  (^) n *   (^) m * # n order-up m }             pearl aye aye 4 captain makeAdder   "
s = "sweet      tripleAndInc mother of  (^) x * ##x barnacles! y} order-up 1} pearl      aye aye 5 captain tripleAndInc"

