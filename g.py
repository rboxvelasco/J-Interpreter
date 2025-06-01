import sys
import numpy as np
from functools import reduce

from antlr4 import *
from gLexer import gLexer
from gParser import gParser
from gVisitor import gVisitor

class ExecVisitor(gVisitor):

    # Initializes the visitor with the next elements:
    #  - vars:   dictionary to store variables and functions
    #  - op_map: dictionary to store binary operators and its action
    def __init__(self):
        self.vars = {}
        self.vars['i.'] = ('function', self._i_dot_funct, 'i.')
        self.bin_op_map = {
            '+':  lambda x, y: x + y,  # Addition
            '-':  lambda x, y: x - y,  # Substraction
            '*':  lambda x, y: x * y,  # Product
            '%':  lambda x, y: x // y, # Division
            '|':  lambda x, y: y % x,  # Remaining
            '^':  lambda x, y: x ** y, # Power
            '>':  lambda x, y: (x > y).astype(int),       # Greater than
            '<':  lambda x, y: (x < y).astype(int),       # Less than
            '>=': lambda x, y: (x >= y).astype(int),      # Greater than or equal
            '<=': lambda x, y: (x <= y).astype(int),      # Less than or equal
            '=':  lambda x, y: (x == y).astype(int),      # Equal
            '<>': lambda x, y: (x != y).astype(int),      # Different
            ',':  lambda x, y: np.concatenate((x, y)),    # Concatenation
            'e.': lambda x, y: np.isin(x, y).astype(int), # Membership
            '*.': lambda x, y: (self._to_array(x) & self._to_array(y)).astype(int),  # AND
            '+.': lambda x, y: (self._to_array(x) | self._to_array(y)).astype(int),  # OR
            '}.': lambda n, y: self._to_array(y)[max(0, self._to_array(n).item()):], # Drop
            '{.': self._take,     # Not a lambda function since it fulfills with 0's
            '#':  self._copy_op,  # Binary operator, not unary
            '{':  self._index_op,
            '@:': self._compose_op
        }
        self.un_op_map = {
            '|': lambda x: np.abs(x),  # Absolute Value
            ']': lambda x: x,          # Identity (devuelve el valor sin cambios)
            '#': lambda x: len(x)      # List length
        }

    def visitIDotFunction(self, ctx: gParser.IDotFunctionContext):
        """Devuelve la función i. para usar en composiciones."""
        if 'i.' not in self.vars:
            raise ValueError("i. is not defined")
        return self.vars['i.']  # Retorna la tupla ('function', _i_dot_func, 'i.')

    def apply_unary_op(self, op_text, value):
        value = self._to_array(value)
        if op_text.endswith(':'):
            base_op = op_text[:-1]
            if base_op not in self.bin_op_map:
                raise ValueError(f"Can not transform {base_op} from binary to unary")
            return self.bin_op_map[base_op](value, value)

        base_op = op_text.rstrip('~')
        num_flips = len(op_text) - len(base_op)

        # Special case '#~', that should be transformed to binary
        if base_op == '#':
            return self.bin_op_map[base_op](value, value) if num_flips > 0 else self.un_op_map[base_op](value)
        elif base_op in self.un_op_map:
            return self.un_op_map[base_op](value)
        else:
            raise ValueError(f"Operador unario no soportado: {base_op}")


    def visitUnaryOperation(self, ctx: gParser.UnaryOperationContext):
        op_text = ctx.unaryOp().getText()
        value = self.visit(ctx.expr())
        return self.apply_unary_op(op_text, value)


    def visitDerivedVerbAtom(self, ctx: gParser.DerivedVerbAtomContext):
        base_op = ctx.binToUnOp().baseBinOp().getText()
        if base_op not in self.bin_op_map:
            raise ValueError(f"Unsupported operator: {base_op}")
        func = lambda y: self.bin_op_map[base_op](self._to_array(y), self._to_array(y))
        func_repr = base_op + ':'
        return ('function', func, func_repr)

    def _i_dot_funct(self, y):
            """Implementación de i.: genera un vector de enteros."""
            y = self._to_array(y)  # Asegúrate de que _to_array esté definido
            if y.size != 1:
                raise ValueError("Argument to i. must be a scalar")
            n = y.item()
            if not isinstance(n, (int, np.integer)):
                raise ValueError("Argument to i. must be an integer")
            if n < 0:
                return np.arange(-n - 1, -1, -1)  # Soporte para negativos
            return np.arange(n)  # e.g., i. 3 -> [0, 1, 2]

    def visitGeneratorAtom(self, ctx: gParser.GeneratorAtomContext):
        """Aplica i. al argumento para generar un vector."""
        arg = self.visit(ctx.expr())
        if 'i.' not in self.vars:
            raise ValueError("i. is not defined")
        i_dot_func = self.vars['i.'][1]  # Obtiene la función
        return i_dot_func(arg)




    # ROOT: visits every statement and returns a list of values
    def visitRoot(self, ctx: gParser.RootContext):
        return [self.visit(stmt) for stmt in ctx.stat()]

    # Evaluates a parenthesized expression
    def visitParenExpr(self, ctx: gParser.ParenExprContext):
        return self.visit(ctx.expr())

    # Evaluates an expression
    def visitExpressio(self, ctx: gParser.ExpressioContext):
        result = self.visit(ctx.expr())
        print(self._format_result(result))
        return result

    # Returns an operator
    def visitOperator(self, ctx: gParser.OperatorContext):
        return ctx.getText()

    # Returns the value of a variable
    def visitVariable(self, ctx: gParser.VariableContext):
        name = ctx.ID().getText()
        if name not in self.vars:
            raise ValueError(f"Undefined variable: {name}")
        return self.vars[name]

    # Returns an array
    def visitLists(self, ctx: gParser.ListsContext):
        nums = [self._parse_num(child.getText()) for child in ctx.getChildren()
                if child.getSymbol().type == gParser.NUM]
        return np.array(nums)

    # Stores the variable and returns its value
    def visitAssignation(self, ctx: gParser.AssignationContext):
        name = ctx.ID().getText()
        value = self.visit(ctx.expr())
        if isinstance(value, str) and value in self.bin_op_map:
            func = lambda y: self.bin_op_map[value](y, y)
            self.vars[name] = ('function', func, value)
        else:
            self.vars[name] = value
        return value





    def _compose_op(self, left, right):
        """Compone dos funciones: (left @: right) y"""
        # Verificar que ambos operandos sean funciones
        if not (isinstance(left, tuple) and left[0] == 'function'):
            raise ValueError("Left operand of @: must be a function")
        if not (isinstance(right, tuple) and right[0] == 'function'):
            raise ValueError("Right operand of @: must be a function")
        
        left_func = left[1]
        right_func = right[1]
        left_repr = left[2] if len(left) > 2 else ""
        right_repr = right[2] if len(right) > 2 else ""
        
        # Crear función compuesta: left(right(y))
        composed_func = lambda y: left_func(right_func(y))
        composed_repr = f"{left_repr} @: {right_repr}"
        
        return ('function', composed_func, composed_repr)

    # Asegura mides compatibles
    def _ensure_compatible_shapes(self, left, right, op):
        # Para composición, no convertir a arrays
        if op == '@:':
            return left, right

        left = self._to_array(left)
        right = self._to_array(right)
        if op in {',', '{', '#', 'e.', '{.', '}.'}:  # Operadores que manejan arrays directamente
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
        
        if left.ndim == 0:  # Left is scalar
            n = left.item()
            if not isinstance(n, (int, np.integer)):
                raise ValueError("Replication count must be an integer")
            return np.repeat(right.item() if right.ndim == 0 else right, max(0, n))
        
        if not np.issubdtype(left.dtype, np.integer):
            raise ValueError("Replication counts must be integers")
        
        if right.ndim == 0:
            return np.array([right.item()] * max(0, left.item()) if left.ndim == 0
                    else [x for n in left for x in [right.item()] * max(0, n)])
        
        if left.shape != right.shape or left.ndim != 1 or right.ndim != 1:
            raise ValueError("length error")
        
        return np.array([x for n, x in zip(left, right) for _ in range(max(0, n))])

    def get_op_func(self, bin_op_text):
        base_op = bin_op_text.rstrip('~')  # Quita los '~' del final
        num_flips = len(bin_op_text) - len(base_op)  # Cuenta los '~'
        if base_op not in self.bin_op_map:
            raise ValueError(f"Unsupported operator: {base_op}")

        op_func = self.bin_op_map[base_op]  # Obtener la función base
        if num_flips % 2 == 1:  # Si hay un número impar de '~', invertir operandos
            return lambda x, y: op_func(y, x)
        return op_func

    # Assignació de funcions: guarda la funció i la seva representació
    def visitDeclareFunction(self, ctx: gParser.DeclareFunctionContext):
        name = ctx.ID().getText()
        func_def = ctx.funcDef()
        if func_def.getChildCount() == 2 and func_def.getChild(1).getText() == ':':
            # Caso del modificador ":"
            base_op = func_def.binToUnOp().getText()
            if base_op not in self.bin_op_map:
                raise ValueError(f"Unsupported operator: {base_op}")
            func_repr = base_op + ':'  # Ej. "*:"
            func = lambda y: self.bin_op_map[base_op](self._to_array(y), self._to_array(y))
        else:
            # Caso original "NUM binOp ]"
            num = self._parse_num(func_def.NUM().getText())
            op = func_def.binOp().getText()
            if op not in self.bin_op_map:
                raise ValueError(f"Unsupported operator in function definition: {op}")
            func_repr = f"{self._format_result(num)} {op} ]"  # Ej. "2 | ]"
            func = lambda y: self.bin_op_map[op](self._to_array(num), self._to_array(y))
        self.vars[name] = ('function', func, func_repr)
        return ('function', func, func_repr)

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
    def visitOperation(self, ctx: gParser.OperationContext):
        atoms = [self.visit(atom) for atom in ctx.atom()]
        ops = [op.getText() for op in ctx.binOp()]

        if not ops:
            return atoms[0]

        # Evaluamos de derecha a izquierda
        result = atoms[-1]
        for i in range(len(ops) - 1, -1, -1):
            op_full = ops[i]
            base_op = op_full.rstrip('~')
            num_flips = len(op_full) - len(base_op)

            if base_op == '@:':
                # Composición de funciones
                left = atoms[i]
                right = result
                if not (isinstance(left, tuple) and left[0] == 'function'):
                    raise ValueError("Left operand of @: must be a function")
                if not (isinstance(right, tuple) and right[0] == 'function'):
                    raise ValueError("Right operand of @: must be a function")
                result = self._compose_op(left, right)
            else:
                # Operación binaria regular
                if isinstance(atoms[i], tuple) and atoms[i][0] == 'function':
                    raise ValueError("Cannot apply binary operator to function")
                if isinstance(result, tuple) and result[0] == 'function':
                    raise ValueError("Cannot apply binary operator to function")
                left = atoms[i]
                right = result
                if num_flips % 2 == 1:
                    left, right = right, left
                left, right = self._ensure_compatible_shapes(left, right, base_op)
                result = self.bin_op_map[base_op](left, right)

        return result

    def visitFoldFunction(self, ctx: gParser.FoldFunctionContext):
        bin_op_text = ctx.binOp().getText()
        op_func = self.get_op_func(bin_op_text)
        func = lambda y: reduce(op_func, self._to_array(y))
        func_repr = f"{bin_op_text}/"
        return ('function', func, func_repr)

    def visitFold(self, ctx: gParser.FoldContext):
        bin_op_text = ctx.binOp().getText()
        array = self.visit(ctx.atom())
        array = self._to_array(array)
        
        if array.size == 0:
            raise ValueError("Fold on empty array")
        if array.ndim == 1:
            array_list = [np.array([x]) for x in array]
        else:
            array_list = array
        
        op_func = self.get_op_func(bin_op_text)
        return reduce(op_func, array_list)



    def _parse_num(self, text):
        return -int(text[1:]) if text[0] == '_' else int(text)


    def visitFunctionEval(self, ctx: gParser.FunctionEvalContext):
        func_name = ctx.ID().getText()
        arg = self.visit(ctx.expr())
        if func_name not in self.vars or self.vars[func_name][0] != 'function':
            raise ValueError(f"Not a function: {func_name}")
        func = self.vars[func_name][1]
        return func(arg)

    # (de moment no suportem funcions)
    def visitFunctionCall(self, ctx: gParser.FunctionCallContext):
        name = ctx.ID().getText()
        if name not in self.vars or self.vars[name][0] != 'function':
            raise ValueError(f"Not a function: {name}")
        func = self.vars[name][1]
        arg = self.visit(ctx.expr())
        result = func(arg)
        print(self._format_result(result))
        return result


    """Auxiliar functions"""
    # Transforms scalars into arrays
    def _to_array(self, value):
        return np.atleast_1d(value)

    # Implements the indexation functionality
    def _index_op(self, indices, array):
        if not np.all((indices >= 0) & (indices < len(array))):
            raise ValueError("Index out of bounds")
        return array[indices.astype(int)]

    # Implements the take functionality
    def _take(self, n, y):
        y = self._to_array(y)
        n = self._to_array(n).item()
        if n > len(y): return np.concatenate((y, np.zeros(n - len(y), dtype=y.dtype)))
        else:          return y[:n]


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
