from antlr4 import *
from gLexer import gLexer
from gParser import gParser
from gVisitor import gVisitor
import numpy as np

class ExecVisitor(gVisitor):
    def __init__(self):
        self.vars = {}

    # ROOT: recorre totes les stat, retorna una llista de valors
    def visitRoot(self, ctx: gParser.RootContext):
        results = []
        for stmt in ctx.stat():
            results.append(self.visit(stmt))
        return results

    # Assignació: guarda la variable i retorna el valor
    def visitAssignacio(self, ctx: gParser.AssignacioContext):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.vars[name] = value
        return value

    # Expressió com a sentència: avaluem i imprimim
    def visitExpressio(self, ctx: gParser.ExpressioContext):
        value = self.visit(ctx.expr())
        print(self.formatResult(value))
        return value

    def formatResult(self, value):
        if isinstance(value, np.ndarray):
            return ' '.join(self.formatResult(x) for x in value)
        if isinstance(value, int):
            return f"_{abs(value)}" if value < 0 else str(value)
        return str(value)

    # Expressió binària dreta
    def visitOperacio(self, ctx: gParser.OperacioContext):
        left = self.visit(ctx.atom())
        if ctx.op() is None:
            return left
        op = ctx.op().getText()
        right = self.visit(ctx.expr())
        
        # Case 1: Both scalars
        if not isinstance(left, np.ndarray) and not isinstance(right, np.ndarray):
            if op == '+':      return left + right
            elif op == '-':    return left - right
            elif op == '*':    return left * right
            elif op == '%':    return int(left / right)
            elif op == '|':    return right % left
            elif op == '^':    return left ** right
            else: raise Exception(f"Operador no reconegut: {op}")
        
        # Case 2: One scalar, one list
        if isinstance(left, np.ndarray) and not isinstance(right, np.ndarray):
            if op == '+':      return left + right
            elif op == '-':    return left - right
            elif op == '*':    return left * right
            elif op == '%':    return left / right
            elif op == '|':    return right % left  # Note: J's | is residue (right % left)
            elif op == '^':    return left ** right
            else: raise Exception(f"Operador no reconegut: {op}")
        if not isinstance(left, np.ndarray) and isinstance(right, np.ndarray):
            if op == '+':      return left + right
            elif op == '-':    return left - right
            elif op == '*':    return left * right
            elif op == '%':    return int(left / right)
            elif op == '|':    return right % left
            elif op == '^':    return left ** right
            else: raise Exception(f"Operador no reconegut: {op}")
        
        # Case 3: Both lists
        if isinstance(left, np.ndarray) and isinstance(right, np.ndarray):
            if len(left) != len(right):
                raise Exception("length error")
            if op == '+':      return left + right
            elif op == '-':    return left - right
            elif op == '*':    return left * right
            elif op == '%':    return left / right
            elif op == '|':    return right % left
            elif op == '^':    return left ** right
            else: raise Exception(f"Operador no reconegut: {op}")

    def visitLlista(self, ctx: gParser.LlistaContext):
        nums = []
        for child in ctx.getChildren():
            if child.getSymbol().type == gParser.NUM:
                nums.append(self.parseNum(child.getText()))
        return np.array(nums)

    def parseNum(self, text):
        if text[0] == '_':
            return -int(text[1:])
        return int(text)

    #def visitNumero(self, ctx: gParser.NumeroContext):
        #return self.parseNum(ctx.NUM().getText())

    def visitVariable(self, ctx: gParser.VariableContext):
        name = ctx.ID().getText()
        if name in self.vars:
            return self.vars[name]
        else:
            raise Exception(f"Variable no definida: {name}")

    def visitParenExpr(self, ctx: gParser.ParenExprContext):
        return self.visit(ctx.expr())

    # (de moment no suportem funcions)
    def visitCridaFuncio(self, ctx):
        raise Exception("Les funcions no estan implementades encara.")

if __name__ == '__main__':
    import sys
    data = open(sys.argv[1], encoding='utf-8').read() if len(sys.argv)>1 else sys.stdin.read()

    input_stream = InputStream(data)
    lexer = gLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = gParser(tokens)
    tree = parser.root()

    executor = ExecVisitor()
    executor.visit(tree)
