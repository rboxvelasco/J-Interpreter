# Generated from g.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,13,55,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,0,4,
        0,14,8,0,11,0,12,0,15,1,0,1,0,1,1,1,1,1,1,1,1,3,1,24,8,1,1,2,1,2,
        1,2,1,2,3,2,30,8,2,1,3,1,3,1,3,1,3,1,3,1,3,3,3,38,8,3,1,4,1,4,5,
        4,42,8,4,10,4,12,4,45,9,4,1,5,1,5,1,5,1,5,1,5,1,5,3,5,53,8,5,1,5,
        0,0,6,0,2,4,6,8,10,0,0,59,0,13,1,0,0,0,2,23,1,0,0,0,4,25,1,0,0,0,
        6,37,1,0,0,0,8,39,1,0,0,0,10,52,1,0,0,0,12,14,3,2,1,0,13,12,1,0,
        0,0,14,15,1,0,0,0,15,13,1,0,0,0,15,16,1,0,0,0,16,17,1,0,0,0,17,18,
        5,0,0,1,18,1,1,0,0,0,19,20,5,12,0,0,20,21,5,1,0,0,21,24,3,4,2,0,
        22,24,3,4,2,0,23,19,1,0,0,0,23,22,1,0,0,0,24,3,1,0,0,0,25,29,3,6,
        3,0,26,27,3,10,5,0,27,28,3,4,2,0,28,30,1,0,0,0,29,26,1,0,0,0,29,
        30,1,0,0,0,30,5,1,0,0,0,31,38,5,12,0,0,32,33,5,2,0,0,33,34,3,4,2,
        0,34,35,5,3,0,0,35,38,1,0,0,0,36,38,3,8,4,0,37,31,1,0,0,0,37,32,
        1,0,0,0,37,36,1,0,0,0,38,7,1,0,0,0,39,43,5,11,0,0,40,42,5,11,0,0,
        41,40,1,0,0,0,42,45,1,0,0,0,43,41,1,0,0,0,43,44,1,0,0,0,44,9,1,0,
        0,0,45,43,1,0,0,0,46,53,5,4,0,0,47,53,5,5,0,0,48,53,5,6,0,0,49,53,
        5,7,0,0,50,53,5,8,0,0,51,53,5,9,0,0,52,46,1,0,0,0,52,47,1,0,0,0,
        52,48,1,0,0,0,52,49,1,0,0,0,52,50,1,0,0,0,52,51,1,0,0,0,53,11,1,
        0,0,0,6,15,23,29,37,43,52
    ]

class gParser ( Parser ):

    grammarFileName = "g.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'=:'", "'('", "')'", "'+'", "'-'", "'*'", 
                     "'%'", "'|'", "'^'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "COMMENT", "NUM", "ID", 
                      "WS" ]

    RULE_root = 0
    RULE_stat = 1
    RULE_expr = 2
    RULE_atom = 3
    RULE_list = 4
    RULE_op = 5

    ruleNames =  [ "root", "stat", "expr", "atom", "list", "op" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    COMMENT=10
    NUM=11
    ID=12
    WS=13

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(gParser.EOF, 0)

        def stat(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(gParser.StatContext)
            else:
                return self.getTypedRuleContext(gParser.StatContext,i)


        def getRuleIndex(self):
            return gParser.RULE_root

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = gParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 13 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 12
                self.stat()
                self.state = 15 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 6148) != 0)):
                    break

            self.state = 17
            self.match(gParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return gParser.RULE_stat

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class AssignacioContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(gParser.ID, 0)
        def expr(self):
            return self.getTypedRuleContext(gParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignacio" ):
                return visitor.visitAssignacio(self)
            else:
                return visitor.visitChildren(self)


    class ExpressioContext(StatContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.StatContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(gParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressio" ):
                return visitor.visitExpressio(self)
            else:
                return visitor.visitChildren(self)



    def stat(self):

        localctx = gParser.StatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stat)
        try:
            self.state = 23
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = gParser.AssignacioContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 19
                self.match(gParser.ID)
                self.state = 20
                self.match(gParser.T__0)
                self.state = 21
                self.expr()
                pass

            elif la_ == 2:
                localctx = gParser.ExpressioContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 22
                self.expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return gParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class OperacioContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def atom(self):
            return self.getTypedRuleContext(gParser.AtomContext,0)

        def op(self):
            return self.getTypedRuleContext(gParser.OpContext,0)

        def expr(self):
            return self.getTypedRuleContext(gParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperacio" ):
                return visitor.visitOperacio(self)
            else:
                return visitor.visitChildren(self)



    def expr(self):

        localctx = gParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_expr)
        self._la = 0 # Token type
        try:
            localctx = gParser.OperacioContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            self.atom()
            self.state = 29
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1008) != 0):
                self.state = 26
                self.op()
                self.state = 27
                self.expr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return gParser.RULE_atom

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class LlistaNumerosContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def list_(self):
            return self.getTypedRuleContext(gParser.ListContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLlistaNumeros" ):
                return visitor.visitLlistaNumeros(self)
            else:
                return visitor.visitChildren(self)


    class VariableContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(gParser.ID, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariable" ):
                return visitor.visitVariable(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(gParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)



    def atom(self):

        localctx = gParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_atom)
        try:
            self.state = 37
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [12]:
                localctx = gParser.VariableContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 31
                self.match(gParser.ID)
                pass
            elif token in [2]:
                localctx = gParser.ParenExprContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 32
                self.match(gParser.T__1)
                self.state = 33
                self.expr()
                self.state = 34
                self.match(gParser.T__2)
                pass
            elif token in [11]:
                localctx = gParser.LlistaNumerosContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 36
                self.list_()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return gParser.RULE_list

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class LlistaContext(ListContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.ListContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUM(self, i:int=None):
            if i is None:
                return self.getTokens(gParser.NUM)
            else:
                return self.getToken(gParser.NUM, i)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLlista" ):
                return visitor.visitLlista(self)
            else:
                return visitor.visitChildren(self)



    def list_(self):

        localctx = gParser.ListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_list)
        try:
            localctx = gParser.LlistaContext(self, localctx)
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self.match(gParser.NUM)
            self.state = 43
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 40
                    self.match(gParser.NUM) 
                self.state = 45
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return gParser.RULE_op

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class SumaContext(OpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.OpContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSuma" ):
                return visitor.visitSuma(self)
            else:
                return visitor.visitChildren(self)


    class PotenciaContext(OpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.OpContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPotencia" ):
                return visitor.visitPotencia(self)
            else:
                return visitor.visitChildren(self)


    class MultiplicacioContext(OpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.OpContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicacio" ):
                return visitor.visitMultiplicacio(self)
            else:
                return visitor.visitChildren(self)


    class ModulContext(OpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.OpContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModul" ):
                return visitor.visitModul(self)
            else:
                return visitor.visitChildren(self)


    class RestaContext(OpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.OpContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitResta" ):
                return visitor.visitResta(self)
            else:
                return visitor.visitChildren(self)


    class DivisioContext(OpContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a gParser.OpContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDivisio" ):
                return visitor.visitDivisio(self)
            else:
                return visitor.visitChildren(self)



    def op(self):

        localctx = gParser.OpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_op)
        try:
            self.state = 52
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                localctx = gParser.SumaContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 46
                self.match(gParser.T__3)
                pass
            elif token in [5]:
                localctx = gParser.RestaContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 47
                self.match(gParser.T__4)
                pass
            elif token in [6]:
                localctx = gParser.MultiplicacioContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 48
                self.match(gParser.T__5)
                pass
            elif token in [7]:
                localctx = gParser.DivisioContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 49
                self.match(gParser.T__6)
                pass
            elif token in [8]:
                localctx = gParser.ModulContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 50
                self.match(gParser.T__7)
                pass
            elif token in [9]:
                localctx = gParser.PotenciaContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 51
                self.match(gParser.T__8)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





