# Generated from E:/python/minecraft-datapack-language/antlr/McFuncDSL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .McFuncDSLParser import McFuncDSLParser
else:
    from McFuncDSLParser import McFuncDSLParser

# This class defines a complete listener for a parse tree produced by McFuncDSLParser.
class McFuncDSLListener(ParseTreeListener):

    # Enter a parse tree produced by McFuncDSLParser#program.
    def enterProgram(self, ctx:McFuncDSLParser.ProgramContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#program.
    def exitProgram(self, ctx:McFuncDSLParser.ProgramContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#includeStmt.
    def enterIncludeStmt(self, ctx:McFuncDSLParser.IncludeStmtContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#includeStmt.
    def exitIncludeStmt(self, ctx:McFuncDSLParser.IncludeStmtContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#annotation.
    def enterAnnotation(self, ctx:McFuncDSLParser.AnnotationContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#annotation.
    def exitAnnotation(self, ctx:McFuncDSLParser.AnnotationContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#classDecl.
    def enterClassDecl(self, ctx:McFuncDSLParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#classDecl.
    def exitClassDecl(self, ctx:McFuncDSLParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#interfaceDecl.
    def enterInterfaceDecl(self, ctx:McFuncDSLParser.InterfaceDeclContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#interfaceDecl.
    def exitInterfaceDecl(self, ctx:McFuncDSLParser.InterfaceDeclContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#interfaceMethodDecl.
    def enterInterfaceMethodDecl(self, ctx:McFuncDSLParser.InterfaceMethodDeclContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#interfaceMethodDecl.
    def exitInterfaceMethodDecl(self, ctx:McFuncDSLParser.InterfaceMethodDeclContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#type.
    def enterType(self, ctx:McFuncDSLParser.TypeContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#type.
    def exitType(self, ctx:McFuncDSLParser.TypeContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#typeList.
    def enterTypeList(self, ctx:McFuncDSLParser.TypeListContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#typeList.
    def exitTypeList(self, ctx:McFuncDSLParser.TypeListContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#primitiveType.
    def enterPrimitiveType(self, ctx:McFuncDSLParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#primitiveType.
    def exitPrimitiveType(self, ctx:McFuncDSLParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#functionDecl.
    def enterFunctionDecl(self, ctx:McFuncDSLParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#functionDecl.
    def exitFunctionDecl(self, ctx:McFuncDSLParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#methodDecl.
    def enterMethodDecl(self, ctx:McFuncDSLParser.MethodDeclContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#methodDecl.
    def exitMethodDecl(self, ctx:McFuncDSLParser.MethodDeclContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#paramList.
    def enterParamList(self, ctx:McFuncDSLParser.ParamListContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#paramList.
    def exitParamList(self, ctx:McFuncDSLParser.ParamListContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#paramDecl.
    def enterParamDecl(self, ctx:McFuncDSLParser.ParamDeclContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#paramDecl.
    def exitParamDecl(self, ctx:McFuncDSLParser.ParamDeclContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#block.
    def enterBlock(self, ctx:McFuncDSLParser.BlockContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#block.
    def exitBlock(self, ctx:McFuncDSLParser.BlockContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#statement.
    def enterStatement(self, ctx:McFuncDSLParser.StatementContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#statement.
    def exitStatement(self, ctx:McFuncDSLParser.StatementContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#breakStmt.
    def enterBreakStmt(self, ctx:McFuncDSLParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#breakStmt.
    def exitBreakStmt(self, ctx:McFuncDSLParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#continueStmt.
    def enterContinueStmt(self, ctx:McFuncDSLParser.ContinueStmtContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#continueStmt.
    def exitContinueStmt(self, ctx:McFuncDSLParser.ContinueStmtContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#forStmt.
    def enterForStmt(self, ctx:McFuncDSLParser.ForStmtContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#forStmt.
    def exitForStmt(self, ctx:McFuncDSLParser.ForStmtContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#forControl.
    def enterForControl(self, ctx:McFuncDSLParser.ForControlContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#forControl.
    def exitForControl(self, ctx:McFuncDSLParser.ForControlContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#whileStmt.
    def enterWhileStmt(self, ctx:McFuncDSLParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#whileStmt.
    def exitWhileStmt(self, ctx:McFuncDSLParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#constDecl.
    def enterConstDecl(self, ctx:McFuncDSLParser.ConstDeclContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#constDecl.
    def exitConstDecl(self, ctx:McFuncDSLParser.ConstDeclContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#varDeclaration.
    def enterVarDeclaration(self, ctx:McFuncDSLParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#varDeclaration.
    def exitVarDeclaration(self, ctx:McFuncDSLParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#varDecl.
    def enterVarDecl(self, ctx:McFuncDSLParser.VarDeclContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#varDecl.
    def exitVarDecl(self, ctx:McFuncDSLParser.VarDeclContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#forLoopVarDecl.
    def enterForLoopVarDecl(self, ctx:McFuncDSLParser.ForLoopVarDeclContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#forLoopVarDecl.
    def exitForLoopVarDecl(self, ctx:McFuncDSLParser.ForLoopVarDeclContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#assignment.
    def enterAssignment(self, ctx:McFuncDSLParser.AssignmentContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#assignment.
    def exitAssignment(self, ctx:McFuncDSLParser.AssignmentContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#returnStmt.
    def enterReturnStmt(self, ctx:McFuncDSLParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#returnStmt.
    def exitReturnStmt(self, ctx:McFuncDSLParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#ifStmt.
    def enterIfStmt(self, ctx:McFuncDSLParser.IfStmtContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#ifStmt.
    def exitIfStmt(self, ctx:McFuncDSLParser.IfStmtContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#LogicalOrExpr.
    def enterLogicalOrExpr(self, ctx:McFuncDSLParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#LogicalOrExpr.
    def exitLogicalOrExpr(self, ctx:McFuncDSLParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#DirectFuncCall.
    def enterDirectFuncCall(self, ctx:McFuncDSLParser.DirectFuncCallContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#DirectFuncCall.
    def exitDirectFuncCall(self, ctx:McFuncDSLParser.DirectFuncCallContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:McFuncDSLParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:McFuncDSLParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#MemberAccess.
    def enterMemberAccess(self, ctx:McFuncDSLParser.MemberAccessContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#MemberAccess.
    def exitMemberAccess(self, ctx:McFuncDSLParser.MemberAccessContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#CompareExpr.
    def enterCompareExpr(self, ctx:McFuncDSLParser.CompareExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#CompareExpr.
    def exitCompareExpr(self, ctx:McFuncDSLParser.CompareExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#NegExpr.
    def enterNegExpr(self, ctx:McFuncDSLParser.NegExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#NegExpr.
    def exitNegExpr(self, ctx:McFuncDSLParser.NegExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#LogicalNotExpr.
    def enterLogicalNotExpr(self, ctx:McFuncDSLParser.LogicalNotExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#LogicalNotExpr.
    def exitLogicalNotExpr(self, ctx:McFuncDSLParser.LogicalNotExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#PrimaryExpr.
    def enterPrimaryExpr(self, ctx:McFuncDSLParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#PrimaryExpr.
    def exitPrimaryExpr(self, ctx:McFuncDSLParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:McFuncDSLParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:McFuncDSLParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#LogicalAndExpr.
    def enterLogicalAndExpr(self, ctx:McFuncDSLParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#LogicalAndExpr.
    def exitLogicalAndExpr(self, ctx:McFuncDSLParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#MethodCall.
    def enterMethodCall(self, ctx:McFuncDSLParser.MethodCallContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#MethodCall.
    def exitMethodCall(self, ctx:McFuncDSLParser.MethodCallContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#VarExpr.
    def enterVarExpr(self, ctx:McFuncDSLParser.VarExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#VarExpr.
    def exitVarExpr(self, ctx:McFuncDSLParser.VarExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#LiteralExpr.
    def enterLiteralExpr(self, ctx:McFuncDSLParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#LiteralExpr.
    def exitLiteralExpr(self, ctx:McFuncDSLParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#ParenExpr.
    def enterParenExpr(self, ctx:McFuncDSLParser.ParenExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#ParenExpr.
    def exitParenExpr(self, ctx:McFuncDSLParser.ParenExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#NewObjectExpr.
    def enterNewObjectExpr(self, ctx:McFuncDSLParser.NewObjectExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#NewObjectExpr.
    def exitNewObjectExpr(self, ctx:McFuncDSLParser.NewObjectExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#TypeCastExpr.
    def enterTypeCastExpr(self, ctx:McFuncDSLParser.TypeCastExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#TypeCastExpr.
    def exitTypeCastExpr(self, ctx:McFuncDSLParser.TypeCastExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#commandExpr.
    def enterCommandExpr(self, ctx:McFuncDSLParser.CommandExprContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#commandExpr.
    def exitCommandExpr(self, ctx:McFuncDSLParser.CommandExprContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#argumentList.
    def enterArgumentList(self, ctx:McFuncDSLParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#argumentList.
    def exitArgumentList(self, ctx:McFuncDSLParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#exprList.
    def enterExprList(self, ctx:McFuncDSLParser.ExprListContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#exprList.
    def exitExprList(self, ctx:McFuncDSLParser.ExprListContext):
        pass


    # Enter a parse tree produced by McFuncDSLParser#literal.
    def enterLiteral(self, ctx:McFuncDSLParser.LiteralContext):
        pass

    # Exit a parse tree produced by McFuncDSLParser#literal.
    def exitLiteral(self, ctx:McFuncDSLParser.LiteralContext):
        pass



del McFuncDSLParser