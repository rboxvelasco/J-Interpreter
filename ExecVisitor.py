import numpy as np
from functools import reduce

from antlr4 import *
from gParser import gParser
from gVisitor import gVisitor


class ExecVisitor(gVisitor):

    # Initializes the visitor with the next elements:
    #  - vars:   dictionary to store variables and functions
    #  - bin_op_map: dictionary to store binary operators and its action
    #  - un_op_map: dictionary to store binary operators and its action
    def __init__(self):
        self.vars = {}
        self.vars['i.'] = ('function', self._i_dot_func, 'i.')
        self.vars['i:'] = ('function', self._i_colon_func, 'i:')
        self.un_op_map = {
            ']': lambda x: x, 
            '#': lambda x: len(x),
            '|': lambda x: np.abs(x), 
            '>:': lambda x: x + 1,
            '<:': lambda x: x - 1,
            '|.': lambda x: np.flip(x),
            '-.': lambda x: (x == 0).astype(int)
        }
        self.bin_op_map = {
            '+':  lambda x, y: x + y,
            '-':  lambda x, y: x - y,
            '*':  lambda x, y: x * y,
            '%':  lambda x, y: x // y,
            '|':  lambda x, y: y % x,
            '^':  lambda x, y: x ** y,
            '>':  lambda x, y: (x > y).astype(int),
            '<':  lambda x, y: (x < y).astype(int),
            '>=': lambda x, y: (x >= y).astype(int),
            '<=': lambda x, y: (x <= y).astype(int),
            '=':  lambda x, y: (x == y).astype(int),
            '<>': lambda x, y: (x != y).astype(int),
            ',':  lambda x, y: np.concatenate((x, y)),
            'e.': lambda x, y: np.isin(x, y).astype(int),
            '*.': lambda x, y: (self._to_array(x) & self._to_array(y)).astype(int),
            '+.': lambda x, y: (self._to_array(x) | self._to_array(y)).astype(int),
            '}.': lambda n, y: self._to_array(y)[max(0, self._to_array(n).item()):],
            '{.': self._take,
            '#':  self._copy_op,
            '{':  self._index_op,
            '@:': self._compose_op
        }

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
    def visitList(self, ctx: gParser.ListContext):
        nums = [self._parse_num(child.getText()) for child in ctx.getChildren()
                if child.getSymbol().type == gParser.NUM]
        return np.array(nums)

    # Returns i. function tuple
    def visitIDotFunction(self, ctx: gParser.IDotFunctionContext):
        return self.vars['i.']

    # Returns i: function tuple
    def visitIColonFunction(self, ctx: gParser.IColonFunctionContext):
        return self.vars['i:']

    # Returns a function tuple
    def visitDerivedVerbAtom(self, ctx: gParser.DerivedVerbAtomContext):
        base_op = ctx.binToUnOp().baseBinOp().getText()
        if base_op not in self.bin_op_map:
            raise ValueError(f"Unsupported operator: {base_op}")
        func = lambda y: self.bin_op_map[base_op](self._to_array(y), self._to_array(y))
        func_repr = base_op + ':'
        return ('function', func, func_repr)

    # Returns the operation evaluated
    def visitUnaryOperation(self, ctx: gParser.UnaryOperationContext):
        op_text = ctx.unaryOp().getText()
        value = self.visit(ctx.expr())
        return self._apply_unary_op(op_text, value)

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

    # Returns a function tuple
    def visitFoldFunction(self, ctx: gParser.FoldFunctionContext):
        bin_op_text = ctx.binOp().getText()
        op_func = self._get_op_func(bin_op_text)
        func = lambda y: reduce(op_func, self._to_array(y))
        func_repr = f"{bin_op_text}/"
        return ('function', func, func_repr)

    # Evaluates the fold expression
    def visitFold(self, ctx: gParser.FoldContext):
        bin_op_text = ctx.binOp().getText()
        array = self._to_array(self.visit(ctx.atom()))
        
        if array.size == 0:
            raise ValueError("Fold on empty array")
        else:
            array_list = [np.array([x]) for x in array]
        
        op_func = self._get_op_func(bin_op_text)
        return reduce(op_func, array_list)

    # Evaluates a declared function
    def visitFunctionEval(self, ctx: gParser.FunctionEvalContext):
        name = ctx.ID().getText()
        arg = self.visit(ctx.expr())
        return self._evaluate_function(name, arg)

    # Evaluates a function and prints its result
    def visitFunctionCall(self, ctx: gParser.FunctionCallContext):
        name = ctx.ID().getText()
        arg = self.visit(ctx.expr())
        result = self._evaluate_function(name, arg)
        print(self._format_result(result))
        return result

    # Applies i. or i: to the argument to generate a vector.
    def visitGenerator(self, ctx: gParser.GeneratorContext):
        generator = ctx.getChild(0).getText()
        arg = self.visit(ctx.expr())
        gen_func = self.vars[generator][1]
        return gen_func(arg)

    # Function assignment: stores function and its representation
    def visitDeclareFunction(self, ctx: gParser.DeclareFunctionContext):
        name = ctx.ID().getText()
        func_def = ctx.funcDef()

        # Special case of modifier :
        if func_def.getChildCount() == 2 and func_def.getChild(1).getText() == ':':
            base_op = func_def.binToUnOp().getText()
            if base_op not in self.bin_op_map:
                raise ValueError(f"Unsupported operator: {base_op}")
            func_repr = base_op + ':'
            func = lambda y: self.bin_op_map[base_op](self._to_array(y), self._to_array(y))
        else:
            num = self._parse_num(func_def.NUM().getText())
            op = func_def.binOp().getText()
            if op not in self.bin_op_map:
                raise ValueError(f"Unsupported operator in function definition: {op}")
            func_repr = f"{self._format_result(num)} {op} ]"
            func = lambda y: self.bin_op_map[op](self._to_array(num), self._to_array(y))

        self.vars[name] = ('function', func, func_repr)
        return ('function', func, func_repr)

    # Evaluates an atom or binary operation
    def visitBinaryOperation(self, ctx: gParser.BinaryOperationContext):
        atoms = [self.visit(atom) for atom in ctx.atom()]
        ops = [op.getText() for op in ctx.binOp()]

        if not ops:
            return atoms[0]

        result = atoms[-1]  # From right to left
        for i in range(len(ops) - 1, -1, -1):
            op_full = ops[i]
            base_op = op_full.rstrip('~')
            num_flips = len(op_full) - len(base_op)
            left = atoms[i]
            right = result

            if base_op != '@:':
                if isinstance(left, tuple) and left[0] == 'function':
                    raise ValueError("Cannot apply binary operator to function")
                if isinstance(right, tuple) and right[0] == 'function':
                    raise ValueError("Cannot apply binary operator to function")
                if num_flips % 2 == 1:
                    left, right = right, left
                left, right = self._ensure_compatible_shapes(left, right, base_op)

            result = self.bin_op_map[base_op](left, right)
        return result


    """ --------------------- Auxiliar methods -----------------------"""

    # Transforms scalars into arrays
    def _to_array(self, value):
        return np.atleast_1d(value)

    # Parses numbers into J's negative representation (_)
    def _parse_num(self, text):
        return -int(text[1:]) if text[0] == '_' else int(text)

    # Formats result to print it
    def _format_result(self, value):
        if isinstance(value, np.ndarray):
            return ' '.join(self._format_result(x) for x in value)
        elif isinstance(value, tuple) and value[0] == 'function':
            return value[2] if len(value) > 2 else "<function>"
        elif isinstance(value, (int, np.integer)):
            return f"_{abs(value)}" if value < 0 else str(value)
        else:
            return str(value)

    # Implements the indexed access functionality
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

    # Returns the original or flipped function, depending on ~ modifier
    def _get_op_func(self, bin_op_text):
        base_op = bin_op_text.rstrip('~')
        num_flips = len(bin_op_text) - len(base_op)
        if base_op not in self.bin_op_map:
            raise ValueError(f"Unsupported operator: {base_op}")

        op_func = self.bin_op_map[base_op]
        if num_flips % 2 == 1:
            return lambda x, y: op_func(y, x)
        return op_func

    # Implements i. functionality
    def _i_dot_func(self, y):
        y = self._to_array(y)
        if y.size != 1:
            raise ValueError("Argument to i. must be an integer")
        n = y.item()
        if not isinstance(n, (int, np.integer)):
            raise ValueError("Argument to i. must be an integer")
        if n < 0:
            return np.arange(-n - 1, -1, -1)
        return np.arange(n)

    # Implements i: functionality
    def _i_colon_func(self, y):
        y = self._to_array(y)
        if y.size != 1:
            raise ValueError("Argument to i: must be a scalar")
        n = y.item()
        if not isinstance(n, (int, np.integer)):
            raise ValueError("Argument to i: must be an integer")
        return np.arange(-abs(n), abs(n) + 1)

    # Evaluates a function, given its name and arguments
    def _evaluate_function(self, name, arg):
        if name not in self.vars or self.vars[name][0] != 'function':
            raise ValueError(f"Not a function: {name}")
        func = self.vars[name][1]
        return func(arg)

    # Evaluates a unary expression
    def _apply_unary_op(self, op_text, value):
        value = self._to_array(value)
        if op_text.endswith(':') and op_text not in ['>:', '<:']:
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
            raise ValueError(f"Unary operator not supported: {base_op}")

    # Ensures compatible sizes of lists
    def _ensure_compatible_shapes(self, left, right, op):
        if op == '@:':
            return left, right

        left = self._to_array(left)
        right = self._to_array(right)
        if op in {',', '{', '#', 'e.', '{.', '}.'}:
            return left, right

        if left.shape != right.shape:
            if left.shape == (1,):
                left = np.repeat(left, len(right))
            elif right.shape == (1,):
                right = np.repeat(right, len(left))
            else:
                raise ValueError("length error")
        return left, right

    # Compounds two functions: (left @: right)
    def _compose_op(self, left, right):
        if not (isinstance(left, tuple) and left[0] == 'function'):
            raise ValueError("Left operand of @: must be a function")
        if not (isinstance(right, tuple) and right[0] == 'function'):
            raise ValueError("Right operand of @: must be a function")
        
        left_func = left[1]
        right_func = right[1]
        left_repr = left[2] if len(left) > 2 else ""
        right_repr = right[2] if len(right) > 2 else ""
        
        composed_func = lambda y: left_func(right_func(y))
        composed_repr = f"{left_repr} @: {right_repr}"
        return ('function', composed_func, composed_repr)

    # Implements replication functionality
    def _copy_op(self, left, right):
        left = self._to_array(left)
        right = self._to_array(right)

        if not np.issubdtype(left.dtype, np.integer):
            raise ValueError("Replication counts must be integers")

        l, r = left, right
        if l.ndim == 0: l = np.full_like(right, l.item())
        if r.ndim == 0: r = np.full(len(left), r.item())

        if len(l) != len(r):
            raise ValueError("length error")

        return np.array([x for n, x in zip(l, r) for _ in range(max(0, n))])
