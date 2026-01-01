# coding=utf-8
"""
基于AST和标准库的代码规范检查工具（带颜色支持）
"""

import ast
import os
from typing import List, Dict
from dataclasses import dataclass
from enum import Enum
import tokenize
from io import BytesIO

# 颜色支持 - 使用 colorama 实现跨平台颜色输出
try:
    from colorama import init, Fore, Back, Style

    init(autoreset=True)  # 自动重置颜色
    HAS_COLORAMA = True
except ImportError:
    # 如果没有安装 colorama，使用基本颜色支持
    class Fore:
        RED = '\033[91m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        CYAN = '\033[96m'
        WHITE = '\033[97m'
        RESET = '\033[0m'


    class Back:
        RED = '\033[41m'
        GREEN = '\033[42m'
        YELLOW = '\033[43m'
        RESET = '\033[0m'


    class Style:
        BRIGHT = '\033[1m'
        RESET_ALL = '\033[0m'


    HAS_COLORAMA = False


class ViolationType(Enum):
    """违规类型枚举"""
    MISSING_DOCSTRING = "缺少文档字符串"
    MISSING_ATTRIBUTES = "缺少Attributes部分"
    INVALID_ATTRIBUTE_FORMAT = "Attributes格式不规范"
    MISSING_PARAM = "缺少参数文档"
    INVALID_PARAM_FORMAT = "参数文档格式不规范"
    MISSING_RETURN = "缺少返回值文档"
    INVALID_RETURN_FORMAT = "返回值文档格式不规范"
    INVALID_NAMING = "命名不规范"
    MISSING_TYPE_HINT = "缺少类型提示"
    MISSING_TYPE_ANNOTATION = "缺少类型注解"
    LONG_FUNCTION = "函数过长"
    LONG_LINE = "行过长"
    TODO_COMMENT = "待办事项注释"
    MISSING_MODULE_DOCSTRING = "模块缺少文档字符串"


@dataclass
class Violation:
    """违规信息"""
    file_path: str
    line_number: int
    type: ViolationType
    message: str
    node_name: str = ""

    def get_color(self) -> str:
        """根据违规类型返回对应颜色"""
        color_map = {
            ViolationType.MISSING_DOCSTRING: Fore.RED,
            ViolationType.MISSING_ATTRIBUTES: Fore.YELLOW,
            ViolationType.INVALID_ATTRIBUTE_FORMAT: Fore.YELLOW,
            ViolationType.MISSING_PARAM: Fore.RED,
            ViolationType.INVALID_PARAM_FORMAT: Fore.YELLOW,
            ViolationType.MISSING_RETURN: Fore.YELLOW,
            ViolationType.INVALID_RETURN_FORMAT: Fore.YELLOW,
            ViolationType.INVALID_NAMING: Fore.MAGENTA,
            ViolationType.MISSING_TYPE_HINT: Fore.CYAN,
            ViolationType.MISSING_TYPE_ANNOTATION: Fore.CYAN,
            ViolationType.LONG_FUNCTION: Fore.BLUE,
            ViolationType.LONG_LINE: Fore.BLUE,
            ViolationType.TODO_COMMENT: Fore.MAGENTA,
            ViolationType.MISSING_MODULE_DOCSTRING: Fore.RED,
        }
        return color_map.get(self.type, Fore.WHITE)


class ColoredPrinter:
    """彩色输出打印机"""

    @staticmethod
    def success(message: str) -> str:
        return f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}"

    @staticmethod
    def error(message: str) -> str:
        return f"{Fore.RED}❌ {message}{Style.RESET_ALL}"

    @staticmethod
    def warning(message: str) -> str:
        return f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}"

    @staticmethod
    def info(message: str) -> str:
        return f"{Fore.BLUE}📄 {message}{Style.RESET_ALL}"

    @staticmethod
    def highlight(text: str, color: str = Fore.CYAN) -> str:
        return f"{color}{text}{Style.RESET_ALL}"

    @staticmethod
    def bold(text: str) -> str:
        return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"

    @staticmethod
    def code_quality(message: str) -> str:
        return f"{Fore.BLUE}🔍 {message}{Style.RESET_ALL}"


class DocstringParser:
    """文档字符串解析器 - 使用标准库方法"""

    @staticmethod
    def parse_sections(docstring: str) -> Dict[str, List[str]]:
        """解析文档字符串的各个部分"""
        if not docstring:
            return {}

        sections = {}
        current_section = None
        current_content = []

        lines = docstring.split('\n')

        for line in lines:
            # 检查是否是新的section标题
            stripped_line = line.strip()
            if stripped_line.endswith(':') and not stripped_line.startswith(' ') and len(stripped_line) > 1:
                # 保存之前的section
                if current_section:
                    sections[current_section] = [line for line in current_content if line.strip()]
                # 开始新的section
                current_section = stripped_line[:-1]  # 去掉冒号
                current_content = []
            elif current_section is not None:
                # 属于当前section的内容
                if stripped_line:  # 忽略空行
                    current_content.append(stripped_line)
                elif current_content:  # 空行但之前有内容，添加空字符串保持结构
                    current_content.append('')
            elif stripped_line:  # 不在section中但有内容，可能是summary
                if 'summary' not in sections:
                    sections['summary'] = [stripped_line]
                else:
                    sections['summary'].append(stripped_line)

        # 保存最后一个section
        if current_section and current_content:
            sections[current_section] = [line for line in current_content if line.strip()]

        return sections

    @staticmethod
    def parse_attributes_section(content: List[str]) -> Dict[str, Dict[str, str]]:
        """解析Attributes部分"""
        attributes = {}

        for line in content:
            if ':' in line and not line.startswith(':'):
                # 格式: name (type): description
                parts = line.split(':', 1)
                if len(parts) == 2:
                    attr_name_and_type = parts[0].strip()
                    description = parts[1].strip()

                    # 解析 name (type)
                    if '(' in attr_name_and_type and ')' in attr_name_and_type:
                        name_end = attr_name_and_type.find('(')
                        attr_name = attr_name_and_type[:name_end].strip()
                        type_start = name_end + 1
                        type_end = attr_name_and_type.find(')', type_start)
                        attr_type = attr_name_and_type[type_start:type_end].strip()

                        attributes[attr_name] = {
                            'type': attr_type,
                            'description': description
                        }
                    else:
                        # 没有类型信息的情况
                        attr_name = attr_name_and_type.strip()
                        attributes[attr_name] = {
                            'type': 'Any',
                            'description': description
                        }

        return attributes

    @staticmethod
    def parse_params_section(content: List[str]) -> Dict[str, Dict[str, str]]:
        """解析参数部分"""
        params = {}

        for line in content:
            if ':' in line and not line.startswith(':'):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    param_name_and_type = parts[0].strip()
                    description = parts[1].strip()

                    # 解析 name (type)
                    if '(' in param_name_and_type and ')' in param_name_and_type:
                        name_end = param_name_and_type.find('(')
                        param_name = param_name_and_type[:name_end].strip()
                        type_start = name_end + 1
                        type_end = param_name_and_type.find(')', type_start)
                        param_type = param_name_and_type[type_start:type_end].strip()

                        params[param_name] = {
                            'type': param_type,
                            'description': description
                        }
                    else:
                        # 没有类型信息
                        param_name = param_name_and_type.strip()
                        params[param_name] = {
                            'type': 'Any',
                            'description': description
                        }

        return params


class NamingConventionChecker:
    """命名规范检查器"""

    # 命名规范规则
    NAMING_RULES = {
        'class': {
            'pattern': r'^[A-Z][a-zA-Z0-9]*$',
            'description': '大驼峰命名法',
            'color': Fore.CYAN
        },
        'function': {
            'pattern': r'^[a-z_][a-zA-Z0-9_]*$',
            'description': '下划线命名法',
            'color': Fore.GREEN
        },
        'variable': {
            'pattern': r'^[a-z_][a-zA-Z0-9_]*$',
            'description': '下划线命名法',
            'color': Fore.GREEN
        },
        'constant': {
            'pattern': r'^[A-Z_][A-Z0-9_]*$',
            'description': '大写加下划线',
            'color': Fore.YELLOW
        },
        'module': {
            'pattern': r'^[a-z_][a-zA-Z0-9_]*$',
            'description': '下划线命名法',
            'color': Fore.GREEN
        }
    }

    @classmethod
    def check_naming(cls, name: str, node_type: str) -> bool:
        """检查命名是否符合规范"""
        import re
        if node_type in cls.NAMING_RULES:
            pattern = cls.NAMING_RULES[node_type]['pattern']
            return bool(re.match(pattern, name))
        return True  # 未知类型默认通过

    @classmethod
    def get_naming_color(cls, node_type: str) -> str:
        """获取命名类型对应的颜色"""
        return cls.NAMING_RULES.get(node_type, {}).get('color', Fore.WHITE)


class CodeAnalyzer:
    """代码分析器"""

    def __init__(self):
        self.violations: List[Violation] = []
        self.docstring_parser = DocstringParser()

    def analyze_file(self, file_path: str) -> List[Violation]:
        """分析单个Python文件"""
        self.violations.clear()

        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            # 使用tokenize检查语法
            try:
                tokens = list(tokenize.tokenize(BytesIO(content).readline))
            except tokenize.TokenError as e:
                self.violations.append(Violation(
                    file_path=file_path,
                    line_number=0,
                    type=ViolationType.MISSING_DOCSTRING,
                    message=f"文件语法错误: {str(e)}"
                ))
                return self.violations

            # 解析AST
            try:
                tree = ast.parse(content)
                visitor = CodeVisitor(file_path, self.docstring_parser)
                visitor.visit(tree)
                self.violations.extend(visitor.violations)
            except SyntaxError as e:
                self.violations.append(Violation(
                    file_path=file_path,
                    line_number=e.lineno or 0,
                    type=ViolationType.MISSING_DOCSTRING,
                    message=f"AST解析错误: {str(e)}"
                ))

        except Exception as e:
            self.violations.append(Violation(
                file_path=file_path,
                line_number=0,
                type=ViolationType.MISSING_DOCSTRING,
                message=f"文件读取错误: {str(e)}"
            ))

        return self.violations


class CodeVisitor(ast.NodeVisitor):
    """AST访问器 - 代码检查的核心"""

    MAX_LINE_LENGTH = 120
    MAX_FUNCTION_LINES = 50

    def __init__(self, file_path: str, docstring_parser: DocstringParser):
        self.file_path = file_path
        self.docstring_parser = docstring_parser
        self.violations: List[Violation] = []
        self.current_class = None
        self.function_stack: List[str] = []
        self.lines = []

    def visit_Module(self, node):
        """检查模块级别的规范"""
        self._check_module_docstring(node)
        # 读取源码行用于行长度检查
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.lines = f.readlines()
        except Exception:
            pass
        else:
            self._check_line_lengths()
            self._check_todo_comments()
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """检查类定义"""
        self.current_class = node.name
        self._check_naming(node.name, 'class', node.lineno)
        self._check_class_docstring(node)
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        """检查函数定义"""
        self.function_stack.append(node.name)
        self._check_function_docstring(node)
        self._check_type_hints(node)
        self._check_function_length(node)
        self.generic_visit(node)
        self.function_stack.pop()

    def visit_AsyncFunctionDef(self, node):
        """检查异步函数定义"""
        self.visit_FunctionDef(node)

    def visit_Assign(self, node):
        """检查变量赋值"""
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            line_no = node.lineno
            # 检查是否为常量（全大写）
            if var_name.isupper() and '_' in var_name:
                self._check_naming(var_name, 'constant', line_no)
            else:
                self._check_naming(var_name, 'variable', line_no)
        self.generic_visit(node)

    def _check_function_length(self, node):
        """检查函数长度"""
        if not self.lines:
            return

        try:
            # 获取函数的起始和结束行号
            start_line = node.lineno
            end_line = getattr(node, 'end_lineno', start_line)

            if end_line - start_line + 1 > self.MAX_FUNCTION_LINES:
                self.violations.append(Violation(
                    file_path=self.file_path,
                    line_number=start_line,
                    type=ViolationType.LONG_FUNCTION,
                    message=f"函数长度超过{self.MAX_FUNCTION_LINES}行限制",
                    node_name=node.name
                ))
        except Exception:
            pass

    def _check_module_docstring(self, node):
        """检查模块文档字符串"""
        docstring = ast.get_docstring(node)
        if not docstring:
            self.violations.append(Violation(
                file_path=self.file_path,
                line_number=1,
                type=ViolationType.MISSING_MODULE_DOCSTRING,
                message="模块缺少文档字符串",
                node_name="module"
            ))

    def _check_line_lengths(self):
        """检查行长度是否超限"""
        for i, line in enumerate(self.lines, 1):
            if len(line.rstrip('\n')) > self.MAX_LINE_LENGTH:
                self.violations.append(Violation(
                    file_path=self.file_path,
                    line_number=i,
                    type=ViolationType.LONG_LINE,
                    message=f"行长度超过{self.MAX_LINE_LENGTH}字符限制",
                    node_name=f"line_{i}"
                ))

    def _check_todo_comments(self):
        """检查TO-DO注释"""
        todo_patterns = ['TODO', 'FIXME', 'XXX']
        for i, line in enumerate(self.lines, 1):
            for pattern in todo_patterns:
                if pattern in line and '#' in line.split(pattern)[0]:
                    self.violations.append(Violation(
                        file_path=self.file_path,
                        line_number=i,
                        type=ViolationType.TODO_COMMENT,
                        message=f"发现{pattern}注释",
                        node_name=f"comment_{i}"
                    ))

    def _check_naming(self, name: str, node_type: str, line_number: int):
        """检查命名规范"""
        if not NamingConventionChecker.check_naming(name, node_type):
            rule_desc = NamingConventionChecker.NAMING_RULES.get(node_type, {}).get('description', '未知规范')
            self.violations.append(Violation(
                file_path=self.file_path,
                line_number=line_number,
                type=ViolationType.INVALID_NAMING,
                message=f"{node_type}命名不规范，应遵循{rule_desc}",
                node_name=name
            ))

    def _check_class_docstring(self, node):
        """检查类文档字符串"""
        docstring = ast.get_docstring(node)
        node_name = getattr(node, 'name', 'unknown')

        if not docstring:
            self.violations.append(Violation(
                file_path=self.file_path,
                line_number=node.lineno,
                type=ViolationType.MISSING_DOCSTRING,
                message="类缺少文档字符串",
                node_name=node_name
            ))
            return

        # 解析文档字符串
        sections = self.docstring_parser.parse_sections(docstring)

        # 检查是否有Attributes部分
        if 'Attributes' not in sections and 'attributes' not in [k.lower() for k in sections.keys()]:
            # 可以更智能地检查类中是否有实例变量
            pass

        # 检查Attributes格式
        for section_name, content in sections.items():
            if section_name.lower() == 'attributes':
                # 这里可以进行更详细的格式检查
                pass

    def _check_function_docstring(self, node):
        """检查函数文档字符串"""
        docstring = ast.get_docstring(node)
        node_name = node.name

        if not docstring:
            # 对于特殊方法跳过检查
            if not node_name.startswith('__') or node_name in ['__init__', '__str__', '__repr__']:
                self.violations.append(Violation(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    type=ViolationType.MISSING_DOCSTRING,
                    message="函数缺少文档字符串",
                    node_name=node_name
                ))
            return

        # 解析文档字符串
        sections = self.docstring_parser.parse_sections(docstring)

        # 检查参数文档
        self._check_function_params(node, sections, node.lineno, node_name)

        # 检查返回值文档
        self._check_function_returns(node, sections, node.lineno, node_name)

    def _check_function_params(self, node, sections: Dict[str, List[str]], line_number: int, node_name: str):
        """检查函数参数文档"""
        # 获取函数参数（排除self和cls）
        func_args = []
        for arg in node.args.args:
            if arg.arg not in ['self', 'cls']:
                func_args.append(arg.arg)

        if not func_args:
            return

        # 查找参数文档部分
        param_sections = ['Args', 'Parameters', 'args', 'parameters']
        param_content = []
        for section_name, content in sections.items():
            if section_name in param_sections:
                param_content = content
                break

        # 解析参数文档
        documented_params = set()
        if param_content:
            params_dict = self.docstring_parser.parse_params_section(param_content)
            documented_params = set(params_dict.keys())

        # 检查是否所有参数都有文档
        undocumented = set(func_args) - documented_params
        for param in undocumented:
            self.violations.append(Violation(
                file_path=self.file_path,
                line_number=line_number,
                type=ViolationType.MISSING_PARAM,
                message=f"参数 '{param}' 缺少文档",
                node_name=node_name
            ))

    def _check_function_returns(self, node, sections: Dict[str, List[str]], line_number: int, node_name: str):
        """检查函数返回值文档"""
        # 检查是否有返回值类型提示
        has_return_annotation = node.returns is not None

        # 检查是否有返回值文档
        return_sections = ['Returns', 'Return', 'returns', 'return']
        has_return_doc = any(section in sections for section in return_sections)

        # 检查函数体内是否有return语句
        has_return_stmt = self._function_has_return(node)

        # 如果有返回值但缺少文档
        if (has_return_annotation or has_return_stmt) and not has_return_doc:
            self.violations.append(Violation(
                file_path=self.file_path,
                line_number=line_number,
                type=ViolationType.MISSING_RETURN,
                message="函数有返回值但缺少Returns文档",
                node_name=node_name
            ))

    def _check_type_hints(self, node):
        """检查类型提示"""
        node_name = node.name

        # 检查参数类型提示
        for arg in node.args.args:
            if arg.arg not in ['self', 'cls'] and arg.annotation is None:
                self.violations.append(Violation(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    type=ViolationType.MISSING_TYPE_HINT,
                    message=f"参数 '{arg.arg}' 缺少类型提示",
                    node_name=node_name
                ))

        # 检查返回值类型提示
        if node.returns is None:
            has_return_stmt = self._function_has_return(node)
            if has_return_stmt:
                self.violations.append(Violation(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    type=ViolationType.MISSING_TYPE_HINT,
                    message="函数有返回语句但缺少返回值类型提示",
                    node_name=node_name
                ))

    def _function_has_return(self, node) -> bool:
        """检查函数是否有返回语句"""
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.Return) and stmt.value is not None:
                return True
        return False


class ProjectScanner:
    """项目扫描器"""

    def __init__(self, no_color: bool = False):
        self.analyzer = CodeAnalyzer()
        self.all_violations: List[Violation] = []
        self.ignored_dirs = {'.git', '__pycache__', '.pytest_cache', '.vscode', '.idea'}
        self.ignored_files = {'__init__.py'}
        self.no_color = no_color
        self.printer = ColoredPrinter()

    def scan_project(self, project_path: str) -> List[Violation]:
        """扫描整个项目"""
        self.all_violations.clear()

        project_path = os.path.abspath(project_path)

        if os.path.isfile(project_path):
            # 单个文件
            if project_path.endswith('.py'):
                violations = self.analyzer.analyze_file(project_path)
                self.all_violations.extend(violations)
        else:
            # 目录
            for root, dirs, files in os.walk(project_path):
                # 过滤忽略的目录
                dirs[:] = [d for d in dirs if d not in self.ignored_dirs]

                for file in files:
                    if file.endswith('.py') and file not in self.ignored_files:
                        file_path = os.path.join(root, file)
                        violations = self.analyzer.analyze_file(file_path)
                        self.all_violations.extend(violations)

        return self.all_violations

    def print_report(self, show_summary: bool = True):
        """打印检查报告 - 带颜色支持"""
        if not self.all_violations:
            print(self.printer.success("所有文件都符合规范！"))
            return

        print(self.printer.error(f"发现 {len(self.all_violations)} 个违规项：\n"))

        # 按文件分组显示
        violations_by_file = {}
        for violation in self.all_violations:
            if violation.file_path not in violations_by_file:
                violations_by_file[violation.file_path] = []
            violations_by_file[violation.file_path].append(violation)

        for file_path, violations in violations_by_file.items():
            rel_path = os.path.relpath(file_path, os.getcwd())
            print(self.printer.info(f"{rel_path}:"))

            for violation in violations:
                node_info = f" [{self.printer.highlight(violation.node_name)}]" if violation.node_name else ""

                # 根据是否有颜色支持选择输出方式
                if self.no_color:
                    print(f"  {violation.type.value} - 第{violation.line_number}行{node_info}: {violation.message}")
                else:
                    color = violation.get_color()
                    print(
                        f"  {color}⚠️  第{violation.line_number}行{node_info}: {violation.type.value} - {violation.message}{Style.RESET_ALL}")
            print()

        if show_summary:
            self._print_summary()

    def _print_summary(self):
        """打印违规统计摘要"""
        type_count = {}
        for violation in self.all_violations:
            type_name = violation.type.value
            type_count[type_name] = type_count.get(type_name, 0) + 1

        print(self.printer.bold("📊 违规类型统计:"))
        for violation_type, count in sorted(type_count.items()):
            print(f"  {violation_type}: {count} 个")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='Python项目代码规范检查工具（带颜色支持）')
    parser.add_argument('path', nargs='?', default='.', help='项目路径（默认为当前目录）')
    parser.add_argument('--quiet', '-q', action='store_true', help='只显示违规统计')
    parser.add_argument('--no-color', action='store_true', help='禁用颜色输出')

    args = parser.parse_args()

    # 尝试导入 colorama
    global HAS_COLORAMA
    try:
        import colorama
        colorama.init(autoreset=True)
        HAS_COLORAMA = True
    except ImportError:
        HAS_COLORAMA = False
        if not args.no_color:
            print("提示: 安装 colorama 以获得更好的颜色支持: pip install colorama")

    scanner = ProjectScanner(no_color=args.no_color or not HAS_COLORAMA)
    violations = scanner.scan_project(args.path)

    if args.quiet:
        # 只显示统计信息
        type_count = {}
        for violation in violations:
            type_name = violation.type.value
            type_count[type_name] = type_count.get(type_name, 0) + 1

        printer = ColoredPrinter()
        print(printer.bold("违规统计:"))
        for violation_type, count in sorted(type_count.items()):
            print(f"  {violation_type}: {count}")
    else:
        scanner.print_report()


if __name__ == "__main__":
    main()
