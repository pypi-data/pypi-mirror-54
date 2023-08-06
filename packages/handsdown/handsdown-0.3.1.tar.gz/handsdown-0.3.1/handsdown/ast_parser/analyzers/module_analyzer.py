"""
AST analyzer for `ast.Module` records.
"""
from handsdown.ast_parser.node_records.import_record import ImportRecord
from handsdown.ast_parser.node_records.class_record import ClassRecord
from handsdown.ast_parser.node_records.function_record import FunctionRecord
from handsdown.ast_parser.node_records.attribute_record import AttributeRecord
from handsdown.ast_parser.analyzers.base_analyzer import BaseAnalyzer
import handsdown.ast_parser.smart_ast as ast


class ModuleAnalyzer(BaseAnalyzer):
    """
    AST analyzer for `ast.Module` records.
    """

    def visit_Import(self, node):
        # type: (ast.Import) -> None
        """
        Parse info about module `import ...` statements.

        Adds new `ImportRecord` entry to `import_records`.

        Examples::

            import my_module
            import my_module as my
            import my_module.my_class
            import my_module.my_class as my_class

        Arguments:
            node -- AST node.
        """
        for alias in node.names:
            record = ImportRecord(node, alias)
            self.import_records.append(record)

    def visit_ImportFrom(self, node):
        # type: (ast.ImportFrom) -> None
        """
        Parse info about module `import ... from ...` statements.

        Adds new `ImportRecord` entry to `import_records`.

        Examples::

            from my_module import my_class
            from my_module import my_class as new_class

        Arguments:
            node -- AST node.
        """
        for alias in node.names:
            record = ImportRecord(node, alias)
            self.import_records.append(record)

    def visit_ClassDef(self, node):
        # type: (ast.ClassDef) -> None
        """
        Parse info about module `class ...` statements.

        Adds new `ClassRecord` entry to `class_records`.

        Examples::

            class MyClass():
                pass

        Arguments:
            node -- AST node.
        """
        record = ClassRecord(node)
        self.class_records.append(record)

    def visit_FunctionDef(self, node):
        # type: (ast.FunctionDef) -> None
        """
        Parse info about module `def ...` statements.

        Adds new `FunctionRecord` entry to `function_records`.

        Examples::

            def my_func(arg1):
                pass

        Arguments:
            node -- AST node.
        """
        record = FunctionRecord(node, is_method=False)
        self.function_records.append(record)

    def visit_Assign(self, node):
        # type: (ast.Assign) -> None
        """
        Parse info about module attribute statements.

        Adds new `AttributeRecord` entry to `attribute_records`.

        Examples::

            MY_MODULE_ATTR = 'value'

        Arguments:
            node -- AST node.
        """
        # skip multiple assignments
        if len(node.targets) != 1:
            return
        # skip complex assignments
        if not isinstance(node.targets[0], ast.Name):
            return

        record = AttributeRecord(node)
        self.attribute_records.append(record)
