# Generated from g.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .gParser import gParser
else:
    from gParser import gParser

# This class defines a complete generic visitor for a parse tree produced by gParser.

class gVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by gParser#root.
    def visitRoot(self, ctx:gParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#assignacio.
    def visitAssignacio(self, ctx:gParser.AssignacioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#expressio.
    def visitExpressio(self, ctx:gParser.ExpressioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#operacio.
    def visitOperacio(self, ctx:gParser.OperacioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#variable.
    def visitVariable(self, ctx:gParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#parenExpr.
    def visitParenExpr(self, ctx:gParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#llistaNumeros.
    def visitLlistaNumeros(self, ctx:gParser.LlistaNumerosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#llista.
    def visitLlista(self, ctx:gParser.LlistaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#suma.
    def visitSuma(self, ctx:gParser.SumaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#resta.
    def visitResta(self, ctx:gParser.RestaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#multiplicacio.
    def visitMultiplicacio(self, ctx:gParser.MultiplicacioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#divisio.
    def visitDivisio(self, ctx:gParser.DivisioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#modul.
    def visitModul(self, ctx:gParser.ModulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by gParser#potencia.
    def visitPotencia(self, ctx:gParser.PotenciaContext):
        return self.visitChildren(ctx)



del gParser