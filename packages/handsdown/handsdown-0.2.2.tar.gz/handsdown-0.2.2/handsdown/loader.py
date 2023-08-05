"""
Loader for python source code.
"""

import importlib

import sys
import inspect
import os
from typing import Optional, Text, Any, Callable, Generator, TYPE_CHECKING

try:
    from unittest import mock
except ImportError:
    import mock  # type: ignore

from handsdown.docstring_formatter import DocstringFormatter
from handsdown.utils.os_environ_mock import OSEnvironMock
from handsdown.utils.type_checking_mock import TypeCheckingMock
from handsdown.utils import make_title
from handsdown.module_record import ModuleRecord, ModuleObjectRecord
from handsdown.path_finder import PathFinder, Path

if TYPE_CHECKING:  # pragma: no cover
    import logging


class LoaderError(Exception):
    """
    Main error for `Loader` class.
    """


class Loader:
    """
    Loader for python source code.

    Examples::

        loader = Loader(Path('path/to/my_module/'))
        my_module_utils = loader.import_module('my_module.utils')

    Arguments:
        root_path -- Root path of the project.
        output_path -- Docs output path.
        logger -- Logger instance.
    """

    DJANGO_SETTINGS_ENV_VAR = "DJANGO_SETTINGS_MODULE"

    def __init__(self, root_path, output_path, logger):
        # type: (Path, Path, logging.Logger) -> None
        self._logger = logger
        self._root_path = root_path
        self._root_path_finder = PathFinder(self._root_path)
        self._output_path = output_path
        self._os_environ_patch = mock.patch("os.environ", OSEnvironMock(os.environ))
        self._logging_logger_patch = mock.patch("logging.Logger", mock.MagicMock())
        self._logging_config_patch = mock.patch(
            "logging.config.dictConfig", mock.MagicMock()
        )
        self._sys_path_patch = mock.patch(
            "sys.path", sys.path + [self._root_path.as_posix()]
        )
        self.setup()

    def setup(self):
        # type: () -> None
        """
        Setup local frameworks if needed.

        Frameworks supported:
        - `Django` (if `DJANGO_SETTINGS_MODULE` env variable is defined)
        """
        django_settings_env_var = os.environ.get(self.DJANGO_SETTINGS_ENV_VAR)
        if django_settings_env_var:
            self._logger.info(
                "Found {} env variable, trying to setup django apps with {} settings".format(
                    self.DJANGO_SETTINGS_ENV_VAR, django_settings_env_var
                )
            )
            self._setup_django()

    def get_output_path(self, source_path):
        # type: (Path) -> Path
        """
        Get output MD document path based on `source_path`.

        Arguments:
            source_path -- Path to source code file.

        Returns:
            A path to the output `.md` file even if it does not exist yet.
        """
        relative_source_path = self._root_path_finder.relative(source_path)
        if relative_source_path.stem == "__init__":
            relative_source_path = relative_source_path.parent / "index"
        if relative_source_path.stem == "__main__":
            relative_source_path = relative_source_path.parent / "magic_main"

        file_name = "{}.md".format(relative_source_path.stem)
        relative_output_path = relative_source_path.parent / file_name
        return self._output_path / relative_output_path

    def get_module_record(self, source_path):
        # type: (Path) -> Optional[ModuleRecord]
        """
        Build `ModuleRecord` for given `source_path`.

        Arguments:
            source_path -- Absolute path to source file.

        Returns:
            A new `ModuleRecord` instance or None if there is ntohing to import.

        Raises:
            LoaderError -- If module or any of it's objects cannot be imported.
        """
        if not (source_path.parent / "__init__.py").exists():
            return None

        if source_path.name == "__init__.py" and source_path.parent == self._root_path:
            return None

        file_import = self.get_import_string(source_path)
        main_class_lookup_name = source_path.stem.replace("_", "")

        try:
            inspect_module = self.import_module(source_path)
        except Exception as e:
            raise LoaderError("Cannot import {}: {}".format(source_path.name, e))

        docstring_parts = []
        docstring = self._get_object_docstring(inspect_module)
        if docstring:
            docstring_parts.append(docstring)

        if source_path.name == "__init__.py":
            readme_md_path = source_path.parent / "README.md"
            if readme_md_path.exists():
                docstring_parts.append(readme_md_path.read_text())

        module_record = ModuleRecord(
            module=inspect_module,
            title=make_title(file_import.split(".")[-1]),
            docstring="\n\n".join(docstring_parts),
            output_path=self.get_output_path(source_path),
            source_path=source_path,
            import_string=file_import,
            objects=[],
        )

        try:
            module_object_records = list(self._discover_module_objects(module_record))
        except Exception as e:
            raise LoaderError(
                "Cannot import module objects from {}: {}".format(source_path.name, e)
            )

        for object_record in module_object_records:
            # if class name looks like it is a main class in the module - set it as a title.
            if (
                object_record.is_class
                and not object_record.is_related
                and object_record.title.lower() == main_class_lookup_name
            ):
                module_record.title = object_record.title

            module_record.objects.append(object_record)

        # skip modules without objects and docstring
        if not module_record.objects and not module_record.docstring:
            return None

        return module_record

    def _setup_django(self):
        # type: () -> None
        """
        Initialize Django apps in order to safely import Django models.
        Patches applied during apps initialization:

        - Patch `os.environ` to avoid failing on undefined variables.
        - Patch `sys.path` to add current repo to it.
        - Patch `logging.config.dictConfig`.
        """
        self._os_environ_patch.start()
        self._sys_path_patch.start()
        self._logging_config_patch.start()

        try:
            django = importlib.import_module("django")
            getattr(django, "setup")()
        except Exception as e:
            self._logger.warning("Cannot setup django apps: {}".format(e))
        else:
            self._logger.info("Django apps are initialized")

        self._os_environ_patch.stop()
        self._sys_path_patch.stop()
        self._logging_config_patch.stop()

    def _get_object_docstring(self, obj):
        # type: (Any) -> Text
        """
        Get trimmed object docstring or an empty string.

        Arguments:
            obj -- Object to inspect.

        Returns:
            A string with object docsting.
        """
        docstring = self._get_docstring(obj)
        return DocstringFormatter(docstring).render()

    def get_import_string(self, source_path):
        # type: (Path) -> Text
        """
        Get Python import string for a source `source_path` relative to `root_path`.

        Examples::

            loader = Loader(root_path=Path("/root"), ...)
            loader.get_import_string('/root/my_module/test.py')
            'my_module.test'

            loader.get_import_string('/root/my_module/__init__.py')
            'my_module'

        Arguments:
            source_path -- Path to a source file.

        Returns:
            A Python import string.
        """
        relative_path = source_path.relative_to(self._root_path)
        name_parts = []
        for part in relative_path.parts:
            stem = part.split(".")[0]
            if stem == "__init__":
                continue
            name_parts.append(stem)

        return ".".join(name_parts)

    def import_module(self, file_path):
        # type: (Path) -> Any
        """
        Import module using `import_paths` list. Clean up all patches afterwards.

        - Patch `sys.path` to add current repo to it.
        - Patch `os.environ` to avoid failing on undefined variables.
        - Patch `typing.TYPE_CHECKING` to `True`.
        - Patch `logging.Logger`.
        - Patch `logging.config.dictConfig`.

        Arguments:
            file_path -- Abslute path to source file.

        Returns:
            Imported module object.
        """
        import_string = self.get_import_string(file_path)
        self._sys_path_patch.start()
        self._os_environ_patch.start()
        self._logging_logger_patch.start()
        self._logging_config_patch.start()

        self._logger.debug("Importing {} as {}".format(file_path, import_string))
        with mock.patch("typing.TYPE_CHECKING", TypeCheckingMock(file_path)):
            module = importlib.import_module(import_string)

        self._sys_path_patch.stop()
        self._os_environ_patch.stop()
        self._logging_logger_patch.stop()
        self._logging_config_patch.stop()

        return module

    @staticmethod
    def _inspect_predicate(obj):
        # type: (Any) -> bool
        # skip built-in objects
        if getattr(obj, "__name__", "type") == "type":
            return False

        # skip built-in objects
        if getattr(obj, "__module__", "builtins") == "builtins":
            return False

        # skip nameless objects
        if not getattr(obj, "__name__", None):
            return False

        # skip built-in objects
        if obj.__name__.startswith("__"):
            return False

        if not inspect.isclass(obj) and not inspect.isfunction(obj):
            return False

        return True

    @staticmethod
    def _get_parent_inspect_predicate(parent):
        # type: (Any) -> Callable[[Any], bool]
        def predicate(obj):
            # type: (Any) -> bool
            # skip nameless attributes
            if not getattr(obj, "__name__", None):
                return False

            # skip private attributes
            if obj.__name__.startswith("_"):
                return False

            # skip built-in attributes
            if obj.__name__ not in parent.__dict__:
                return False

            if inspect.ismethod(obj) or inspect.isfunction(obj):
                return True

            return False

        return predicate

    def _discover_module_objects(self, module_record):
        # type: (ModuleRecord) -> Generator[ModuleObjectRecord, None, None]
        """
        Get `ModuleObjectRecord` for every object in a module.

        Arguments:
            module_record -- `ModuleRecord` instance.

        Yields:
            New `ModuleObjectRecord` instances.
        """
        inspect_module = module_record.module
        relative_source_path = module_record.source_path.relative_to(self._root_path)

        members = inspect.getmembers(inspect_module, self._inspect_predicate)
        members.sort(key=lambda x: x[0])

        for object_name, inspect_object in members:
            is_class = inspect.isclass(inspect_object)

            # skip modules with unknown source
            try:
                source_path_str = inspect.getsourcefile(inspect_object)
            except (TypeError, OSError, ValueError):
                continue

            if not source_path_str:
                continue

            source_path = Path(source_path_str)

            # fix source path if module was imported from installed pacakges
            if source_path.as_posix().endswith(relative_source_path.as_posix()):
                source_path = module_record.source_path

            # skip modules from 3rd party libraries
            try:
                source_path.relative_to(self._root_path)
            except ValueError:
                continue

            is_related = source_path != module_record.source_path
            docstring = ""
            if not is_related:
                docstring = self._get_object_docstring(inspect_object)

            module_object_record = ModuleObjectRecord(
                import_string=object_name,
                level=0,
                obj=inspect_object,
                docstring=docstring,
                title=object_name,
                module_record=module_record,
                source_path=source_path,
                output_path=self.get_output_path(source_path),
                source_line_number=self.get_source_line_number(inspect_object),
                is_class=is_class,
                is_related=is_related,
            )
            yield module_object_record

            if not is_class or is_related:
                continue

            for item in self._discover_class_properties(
                module_object_record, module_record
            ):
                yield item

            for item in self._discover_class_methods(
                module_object_record, module_record
            ):
                yield item

    def _discover_class_properties(self, module_object_record, module_record):
        # type: (ModuleObjectRecord, ModuleRecord) -> Generator[ModuleObjectRecord, None, None]
        """
        Get `ModuleObjectRecord` for every property in a class.

        Arguments:
            module_object_record -- `ModuleObjectRecord` instance to inspect.

        Yields:
            New `ModuleObjectRecord` instances.
        """
        object_name = module_object_record.import_string
        inspect_object = module_object_record.obj
        source_path = module_object_record.source_path

        for property_name in dir(inspect_object):
            property_object = getattr(inspect_object, property_name, None)
            if property_object and isinstance(property_object, property):

                # skip inherited properties
                inspect_object_parents = inspect.getmro(inspect_object)
                if len(inspect_object_parents) > 2:
                    if (
                        getattr(inspect_object_parents[1], property_name, None)
                        == property_object
                    ):
                        continue

                import_string = "{}.{}".format(object_name, property_name)
                title = "{}().{}".format(object_name, property_name)
                yield ModuleObjectRecord(
                    import_string=import_string,
                    level=1,
                    obj=property_object,
                    docstring=self._get_object_docstring(property_object),
                    title=title,
                    module_record=module_record,
                    source_path=source_path,
                    output_path=self.get_output_path(source_path),
                    source_line_number=self.get_source_line_number(inspect_object),
                    is_class=False,
                    is_related=False,
                )

    def _discover_class_methods(self, module_object_record, module_record):
        # type: (ModuleObjectRecord, ModuleRecord) -> Generator[ModuleObjectRecord, None, None]
        """
        Get `ModuleObjectRecord` for every method in a class.

        Arguments:
            module_object_record -- `ModuleObjectRecord` instance to inspect.

        Yields:
            New `ModuleObjectRecord` instances.
        """
        object_name = module_object_record.import_string
        inspect_object = module_object_record.obj
        source_path = module_object_record.source_path

        object_members = inspect.getmembers(
            inspect_object, self._get_parent_inspect_predicate(inspect_object)
        )
        object_members.sort(key=lambda x: x[0])

        for method_name, inspect_method in object_members:
            class_method = getattr(inspect_object, method_name)
            unbound_method = inspect_object.__dict__[method_name]

            import_string = "{}.{}".format(object_name, method_name)
            title = "{}().{}".format(object_name, method_name)
            if isinstance(unbound_method, (staticmethod, classmethod)):
                title = "{}.{}".format(object_name, method_name)

            yield ModuleObjectRecord(
                import_string=import_string,
                level=1,
                obj=class_method,
                module_record=module_record,
                docstring=self._get_object_docstring(inspect_method),
                title=title,
                source_path=source_path,
                output_path=self.get_output_path(source_path),
                source_line_number=self.get_source_line_number(inspect_method),
                is_class=False,
                is_related=False,
            )

    @staticmethod
    def _get_docstring(obj):
        # type: (Any) -> Text
        if isinstance(obj, (staticmethod, classmethod)):
            return obj.__func__.__doc__ or ""
        if hasattr(obj, "__name__") or isinstance(obj, property):
            return obj.__doc__ or ""
        if hasattr(obj, "__call__"):
            return obj.__call__.__doc__ or ""

        return obj.__doc__ or ""

    def get_source_line_number(self, obj):
        # type: (Any) -> int
        """
        Get line number in source file where `obj` is declared.

        obj -- Object to inspect.

        Returns:
            A line number as an integer, starting for 1.
        """
        try:
            source_code_info = inspect.findsource(obj)
        except OSError:
            self._logger.debug("Cannot get source line for {}".format(obj))
            return 1
        return source_code_info[1] + 1
