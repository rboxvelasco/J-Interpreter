import sys

from antlr4 import *
from gLexer import gLexer
from gParser import gParser
from ExecVisitor import ExecVisitor


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
