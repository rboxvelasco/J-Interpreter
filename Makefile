# Variables
GRAMMAR = g.g4

# Archivos generados
GENERATED = gLexer.py gParser.py gVisitor.py

# Default target
all: $(GENERATED)

# Compile the grammar
$(GENERATED): $(GRAMMAR)
	java -jar ~/.local/lib/antlr/antlr-4.13.1-complete.jar -Dlanguage=Python3 -no-listener -visitor $(GRAMMAR)
#	antlr4 -Dlanguage=Python3 -no-listener -visitor $(GRAMMAR)

# Clean generated files
clean:
	rm -f *.interp *.tokens *Lexer.py *Parser.py gVisitor.py
