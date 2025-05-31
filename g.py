import sys
import numpy as np

from antlr4 import *
from gLexer import gLexer
from gParser import gParser
from gVisitor import gVisitor

class ExecVisitor(gVisitor):
    def __init__(self):
        self.vars = {}
        self.op_map = {
            '+':  lambda x, y: x + y,
            '-':  lambda x, y: x - y,
            '*':  lambda x, y: x * y,
            '%':  lambda x, y: x // y,
            '|':  lambda x, y: y % x,
            '^':  lambda x, y: x ** y,
            ',':  lambda x, y: np.concatenate((x, y)),
            '{':  self._index_op,
            '>':  lambda x, y: (x > y).astype(int),
            '<':  lambda x, y: (x < y).astype(int),
            '>=': lambda x, y: (x >= y).astype(int),
            '<=': lambda x, y: (x <= y).astype(int),
            '=':  lambda x, y: (x == y).astype(int),
            '<>': lambda x, y: (x != y).astype(int)
        }

    # Controla la indexació
    def _index_op(self, indices, array):
        if array.ndim != 1:
            raise ValueError("Indexing target must be a 1D array")
        if not np.all((indices >= 0) & (indices < len(array))):
            raise ValueError("Index out of bounds")
        return array[indices.astype(int)]

    # Funció auxiliar que transforma escalars en arrays
    def _to_array(self, value):
        return np.atleast_1d(value)

    # Asegura mides compatibles
    def _ensure_compatible_shapes(self, left, right, op):
        left, right = self._to_array(left), self._to_array(right)
        if op in {',', '{'}:
            return left, right
        if left.shape != right.shape:
            if left.shape == (1,):
                left = np.repeat(left, len(right))
            elif right.shape == (1,):
                right = np.repeat(right, len(left))
            else:
                raise ValueError("length error")
        return left, right

    # ROOT: recorre totes les stat, retorna una llista de valors
    def visitRoot(self, ctx: gParser.RootContext):
        return [self.visit(stmt) for stmt in ctx.stat()]

    # Assignació: guarda la variable i retorna el valor
    def visitAssignacio(self, ctx: gParser.AssignacioContext):
        name = ctx.ID().getText()
        expr = ctx.expr()
        value = self.visit(expr)
        if isinstance(value, str) and value in self.op_map:
            func = lambda y: self.op_map[value](y, y)
            # Almacenamos siempre con la representación textual
            self.vars[name] = ('function', func, value)
        else:
            self.vars[name] = value
        return value

    # Assignació de funcions: guarda la funció i la seva representació
    def visitAssignacioFuncio(self, ctx: gParser.AssignacioFuncioContext):
        name = ctx.ID().getText()
        func_def = ctx.funcDef()
        num = self._parse_num(func_def.NUM().getText())
        op = func_def.op().getText()
        if op not in self.op_map:
            raise ValueError(f"Unsupported operator in function definition: {op}")
        # Guardem la representació textual, per exemple "2 | ]"
        func_repr = f"{self._format_result(num)} {op} ]"
        func = lambda y: self.op_map[op](self._to_array(num), self._to_array(y))
        self.vars[name] = ('function', func, func_repr)
        return ('function', func, func_repr)

    # Expressió com a sentència: avaluem i imprimim
    def visitExpressio(self, ctx: gParser.ExpressioContext):
        result = self.visit(ctx.expr())
        print(self._format_result(result))
        return result

    # Formatea el resultat per a la impressió
    def _format_result(self, value):
        if isinstance(value, np.ndarray):
            return ' '.join(self._format_result(x) for x in value)
        elif isinstance(value, tuple) and value[0] == 'function':
            # Si la tupla tiene un tercer elemento, usarlo; si no, usar una representación genérica
            return value[2] if len(value) > 2 else "<function>"
        elif isinstance(value, (int, np.integer)):
            return f"_{abs(value)}" if value < 0 else str(value)
        else:
            return str(value)

    # Expressió binària dreta
    def visitOperacio(self, ctx: gParser.OperacioContext):
        un_op = ctx.unOp()
        atoms = [self.visit(atom) for atom in ctx.atom()]
        ops = [op.getText() for op in ctx.op()]
        
        # Si no hi ha operadors binaris, només tenim un atom
        if not ops:
            result = atoms[0]
        else:
            # Avaluem de dreta a esquerra
            result = atoms[-1]
            for i in range(len(ops) - 1, -1, -1):
                left, right = self._ensure_compatible_shapes(atoms[i], result, ops[i])
                result = self.op_map[ops[i]](left, right)
        
        # Si hi ha un operador unari ']'
        if un_op:
            un_op_text = un_op.getText()
            if un_op_text == ']':
                # Identitat: no fem res, retornem el resultat
                pass
            else:
                raise ValueError(f"Unsupported unary operator: {un_op_text}")
        
        return result

    def visitLlista(self, ctx: gParser.LlistaContext):
        nums = [self._parse_num(child.getText()) for child in ctx.getChildren()
                if child.getSymbol().type == gParser.NUM]
        return np.array(nums)

    def _parse_num(self, text):
        return -int(text[1:]) if text[0] == '_' else int(text)

    def visitVariable(self, ctx: gParser.VariableContext):
        name = ctx.ID().getText()
        if name not in self.vars:
            raise ValueError(f"Undefined variable: {name}")
        return self.vars[name]  # Devolvemos el valor completo (tupla o valor directo)

    def visitOperador(self, ctx: gParser.OperadorContext):
        return ctx.op().getText()

    def visitParenExpr(self, ctx: gParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitLlamadaFuncio(self, ctx: gParser.LlamadaFuncioContext):
        func_name = ctx.ID().getText()
        arg = self.visit(ctx.expr())
        if func_name not in self.vars or self.vars[func_name][0] != 'function':
            raise ValueError(f"Not a function: {func_name}")
        func = self.vars[func_name][1]
        return func(arg)

    # (de moment no suportem funcions)
    def visitCridaFuncio(self, ctx: gParser.CridaFuncioContext):
        name = ctx.ID().getText()
        if name not in self.vars or self.vars[name][0] != 'function':
            raise ValueError(f"Not a function: {name}")
        func = self.vars[name][1]
        arg = self.visit(ctx.expr())
        result = func(arg)
        print(self._format_result(result))
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
