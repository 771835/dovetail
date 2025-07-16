# Generated from E:/python/minecraft-datapack-language/antlr/transpiler.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .transpilerParser import transpilerParser
else:
    from transpilerParser import transpilerParser

# This class defines a complete listener for a parse tree produced by transpilerParser.
class transpilerListener(ParseTreeListener):

    # Enter a parse tree produced by transpilerParser#program.
    def enterProgram(self, ctx:transpilerParser.ProgramContext):
        pass

    # Exit a parse tree produced by transpilerParser#program.
    def exitProgram(self, ctx:transpilerParser.ProgramContext):
        pass


    # Enter a parse tree produced by transpilerParser#includeStmt.
    def enterIncludeStmt(self, ctx:transpilerParser.IncludeStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#includeStmt.
    def exitIncludeStmt(self, ctx:transpilerParser.IncludeStmtContext):
        pass


    # Enter a parse tree produced by transpilerParser#annotation.
    def enterAnnotation(self, ctx:transpilerParser.AnnotationContext):
        pass

    # Exit a parse tree produced by transpilerParser#annotation.
    def exitAnnotation(self, ctx:transpilerParser.AnnotationContext):
        pass


    # Enter a parse tree produced by transpilerParser#classDecl.
    def enterClassDecl(self, ctx:transpilerParser.ClassDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#classDecl.
    def exitClassDecl(self, ctx:transpilerParser.ClassDeclContext):
        pass


    # Enter a parse tree produced by transpilerParser#interfaceDecl.
    def enterInterfaceDecl(self, ctx:transpilerParser.InterfaceDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#interfaceDecl.
    def exitInterfaceDecl(self, ctx:transpilerParser.InterfaceDeclContext):
        pass


    # Enter a parse tree produced by transpilerParser#interfaceMethodDecl.
    def enterInterfaceMethodDecl(self, ctx:transpilerParser.InterfaceMethodDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#interfaceMethodDecl.
    def exitInterfaceMethodDecl(self, ctx:transpilerParser.InterfaceMethodDeclContext):
        pass


    # Enter a parse tree produced by transpilerParser#type.
    def enterType(self, ctx:transpilerParser.TypeContext):
        pass

    # Exit a parse tree produced by transpilerParser#type.
    def exitType(self, ctx:transpilerParser.TypeContext):
        pass


    # Enter a parse tree produced by transpilerParser#typeList.
    def enterTypeList(self, ctx:transpilerParser.TypeListContext):
        pass

    # Exit a parse tree produced by transpilerParser#typeList.
    def exitTypeList(self, ctx:transpilerParser.TypeListContext):
        pass


    # Enter a parse tree produced by transpilerParser#primitiveType.
    def enterPrimitiveType(self, ctx:transpilerParser.PrimitiveTypeContext):
        pass

    # Exit a parse tree produced by transpilerParser#primitiveType.
    def exitPrimitiveType(self, ctx:transpilerParser.PrimitiveTypeContext):
        pass


    # Enter a parse tree produced by transpilerParser#functionDecl.
    def enterFunctionDecl(self, ctx:transpilerParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#functionDecl.
    def exitFunctionDecl(self, ctx:transpilerParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by transpilerParser#methodDecl.
    def enterMethodDecl(self, ctx:transpilerParser.MethodDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#methodDecl.
    def exitMethodDecl(self, ctx:transpilerParser.MethodDeclContext):
        pass


    # Enter a parse tree produced by transpilerParser#paramList.
    def enterParamList(self, ctx:transpilerParser.ParamListContext):
        pass

    # Exit a parse tree produced by transpilerParser#paramList.
    def exitParamList(self, ctx:transpilerParser.ParamListContext):
        pass


    # Enter a parse tree produced by transpilerParser#paramDecl.
    def enterParamDecl(self, ctx:transpilerParser.ParamDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#paramDecl.
    def exitParamDecl(self, ctx:transpilerParser.ParamDeclContext):
        pass


    # Enter a parse tree produced by transpilerParser#block.
    def enterBlock(self, ctx:transpilerParser.BlockContext):
        pass

    # Exit a parse tree produced by transpilerParser#block.
    def exitBlock(self, ctx:transpilerParser.BlockContext):
        pass


    # Enter a parse tree produced by transpilerParser#statement.
    def enterStatement(self, ctx:transpilerParser.StatementContext):
        pass

    # Exit a parse tree produced by transpilerParser#statement.
    def exitStatement(self, ctx:transpilerParser.StatementContext):
        pass


    # Enter a parse tree produced by transpilerParser#breakStmt.
    def enterBreakStmt(self, ctx:transpilerParser.BreakStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#breakStmt.
    def exitBreakStmt(self, ctx:transpilerParser.BreakStmtContext):
        pass


    # Enter a parse tree produced by transpilerParser#continueStmt.
    def enterContinueStmt(self, ctx:transpilerParser.ContinueStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#continueStmt.
    def exitContinueStmt(self, ctx:transpilerParser.ContinueStmtContext):
        pass


    # Enter a parse tree produced by transpilerParser#forStmt.
    def enterForStmt(self, ctx:transpilerParser.ForStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#forStmt.
    def exitForStmt(self, ctx:transpilerParser.ForStmtContext):
        pass


    # Enter a parse tree produced by transpilerParser#forControl.
    def enterForControl(self, ctx:transpilerParser.ForControlContext):
        pass

    # Exit a parse tree produced by transpilerParser#forControl.
    def exitForControl(self, ctx:transpilerParser.ForControlContext):
        pass


    # Enter a parse tree produced by transpilerParser#whileStmt.
    def enterWhileStmt(self, ctx:transpilerParser.WhileStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#whileStmt.
    def exitWhileStmt(self, ctx:transpilerParser.WhileStmtContext):
        pass


    # Enter a parse tree produced by transpilerParser#constDecl.
    def enterConstDecl(self, ctx:transpilerParser.ConstDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#constDecl.
    def exitConstDecl(self, ctx:transpilerParser.ConstDeclContext):
        pass


    # Enter a parse tree produced by transpilerParser#varDeclaration.
    def enterVarDeclaration(self, ctx:transpilerParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by transpilerParser#varDeclaration.
    def exitVarDeclaration(self, ctx:transpilerParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by transpilerParser#varDecl.
    def enterVarDecl(self, ctx:transpilerParser.VarDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#varDecl.
    def exitVarDecl(self, ctx:transpilerParser.VarDeclContext):
        pass


    # Enter a parse tree produced by transpilerParser#forLoopVarDecl.
    def enterForLoopVarDecl(self, ctx:transpilerParser.ForLoopVarDeclContext):
        pass

    # Exit a parse tree produced by transpilerParser#forLoopVarDecl.
    def exitForLoopVarDecl(self, ctx:transpilerParser.ForLoopVarDeclContext):
        pass


    # Enter a parse tree produced by transpilerParser#assignment.
    def enterAssignment(self, ctx:transpilerParser.AssignmentContext):
        pass

    # Exit a parse tree produced by transpilerParser#assignment.
    def exitAssignment(self, ctx:transpilerParser.AssignmentContext):
        pass


    # Enter a parse tree produced by transpilerParser#returnStmt.
    def enterReturnStmt(self, ctx:transpilerParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#returnStmt.
    def exitReturnStmt(self, ctx:transpilerParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by transpilerParser#ifStmt.
    def enterIfStmt(self, ctx:transpilerParser.IfStmtContext):
        pass

    # Exit a parse tree produced by transpilerParser#ifStmt.
    def exitIfStmt(self, ctx:transpilerParser.IfStmtContext):
        pass


    # Enter a parse tree produced by transpilerParser#LogicalOrExpr.
    def enterLogicalOrExpr(self, ctx:transpilerParser.LogicalOrExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#LogicalOrExpr.
    def exitLogicalOrExpr(self, ctx:transpilerParser.LogicalOrExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#DirectFuncCall.
    def enterDirectFuncCall(self, ctx:transpilerParser.DirectFuncCallContext):
        pass

    # Exit a parse tree produced by transpilerParser#DirectFuncCall.
    def exitDirectFuncCall(self, ctx:transpilerParser.DirectFuncCallContext):
        pass


    # Enter a parse tree produced by transpilerParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:transpilerParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:transpilerParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#MemberAccess.
    def enterMemberAccess(self, ctx:transpilerParser.MemberAccessContext):
        pass

    # Exit a parse tree produced by transpilerParser#MemberAccess.
    def exitMemberAccess(self, ctx:transpilerParser.MemberAccessContext):
        pass


    # Enter a parse tree produced by transpilerParser#CompareExpr.
    def enterCompareExpr(self, ctx:transpilerParser.CompareExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#CompareExpr.
    def exitCompareExpr(self, ctx:transpilerParser.CompareExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#NegExpr.
    def enterNegExpr(self, ctx:transpilerParser.NegExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#NegExpr.
    def exitNegExpr(self, ctx:transpilerParser.NegExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#LogicalNotExpr.
    def enterLogicalNotExpr(self, ctx:transpilerParser.LogicalNotExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#LogicalNotExpr.
    def exitLogicalNotExpr(self, ctx:transpilerParser.LogicalNotExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#PrimaryExpr.
    def enterPrimaryExpr(self, ctx:transpilerParser.PrimaryExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#PrimaryExpr.
    def exitPrimaryExpr(self, ctx:transpilerParser.PrimaryExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:transpilerParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:transpilerParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#LogicalAndExpr.
    def enterLogicalAndExpr(self, ctx:transpilerParser.LogicalAndExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#LogicalAndExpr.
    def exitLogicalAndExpr(self, ctx:transpilerParser.LogicalAndExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#MethodCall.
    def enterMethodCall(self, ctx:transpilerParser.MethodCallContext):
        pass

    # Exit a parse tree produced by transpilerParser#MethodCall.
    def exitMethodCall(self, ctx:transpilerParser.MethodCallContext):
        pass


    # Enter a parse tree produced by transpilerParser#VarExpr.
    def enterVarExpr(self, ctx:transpilerParser.VarExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#VarExpr.
    def exitVarExpr(self, ctx:transpilerParser.VarExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#LiteralExpr.
    def enterLiteralExpr(self, ctx:transpilerParser.LiteralExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#LiteralExpr.
    def exitLiteralExpr(self, ctx:transpilerParser.LiteralExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#ParenExpr.
    def enterParenExpr(self, ctx:transpilerParser.ParenExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#ParenExpr.
    def exitParenExpr(self, ctx:transpilerParser.ParenExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#NewObjectExpr.
    def enterNewObjectExpr(self, ctx:transpilerParser.NewObjectExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#NewObjectExpr.
    def exitNewObjectExpr(self, ctx:transpilerParser.NewObjectExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#TypeCastExpr.
    def enterTypeCastExpr(self, ctx:transpilerParser.TypeCastExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#TypeCastExpr.
    def exitTypeCastExpr(self, ctx:transpilerParser.TypeCastExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#commandExpr.
    def enterCommandExpr(self, ctx:transpilerParser.CommandExprContext):
        pass

    # Exit a parse tree produced by transpilerParser#commandExpr.
    def exitCommandExpr(self, ctx:transpilerParser.CommandExprContext):
        pass


    # Enter a parse tree produced by transpilerParser#argumentList.
    def enterArgumentList(self, ctx:transpilerParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by transpilerParser#argumentList.
    def exitArgumentList(self, ctx:transpilerParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by transpilerParser#exprList.
    def enterExprList(self, ctx:transpilerParser.ExprListContext):
        pass

    # Exit a parse tree produced by transpilerParser#exprList.
    def exitExprList(self, ctx:transpilerParser.ExprListContext):
        pass


    # Enter a parse tree produced by transpilerParser#literal.
    def enterLiteral(self, ctx:transpilerParser.LiteralContext):
        pass

    # Exit a parse tree produced by transpilerParser#literal.
    def exitLiteral(self, ctx:transpilerParser.LiteralContext):
        pass



del transpilerParser