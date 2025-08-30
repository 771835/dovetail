grammar transpiler;

/* 程序结构 */
program
    : (includeStmt)*
      (classDecl
      | interfaceDecl
      | functionDecl
      | varDecl SEMI?
      | constDecl SEMI?)* EOF
    ;

includeStmt
    : INCLUDE literal SEMI?             // 包含库文件，如：include "mathlib.mcdl";
    ;

/* 2. 注解系统 */

annotation
    : '@' ID     // 仅允许使用预定义注解
    ;

/* 3. 类系统 */
classDecl
    : annotation* CLASS ID
      (EXTENDS type)?                      // 单继承
      (IMPLEMENTS type)?               // 单接口实现
      LBRACE // 构造函数为__init__
        (varDecl SEMI?
        | constDecl SEMI?
        | methodDecl 
        )*

      RBRACE
    ;

interfaceDecl
    : annotation* INTERFACE ID
      (EXTENDS type)?                  // 接口单继承
      LBRACE 
        (methodDecl)*
      RBRACE
    ;



/* 4. 类型系统(阉割版) */
type
    : ID // ('[' (type ',')* ']')?
    | NULL
    ;

functionDecl
    : annotation* FUNC ID paramList ((ARROW | COLON) type)? block // 返回类型标注
    | annotation* FUNC type? ID paramList block
    ;


methodDecl
    : annotation* METHOD ID paramList ((ARROW | COLON) type)? block
    | annotation* METHOD type? ID paramList block
    ;

paramList
    : LPAREN (paramDecl (COMMA paramDecl)*)? RPAREN
    | PAREN
    ;

paramDecl
    : ID (ARROW | COLON) type (ASSIGN expr)?   // 强制类型标注
    | type ID (ASSIGN expr)?
    ;


block
    : statement // 单条语句
    | LBRACE statement* RBRACE              // 代码块，包含多个语句
    | SEMI // 空的代码块
    ;


/* 6. 流程控制 */
statement
    : functionDecl                         // 函数定义
    | varDecl SEMI?                        // 变量声明
    | constDecl SEMI?                      // 常量声明
    | forStmt                              // for循环
    | whileStmt                            // while循环
    | expr SEMI?                           // 表达式语句
    | returnStmt SEMI?                     // 返回
    | ifStmt                               // 条件语句
    | breakStmt SEMI?                      // break语句
    | continueStmt SEMI?                   // continue语句
    | SEMI                                 // 分号
    ;

breakStmt
    : BREAK
    ;

continueStmt
    : CONTINUE
    ;

forStmt
    : FOR LPAREN forControl RPAREN block        // 传统for循环
    | FOR LPAREN type ID COLON expr RPAREN block       // 增强for循环 (expr需为可迭代class)
    ;


forControl
    : forInit? SEMI condition? SEMI forUpdate?
    ;


forInit
    : varDecl
    | expr
    ;

condition
    : expr
    ;

forUpdate
    : expr
    ;


whileStmt
    : WHILE LPAREN condition RPAREN block            // while循环
    ;

constDecl
    : CONST ID ((ARROW | COLON) type)? ('?')? (ASSIGN expr)  // 常量声明
    | CONST type ID (ASSIGN expr)
    ;

// 变量声明
varDecl
    : LET ID ('?')? ASSIGN expr
    | ID (ARROW | COLON) type ('?')? (ASSIGN expr)?
    | type ID ('?')? (ASSIGN expr)? // 更符合大多数人习惯的变量声明
    | LET ID ('?')? (ARROW | COLON) type ASSIGN expr
    ;


returnStmt
    : RETURN expr?                  // 返回语句，如：return result;
    ;

ifStmt
    : IF LPAREN condition RPAREN block (ELSE block)?  // 条件语句
    ;


/* 表达式系统 */
expr
    :primary                               # PrimaryExpr        // 基础表达式

    //| lambdaExpr                            # LambdaExpression   // Lambda
    //| methodReference                       # MethodRefExpr      // 方法引用
    //| expr '?' '.' ID                       # SafeNavigation     // 安全导航
    | expr '.' ID argumentList         # MethodCall         // 方法调用
    | expr '.' ID                           # MemberAccess       // 成员访问
    | expr LBRACK expr RBRACK                     # ArrayAccess        // 数组访问
    | expr argumentList                # FunctionCall       // 函数调用

    | SUB expr                              # NegExpr            // 负号
    | NOT expr                         #LogicalNotExpr             // not运算符

    | expr (MUL|DIV|MOD) expr                   # FactorExpr         // 算术运算
    | expr (ADD|SUB) expr                   # TermExpr

    | expr (GT | LT | EQ | NEQ | LTE | GTE) expr # CompareExpr      // 比较运算

    | expr AND expr                   #LogicalAndExpr             // and运算符
    | expr OR expr                   #LogicalOrExpr              // or运算符

    | <assoc=right> expr QUESTION expr COLON expr  # TernaryTraditionalExpr
    | <assoc=right> expr IF expr ELSE expr  # TernaryPythonicExpr

    | expr LBRACK expr RBRACK ASSIGN expr           # ArrayAssignmentExpr
    | expr '.' ID ASSIGN expr           # MemberAssignmentExpr
    | ID ASSIGN expr                    # LocalAssignmentExpr
    ;


primary
    :ID                                    # IdentifierExpr      // 标识符（变量、函数、类等）
    | literal                               # LiteralExpr        // 字面量
    | LPAREN expr RPAREN                          # ParenExpr          // 括号
    ;


/* 辅助规则 */

argumentList
    : LPAREN exprList? RPAREN
    | PAREN
    ;

exprList
    : expr (COMMA expr)*                      // 表达式列表
    ;

literal
    : NUMBER                                // 数字
    | STRING                                // 普通字符串
    | FSTRING                               // 插值字符串
    | TRUE | FALSE                      // 布尔值
    | NULL                                // 空值
    ;

// 词法规则

// 分隔符（定义在ID之前）
PAREN : '()';
LPAREN : '(';
RPAREN : ')';
LBRACK : '[';
RBRACK : ']';
LBRACE : '{';
RBRACE : '}';
SEMI : ';';
COMMA : ',';
QUESTION : '?';
ARROW: '->'
    | 'fuck'
    | 'as'
    ;
COLON : ':';

DOUBLE_COLON: '::';

// 关键字
INCLUDE: 'include';
FUNC: 'func';
METHOD: 'method';
CLASS: 'class';
INTERFACE: 'interface';
EXTENDS: 'extends';
IMPLEMENTS: 'implements';
CONST: 'const';
LET: 'let';
RETURN: 'return';
FOR: 'for';
WHILE: 'while';
IF: 'if';
ELSE: 'else';
NEW: 'new';
TRUE: 'true';
FALSE: 'false';
NULL: 'null';
IN: 'in';
BREAK: 'break';
CONTINUE: 'continue';




// 运算符
NOT : '!'
    | 'not'
    ;
MUL : '*';
DIV : '/';
MOD : '%';
ADD : '+';
SUB : '-';
GT  : '>';
LT  : '<';
EQ  : '==';
NEQ : '!=';
GTE : '>=';
LTE : '<=';
AND : '&&'
    | 'and'
    ;
OR  : '||'
    | 'or'
    ;
ASSIGN : '=';


// 数字
NUMBER: [0-9]+ ('.' [0-9]+)?;

// 字符串
STRING: '"' ( ESC | SAFE_CHAR )* '"';
FSTRING: 'f"' ( '\\' [\\"] | ~["\\$] | '${' )* '"' ; // 合并处理插值

// 转义字符（修正版）
fragment ESC: '\\' [btnfr"\\$];  // 正确转义字符集
fragment SAFE_CHAR: ~["\\\r\n];  // 安全字符

// 最后定义ID
ID  : [a-zA-Z_] [a-zA-Z0-9_]*;



// 空白处理
WS  : [ \t\r\n]+ -> skip;
LINE_COMMENT: ('//' ~[\r\n]*) -> skip;
LINE_COMMENT2: ('#' ~[\r\n]*) -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
