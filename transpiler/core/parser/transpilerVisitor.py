# Generated from E:/python/minecraft-datapack-language/antlr/transpiler.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .transpilerParser import transpilerParser
else:
    from transpilerParser import transpilerParser

# This class defines a complete generic visitor for a parse tree produced by transpilerParser.

class transpilerVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by transpilerParser#program.
    def visitProgram(self, ctx:transpilerParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#includeStmt.
    def visitIncludeStmt(self, ctx:transpilerParser.IncludeStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#annotation.
    def visitAnnotation(self, ctx:transpilerParser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#classDecl.
    def visitClassDecl(self, ctx:transpilerParser.ClassDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#interfaceDecl.
    def visitInterfaceDecl(self, ctx:transpilerParser.InterfaceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#type.
    def visitType(self, ctx:transpilerParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#functionDecl.
    def visitFunctionDecl(self, ctx:transpilerParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#methodDecl.
    def visitMethodDecl(self, ctx:transpilerParser.MethodDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#paramList.
    def visitParamList(self, ctx:transpilerParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#paramDecl.
    def visitParamDecl(self, ctx:transpilerParser.ParamDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#block.
    def visitBlock(self, ctx:transpilerParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#statement.
    def visitStatement(self, ctx:transpilerParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#breakStmt.
    def visitBreakStmt(self, ctx:transpilerParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#continueStmt.
    def visitContinueStmt(self, ctx:transpilerParser.ContinueStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#forStmt.
    def visitForStmt(self, ctx:transpilerParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#forControl.
    def visitForControl(self, ctx:transpilerParser.ForControlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#forInit.
    def visitForInit(self, ctx:transpilerParser.ForInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#forCondition.
    def visitForCondition(self, ctx:transpilerParser.ForConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#forUpdate.
    def visitForUpdate(self, ctx:transpilerParser.ForUpdateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#whileStmt.
    def visitWhileStmt(self, ctx:transpilerParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#constDecl.
    def visitConstDecl(self, ctx:transpilerParser.ConstDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#varDeclaration.
    def visitVarDeclaration(self, ctx:transpilerParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#varDecl.
    def visitVarDecl(self, ctx:transpilerParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#forLoopVarDecl.
    def visitForLoopVarDecl(self, ctx:transpilerParser.ForLoopVarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#returnStmt.
    def visitReturnStmt(self, ctx:transpilerParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#ifStmt.
    def visitIfStmt(self, ctx:transpilerParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#TermExpr.
    def visitTermExpr(self, ctx:transpilerParser.TermExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#NegExpr.
    def visitNegExpr(self, ctx:transpilerParser.NegExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#LogicalNotExpr.
    def visitLogicalNotExpr(self, ctx:transpilerParser.LogicalNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#MemberAssignmentExpr.
    def visitMemberAssignmentExpr(self, ctx:transpilerParser.MemberAssignmentExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#LocalAssignmentExpr.
    def visitLocalAssignmentExpr(self, ctx:transpilerParser.LocalAssignmentExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#LogicalAndExpr.
    def visitLogicalAndExpr(self, ctx:transpilerParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#MethodCall.
    def visitMethodCall(self, ctx:transpilerParser.MethodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#LogicalOrExpr.
    def visitLogicalOrExpr(self, ctx:transpilerParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#ArrayAccess.
    def visitArrayAccess(self, ctx:transpilerParser.ArrayAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#MemberAccess.
    def visitMemberAccess(self, ctx:transpilerParser.MemberAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#CompareExpr.
    def visitCompareExpr(self, ctx:transpilerParser.CompareExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#PrimaryExpr.
    def visitPrimaryExpr(self, ctx:transpilerParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#FunctionCall.
    def visitFunctionCall(self, ctx:transpilerParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#FactorExpr.
    def visitFactorExpr(self, ctx:transpilerParser.FactorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#IdentifierExpr.
    def visitIdentifierExpr(self, ctx:transpilerParser.IdentifierExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#LiteralExpr.
    def visitLiteralExpr(self, ctx:transpilerParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#ParenExpr.
    def visitParenExpr(self, ctx:transpilerParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#argumentList.
    def visitArgumentList(self, ctx:transpilerParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#exprList.
    def visitExprList(self, ctx:transpilerParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by transpilerParser#literal.
    def visitLiteral(self, ctx:transpilerParser.LiteralContext):
        return self.visitChildren(ctx)



del transpilerParser