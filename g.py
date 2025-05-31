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
            '<>': lambda x, y: (x != y).astype(int),
            '#':  self._copy_op  # Operador binario '#'
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
        left = self._to_array(left)
        right = self._to_array(right)
        if op in {',', '{', '#'}:  # Operadores que manejan arrays directamente
            return left, right
        if left.shape != right.shape:
            if left.shape == (1,):
                left = np.repeat(left, len(right))
            elif right.shape == (1,):
                right = np.repeat(right, len(left))
            else:
                raise ValueError("length error")
        return left, right

    def _copy_op(self, left, right):
        left = self._to_array(left)
        right = self._to_array(right)
        
        if left.ndim == 0:  # Left es escalar
            n = left.item()
            if not isinstance(n, (int, np.integer)):
                raise ValueError("Replication count must be an integer")
            n = max(0, n)  # No permitir repeticiones negativas
            if right.ndim == 0:  # Right también es escalar
                x = right.item()
                result = np.repeat(x, n)
            else:  # Right es un array
                result = np.repeat(right, n)
        elif right.ndim == 0:  # Right es escalar
            x = right.item()
            if not np.issubdtype(left.dtype, np.integer):
                raise ValueError("Replication counts must be integers")
            result = []
            for n in left:
                n = max(0, n)
                result.extend([x] * n)
            result = np.array(result)
        else:  # Ambos son arrays
            if left.shape != right.shape or left.ndim != 1 or right.ndim != 1:
                raise ValueError("length error")
            if not np.issubdtype(left.dtype, np.integer):
                raise ValueError("Replication counts must be integers")
            result = []
            for n, x in zip(left, right):
                n = max(0, n)
                result.extend([x] * n)
            result = np.array(result)
        return result

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
        if func_def.getChildCount() == 2 and func_def.getChild(1).getText() == ':':
            # Caso del modificador ":"
            base_op = func_def.baseBinOp().getText()
            if base_op not in self.op_map:
                raise ValueError(f"Unsupported operator: {base_op}")
            func_repr = base_op + ':'  # Ej. "*:"
            func = lambda y: self.op_map[base_op](self._to_array(y), self._to_array(y))
        else:
            # Caso original "NUM binOp ]"
            num = self._parse_num(func_def.NUM().getText())
            op = func_def.binOp().getText()
            if op not in self.op_map:
                raise ValueError(f"Unsupported operator in function definition: {op}")
            func_repr = f"{self._format_result(num)} {op} ]"  # Ej. "2 | ]"
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

    def visitGenerador(self, ctx: gParser.GeneradorContext):
        expr_value = self.visit(ctx.expr())  # Evaluamos la expresión
        n = self._to_array(expr_value)  # Convertimos a array
        if n.size != 1:
            raise ValueError("Argument to i. must be a scalar")
        n = n.item()  # Obtenemos el valor escalar
        if not isinstance(n, (int, np.integer)):
            raise ValueError("Argument to i. must be an integer")
        if n < 0:
            return np.arange(-n - 1, -1, -1)  # Ej. n = -5 -> [4, 3, 2, 1, 0]
        return np.arange(n)  # Ej. n = 7 -> [0, 1, 2, 3, 4, 5, 6]

    # Expressió binària dreta
    def visitOperacio(self, ctx: gParser.OperacioContext):
        un_op = ctx.unOp()
        atoms = [self.visit(atom) for atom in ctx.atom()]
        ops = [op.getText() for op in ctx.binOp()]

        # Si no hay operadores binarios, tomamos el primer atom
        if not ops:
            result = atoms[0]
        else:
            # Evaluamos de derecha a izquierda
            result = atoms[-1]
            for i in range(len(ops) - 1, -1, -1):
                op_full = ops[i]
                base_op = op_full.rstrip('~')
                num_flips = len(op_full) - len(base_op)
                if base_op not in self.op_map:
                    raise ValueError(f"Unsupported operator: {base_op}")
                if num_flips % 2 == 0:
                    left = atoms[i]
                    right = result
                else:
                    left = result
                    right = atoms[i]
                left, right = self._ensure_compatible_shapes(left, right, base_op)
                result = self.op_map[base_op](left, right)

        # Aplicar operador unario si existe
        if un_op:
            un_op_text = un_op.getText()
            if un_op_text.endswith(':'):
                base_op = un_op_text[:-1]  # Extraer el operador base, ej. "+" de "+:"
                if base_op not in self.op_map:
                    raise ValueError(f"Unsupported operator: {base_op}")
                result = self.op_map[base_op](self._to_array(result), self._to_array(result))
            else:
                base_un_op = un_op_text.rstrip('~')
                num_flips = len(un_op_text) - len(base_un_op)
                if base_un_op == ']':
                    pass  # Identidad
                elif base_un_op == '#':
                    if num_flips % 2 == 0:
                        result = len(self._to_array(result))  # Longitud
                    else:
                        result = self._copy_op(result, result)  # Reflexivo
                else:
                    raise ValueError(f"Unsupported unary operator: {base_un_op}")

        return result

    def visitOperador(self, ctx: gParser.OperadorContext):
        return ctx.getText()  # Devuelve el texto completo, por ejemplo "+~" o "#"

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
                # Imprimir en rojo usando códigos ANSI
                print(f"\033[91mError: {e}\033[0m")
