import sys
import numpy as np

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
        
        # If the value is an operator, store it as a function
        if isinstance(value, str) and value in {'+', '-', '*', '%', '|', '^'}:
            self.vars[name] = ('function', value)
        else:
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
        else:
            return f"_{abs(value)}" if value < 0 else str(value)
        return str(value)

    # Expressió binària dreta
    def visitOperacio(self, ctx: gParser.OperacioContext):
        # Collect all atoms and operators
        atoms = [self.visit(atom) for atom in ctx.atom()]
        ops = [op.getText() for op in ctx.op()]
        
        # If no operators, return the single atom
        if not ops:
            return atoms[0]
        
        # Evaluate right-to-left
        result = atoms[-1]
        for i in range(len(ops) - 1, -1, -1):
            left = atoms[i]
            right = result
            op = ops[i]
            
            # Ensure operands are arrays
            left = np.atleast_1d(left)
            right = np.atleast_1d(right)
            
            # Handle array shapes for non-concatenation and non-indexing operations
            if op not in {',', '{'} and left.shape != right.shape:
                if left.shape == (1,):
                    left = np.repeat(left, len(right))
                elif right.shape == (1,):
                    right = np.repeat(right, len(left))
                else:
                    raise Exception("length error")
            
            # Apply operation
            if op == '+':      result = left + right
            elif op == '-':    result = left - right
            elif op == '*':    result = left * right
            elif op == '%':    result = left // right
            elif op == '|':    result = right % left
            elif op == '^':    result = left ** right
            elif op == ',':    result = np.concatenate((left, right))
            elif op == '{':
                # Ensure right is a 1D array
                if right.ndim != 1:
                    raise Exception("Indexing target must be a 1D array")
                # Ensure left contains valid indices
                if not np.all((left >= 0) & (left < len(right))):
                    raise Exception("Index out of bounds")
                result = right[left.astype(int)]
            else: raise Exception(f"Operador no reconegut: {op}")
        
        return result

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

    def visitVariable(self, ctx: gParser.VariableContext):
        name = ctx.ID().getText()
        if name in self.vars:
            value = self.vars[name]
            if isinstance(value, tuple) and value[0] == 'function':
                return value[1]  # Return the operator string for assignments
            return value
        else:
            raise Exception(f"Variable no definida: {name}")

    def visitOperador(self, ctx: gParser.OperadorContext):
        return ctx.op().getText()

    def visitParenExpr(self, ctx: gParser.ParenExprContext):
        return self.visit(ctx.expr())

    # (de moment no suportem funcions)
    def visitCridaFuncio(self, ctx: gParser.CridaFuncioContext):
        name = ctx.ID().getText()
        arg = self.visit(ctx.expr())
        
        if name not in self.vars or self.vars[name][0] != 'function':
            raise Exception(f"No és una funció: {name}")
        
        op = self.vars[name][1]
        arg = np.atleast_1d(arg)  # Ensure argument is an array
        
        # Apply the operator monadically (x op x)
        if op == '+':      result = arg + arg
        elif op == '-':    result = arg - arg
        elif op == '*':    result = arg * arg
        elif op == '%':    result = arg // arg
        elif op == '|':    result = arg % arg
        elif op == '^':    result = arg ** arg
        else: raise Exception(f"Operador no suportat per funcions: {op}")
        
        print(self.formatResult(result))
        return result

def process_input(data, executor):
    input_stream = InputStream(data + '\n')
    lexer = gLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = gParser(tokens)
    return executor.visit(parser.root())

if __name__ == '__main__':
    executor = ExecVisitor()
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8') as f:
            process_input(f.read(), executor)
    else:
        print("Interactive mode. Enter expressions, or press Ctrl+D/Ctrl+C to exit.")
        while True:
            try:
                sys.stdout.write('> ')
                sys.stdout.flush()
                line = input()
                if line.strip():
                    process_input(line, executor)
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
