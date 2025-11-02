# coding=utf-8
# Generated from E:/python/minecraft-datapack-language/antlr/transpiler.g4 by ANTLR 4.13.2
from antlr4 import *

if "." in __name__:
    from .transpilerParser import transpilerParser
else:
    from transpilerParser import transpilerParser


# This class defines a complete listener for a parse tree produced by transpilerParser.
class transpilerListener(ParseTreeListener):

    # Enter a parse tree produced by transpilerParser#program.
    def enterProgram(self, ctx: transpilerParser.ProgramContext):
        pass

    # Exit a parse tree produced by transpilerParser#program.
    def exitProgram(self, ctx: transpilerParser.ProgramContext):
        pass

    # Enter a parse tree produced by transpilerParser#includeStmt.
    def enterIncludeStmt(self, ctx: transpilerParser.IncludeStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#includeStmt.
    def exitIncludeStmt(self, ctx: transpilerParser.IncludeStmtContext):
        pass

    # Enter a parse tree produced by transpilerParser#annotation.
    def enterAnnotation(self, ctx: transpilerParser.AnnotationContext):
        pass

    # Exit a parse tree produced by transpilerParser#annotation.
    def exitAnnotation(self, ctx: transpilerParser.AnnotationContext):
        pass

    # Enter a parse tree produced by transpilerParser#classDecl.
    def enterClassDecl(self, ctx: transpilerParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#classDecl.
    def exitClassDecl(self, ctx: transpilerParser.ClassDeclContext):
        pass

    # Enter a parse tree produced by transpilerParser#interfaceDecl.
    def enterInterfaceDecl(self, ctx: transpilerParser.InterfaceDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#interfaceDecl.
    def exitInterfaceDecl(self, ctx: transpilerParser.InterfaceDeclContext):
        pass

    # Enter a parse tree produced by transpilerParser#classPropertyDecl.
    def enterClassPropertyDecl(self, ctx: transpilerParser.ClassPropertyDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#classPropertyDecl.
    def exitClassPropertyDecl(self, ctx: transpilerParser.ClassPropertyDeclContext):
        pass

    # Enter a parse tree produced by transpilerParser#type.
    def enterType(self, ctx: transpilerParser.TypeContext):
        pass

    # Exit a parse tree produced by transpilerParser#type.
    def exitType(self, ctx: transpilerParser.TypeContext):
        pass

    # Enter a parse tree produced by transpilerParser#functionDecl.
    def enterFunctionDecl(self, ctx: transpilerParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#functionDecl.
    def exitFunctionDecl(self, ctx: transpilerParser.FunctionDeclContext):
        pass

    # Enter a parse tree produced by transpilerParser#methodDecl.
    def enterMethodDecl(self, ctx: transpilerParser.MethodDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#methodDecl.
    def exitMethodDecl(self, ctx: transpilerParser.MethodDeclContext):
        pass

    # Enter a parse tree produced by transpilerParser#paramList.
    def enterParamList(self, ctx: transpilerParser.ParamListContext):
        pass

    # Exit a parse tree produced by transpilerParser#paramList.
    def exitParamList(self, ctx: transpilerParser.ParamListContext):
        pass

    # Enter a parse tree produced by transpilerParser#paramDecl.
    def enterParamDecl(self, ctx: transpilerParser.ParamDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#paramDecl.
    def exitParamDecl(self, ctx: transpilerParser.ParamDeclContext):
        pass

    # Enter a parse tree produced by transpilerParser#block.
    def enterBlock(self, ctx: transpilerParser.BlockContext):
        pass

    # Exit a parse tree produced by transpilerParser#block.
    def exitBlock(self, ctx: transpilerParser.BlockContext):
        pass

    # Enter a parse tree produced by transpilerParser#statement.
    def enterStatement(self, ctx: transpilerParser.StatementContext):
        pass

    # Exit a parse tree produced by transpilerParser#statement.
    def exitStatement(self, ctx: transpilerParser.StatementContext):
        pass

    # Enter a parse tree produced by transpilerParser#breakStmt.
    def enterBreakStmt(self, ctx: transpilerParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#breakStmt.
    def exitBreakStmt(self, ctx: transpilerParser.BreakStmtContext):
        pass

    # Enter a parse tree produced by transpilerParser#continueStmt.
    def enterContinueStmt(self, ctx: transpilerParser.ContinueStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#continueStmt.
    def exitContinueStmt(self, ctx: transpilerParser.ContinueStmtContext):
        pass

    # Enter a parse tree produced by transpilerParser#forStmt.
    def enterForStmt(self, ctx: transpilerParser.ForStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#forStmt.
    def exitForStmt(self, ctx: transpilerParser.ForStmtContext):
        pass

    # Enter a parse tree produced by transpilerParser#forControl.
    def enterForControl(self, ctx: transpilerParser.ForControlContext):
        pass

    # Exit a parse tree produced by transpilerParser#forControl.
    def exitForControl(self, ctx: transpilerParser.ForControlContext):
        pass

    # Enter a parse tree produced by transpilerParser#forInit.
    def enterForInit(self, ctx: transpilerParser.ForInitContext):
        pass

    # Exit a parse tree produced by transpilerParser#forInit.
    def exitForInit(self, ctx: transpilerParser.ForInitContext):
        pass

    # Enter a parse tree produced by transpilerParser#condition.
    def enterCondition(self, ctx: transpilerParser.ConditionContext):
        pass

    # Exit a parse tree produced by transpilerParser#condition.
    def exitCondition(self, ctx: transpilerParser.ConditionContext):
        pass

    # Enter a parse tree produced by transpilerParser#forUpdate.
    def enterForUpdate(self, ctx: transpilerParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by transpilerParser#forUpdate.
    def exitForUpdate(self, ctx: transpilerParser.ForUpdateContext):
        pass

    # Enter a parse tree produced by transpilerParser#whileStmt.
    def enterWhileStmt(self, ctx: transpilerParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#whileStmt.
    def exitWhileStmt(self, ctx: transpilerParser.WhileStmtContext):
        pass

    # Enter a parse tree produced by transpilerParser#constDecl.
    def enterConstDecl(self, ctx: transpilerParser.ConstDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#constDecl.
    def exitConstDecl(self, ctx: transpilerParser.ConstDeclContext):
        pass

    # Enter a parse tree produced by transpilerParser#varDecl.
    def enterVarDecl(self, ctx: transpilerParser.VarDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#varDecl.
    def exitVarDecl(self, ctx: transpilerParser.VarDeclContext):
        pass

    # Enter a parse tree produced by transpilerParser#returnStmt.
    def enterReturnStmt(self, ctx: transpilerParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#returnStmt.
    def exitReturnStmt(self, ctx: transpilerParser.ReturnStmtContext):
        pass

    # Enter a parse tree produced by transpilerParser#ifStmt.
    def enterIfStmt(self, ctx: transpilerParser.IfStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#ifStmt.
    def exitIfStmt(self, ctx: transpilerParser.IfStmtContext):
        pass

    # Enter a parse tree produced by transpilerParser#TermExpr.
    def enterTermExpr(self, ctx: transpilerParser.TermExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#TermExpr.
    def exitTermExpr(self, ctx: transpilerParser.TermExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#NegExpr.
    def enterNegExpr(self, ctx: transpilerParser.NegExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#NegExpr.
    def exitNegExpr(self, ctx: transpilerParser.NegExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#LogicalNotExpr.
    def enterLogicalNotExpr(self, ctx: transpilerParser.LogicalNotExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#LogicalNotExpr.
    def exitLogicalNotExpr(self, ctx: transpilerParser.LogicalNotExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#MemberAssignmentExpr.
    def enterMemberAssignmentExpr(self, ctx: transpilerParser.MemberAssignmentExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#MemberAssignmentExpr.
    def exitMemberAssignmentExpr(self, ctx: transpilerParser.MemberAssignmentExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#LocalAssignmentExpr.
    def enterLocalAssignmentExpr(self, ctx: transpilerParser.LocalAssignmentExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#LocalAssignmentExpr.
    def exitLocalAssignmentExpr(self, ctx: transpilerParser.LocalAssignmentExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#LogicalAndExpr.
    def enterLogicalAndExpr(self, ctx: transpilerParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#LogicalAndExpr.
    def exitLogicalAndExpr(self, ctx: transpilerParser.LogicalAndExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#MethodCall.
    def enterMethodCall(self, ctx: transpilerParser.MethodCallContext):
        pass

    # Exit a parse tree produced by transpilerParser#MethodCall.
    def exitMethodCall(self, ctx: transpilerParser.MethodCallContext):
        pass

    # Enter a parse tree produced by transpilerParser#LogicalOrExpr.
    def enterLogicalOrExpr(self, ctx: transpilerParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#LogicalOrExpr.
    def exitLogicalOrExpr(self, ctx: transpilerParser.LogicalOrExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#ArrayAccess.
    def enterArrayAccess(self, ctx: transpilerParser.ArrayAccessContext):
        pass

    # Exit a parse tree produced by transpilerParser#ArrayAccess.
    def exitArrayAccess(self, ctx: transpilerParser.ArrayAccessContext):
        pass

    # Enter a parse tree produced by transpilerParser#MemberAccess.
    def enterMemberAccess(self, ctx: transpilerParser.MemberAccessContext):
        pass

    # Exit a parse tree produced by transpilerParser#MemberAccess.
    def exitMemberAccess(self, ctx: transpilerParser.MemberAccessContext):
        pass

    # Enter a parse tree produced by transpilerParser#CompareExpr.
    def enterCompareExpr(self, ctx: transpilerParser.CompareExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#CompareExpr.
    def exitCompareExpr(self, ctx: transpilerParser.CompareExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#TernaryPythonicExpr.
    def enterTernaryPythonicExpr(self, ctx: transpilerParser.TernaryPythonicExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#TernaryPythonicExpr.
    def exitTernaryPythonicExpr(self, ctx: transpilerParser.TernaryPythonicExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#PrimaryExpr.
    def enterPrimaryExpr(self, ctx: transpilerParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#PrimaryExpr.
    def exitPrimaryExpr(self, ctx: transpilerParser.PrimaryExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#ArrayAssignmentExpr.
    def enterArrayAssignmentExpr(self, ctx: transpilerParser.ArrayAssignmentExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#ArrayAssignmentExpr.
    def exitArrayAssignmentExpr(self, ctx: transpilerParser.ArrayAssignmentExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#TernaryTraditionalExpr.
    def enterTernaryTraditionalExpr(self, ctx: transpilerParser.TernaryTraditionalExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#TernaryTraditionalExpr.
    def exitTernaryTraditionalExpr(self, ctx: transpilerParser.TernaryTraditionalExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#FunctionCall.
    def enterFunctionCall(self, ctx: transpilerParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by transpilerParser#FunctionCall.
    def exitFunctionCall(self, ctx: transpilerParser.FunctionCallContext):
        pass

    # Enter a parse tree produced by transpilerParser#FactorExpr.
    def enterFactorExpr(self, ctx: transpilerParser.FactorExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#FactorExpr.
    def exitFactorExpr(self, ctx: transpilerParser.FactorExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#IdentifierExpr.
    def enterIdentifierExpr(self, ctx: transpilerParser.IdentifierExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#IdentifierExpr.
    def exitIdentifierExpr(self, ctx: transpilerParser.IdentifierExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#LiteralExpr.
    def enterLiteralExpr(self, ctx: transpilerParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#LiteralExpr.
    def exitLiteralExpr(self, ctx: transpilerParser.LiteralExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#ParenExpr.
    def enterParenExpr(self, ctx: transpilerParser.ParenExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#ParenExpr.
    def exitParenExpr(self, ctx: transpilerParser.ParenExprContext):
        pass

    # Enter a parse tree produced by transpilerParser#argumentList.
    def enterArgumentList(self, ctx: transpilerParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by transpilerParser#argumentList.
    def exitArgumentList(self, ctx: transpilerParser.ArgumentListContext):
        pass

    # Enter a parse tree produced by transpilerParser#exprList.
    def enterExprList(self, ctx: transpilerParser.ExprListContext):
        pass

    # Exit a parse tree produced by transpilerParser#exprList.
    def exitExprList(self, ctx: transpilerParser.ExprListContext):
        pass

    # Enter a parse tree produced by transpilerParser#literal.
    def enterLiteral(self, ctx: transpilerParser.LiteralContext):
        pass

    # Exit a parse tree produced by transpilerParser#literal.
    def exitLiteral(self, ctx: transpilerParser.LiteralContext):
        pass


del transpilerParser
