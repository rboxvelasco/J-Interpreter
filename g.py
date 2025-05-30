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
            
            # Handle array shapes
            if left.shape != right.shape:
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
            elif op == '%':    result = left // right  # Integer division
            elif op == '|':    result = right % left  # J's | is right % left
            elif op == '^':    result = left ** right
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
    executor = ExecVisitor()

    if len(sys.argv) > 1:
        # If a file is provided as an argument, process it as before
        data = open(sys.argv[1], encoding='utf-8').read()
        input_stream = InputStream(data)
        lexer = gLexer(input_stream)
        tokens = CommonTokenStream(lexer)
        parser = gParser(tokens)
        tree = parser.root()
        executor.visit(tree)
    else:
        # Interactive REPL mode
        print("Interactive mode. Enter expressions, or press Ctrl+D/Ctrl+C to exit.")
        while True:
            try:
                # Display prompt and read input
                sys.stdout.write('> ')
                sys.stdout.flush()
                line = input()
                if not line.strip():
                    continue  # Skip empty lines

                # Process the input line
                input_stream = InputStream(line + '\n')  # Add newline for proper parsing
                lexer = gLexer(input_stream)
                tokens = CommonTokenStream(lexer)
                parser = gParser(tokens)
                tree = parser.root()
                executor.visit(tree)

            except EOFError:
                print("\nExiting...")
                break
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
