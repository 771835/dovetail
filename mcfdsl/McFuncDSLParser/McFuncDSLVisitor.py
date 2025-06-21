# Generated from E:/python/minecraft-datapack-language/antlr/McFuncDSL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .McFuncDSLParser import McFuncDSLParser
else:
    from McFuncDSLParser import McFuncDSLParser

# This class defines a complete generic visitor for a parse tree produced by McFuncDSLParser.

class McFuncDSLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by McFuncDSLParser#program.
    def visitProgram(self, ctx:McFuncDSLParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#importStmt.
    def visitImportStmt(self, ctx:McFuncDSLParser.ImportStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#annotation.
    def visitAnnotation(self, ctx:McFuncDSLParser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#classDecl.
    def visitClassDecl(self, ctx:McFuncDSLParser.ClassDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#interfaceDecl.
    def visitInterfaceDecl(self, ctx:McFuncDSLParser.InterfaceDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#interfaceMethodDecl.
    def visitInterfaceMethodDecl(self, ctx:McFuncDSLParser.InterfaceMethodDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#type.
    def visitType(self, ctx:McFuncDSLParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#typeList.
    def visitTypeList(self, ctx:McFuncDSLParser.TypeListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#primitiveType.
    def visitPrimitiveType(self, ctx:McFuncDSLParser.PrimitiveTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#functionDecl.
    def visitFunctionDecl(self, ctx:McFuncDSLParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#methodDecl.
    def visitMethodDecl(self, ctx:McFuncDSLParser.MethodDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#paramList.
    def visitParamList(self, ctx:McFuncDSLParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#paramDecl.
    def visitParamDecl(self, ctx:McFuncDSLParser.ParamDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#block.
    def visitBlock(self, ctx:McFuncDSLParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#statement.
    def visitStatement(self, ctx:McFuncDSLParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#forStmt.
    def visitForStmt(self, ctx:McFuncDSLParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#forControl.
    def visitForControl(self, ctx:McFuncDSLParser.ForControlContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#whileStmt.
    def visitWhileStmt(self, ctx:McFuncDSLParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#constDecl.
    def visitConstDecl(self, ctx:McFuncDSLParser.ConstDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#varDeclaration.
    def visitVarDeclaration(self, ctx:McFuncDSLParser.VarDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#varDecl.
    def visitVarDecl(self, ctx:McFuncDSLParser.VarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#forLoopVarDecl.
    def visitForLoopVarDecl(self, ctx:McFuncDSLParser.ForLoopVarDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#assignment.
    def visitAssignment(self, ctx:McFuncDSLParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#returnStmt.
    def visitReturnStmt(self, ctx:McFuncDSLParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#ifStmt.
    def visitIfStmt(self, ctx:McFuncDSLParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#LogicalOrExpr.
    def visitLogicalOrExpr(self, ctx:McFuncDSLParser.LogicalOrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#DirectFuncCall.
    def visitDirectFuncCall(self, ctx:McFuncDSLParser.DirectFuncCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#MulDivExpr.
    def visitMulDivExpr(self, ctx:McFuncDSLParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#MemberAccess.
    def visitMemberAccess(self, ctx:McFuncDSLParser.MemberAccessContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#CompareExpr.
    def visitCompareExpr(self, ctx:McFuncDSLParser.CompareExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#NegExpr.
    def visitNegExpr(self, ctx:McFuncDSLParser.NegExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#LogicalNotExpr.
    def visitLogicalNotExpr(self, ctx:McFuncDSLParser.LogicalNotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#PrimaryExpr.
    def visitPrimaryExpr(self, ctx:McFuncDSLParser.PrimaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:McFuncDSLParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#LogicalAndExpr.
    def visitLogicalAndExpr(self, ctx:McFuncDSLParser.LogicalAndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#MethodCall.
    def visitMethodCall(self, ctx:McFuncDSLParser.MethodCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#NewSelectorExpr.
    def visitNewSelectorExpr(self, ctx:McFuncDSLParser.NewSelectorExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#VarExpr.
    def visitVarExpr(self, ctx:McFuncDSLParser.VarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#LiteralExpr.
    def visitLiteralExpr(self, ctx:McFuncDSLParser.LiteralExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#ParenExpr.
    def visitParenExpr(self, ctx:McFuncDSLParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#NewObjectExpr.
    def visitNewObjectExpr(self, ctx:McFuncDSLParser.NewObjectExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#TypeCastExpr.
    def visitTypeCastExpr(self, ctx:McFuncDSLParser.TypeCastExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#cmdExpr.
    def visitCmdExpr(self, ctx:McFuncDSLParser.CmdExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#cmdBlockExpr.
    def visitCmdBlockExpr(self, ctx:McFuncDSLParser.CmdBlockExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#argumentList.
    def visitArgumentList(self, ctx:McFuncDSLParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#exprList.
    def visitExprList(self, ctx:McFuncDSLParser.ExprListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by McFuncDSLParser#literal.
    def visitLiteral(self, ctx:McFuncDSLParser.LiteralContext):
        return self.visitChildren(ctx)



del McFuncDSLParser