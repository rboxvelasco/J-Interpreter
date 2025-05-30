from antlr4 import *
from gLexer import gLexer
from gParser import gParser
from gVisitor import gVisitor

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
        if isinstance(value, int): #or isinstance(value, float):
            return f"_{abs(value)}" if value < 0 else str(value)
        return str(value)


    # Expressió binària dreta
    def visitOperacio(self, ctx: gParser.OperacioContext):
        left = self.visit(ctx.atom())
        if ctx.op() is not None:
            op = ctx.op().getText()
            right = self.visit(ctx.expr())
            if op == '+':      return left + right
            elif op == '-':    return left - right
            elif op == '*':    return left * right
            elif op == '%':    return left / right    # divisió real
            elif op == '|':    return right % left    # modul invertit
            elif op == '^':    return left ** right
            else: raise Exception(f"Operador no reconegut: {op}")
        else:
            return left

    def visitNumero(self, ctx: gParser.NumeroContext):
        text = ctx.NUM().getText()
        if text[0] == '_':
            return - int(text[1:])
        else:
            return int(text)

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
