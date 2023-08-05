from dataclasses import dataclass
from pathlib import Path
from typing import Any, Text, Set, List, Generator, Dict, Optional

from handsdown.utils import get_title_from_path_part


@dataclass
class ModuleObjectRecord:
    """
    Representation of an imported module object.

    Arguments:
        source_path -- Absolute import source path.
        source_line_number -- Line number of object definition.
        output_file_name -- MD file name for this module.
        object -- Imported module object.
        import_string -- Module import string.
        level -- 0 for classes and functions, 1 for methods.
        title -- Object human-readable title.
        docstring -- Object docstring.
        is_class -- True if object is a class.
        is_related -- True if object is from a different module
    """

    source_path: Path
    source_line_number: int
    output_file_name: Text
    object: Any
    import_string: Text
    level: int
    title: Text
    docstring: Optional[Text]
    is_class: bool
    is_related: bool


@dataclass
class ModuleRecord:
    """
    Representation of an imported module.

    Arguments:
        source_path -- Absolute import source path.
        output_file_name -- MD file name for this module.
        module -- Imported module.
        title -- Human readable module title.
        import_string -- Module import string.
        objects -- List of objects in the module.
        docstring -- Module docstring.
    """

    source_path: Path
    output_file_name: Text
    module: Any
    title: Text
    import_string: Text
    objects: List[ModuleObjectRecord]
    docstring: Optional[Text]

    def get_import_string_parts(self) -> List[Text]:
        """
        Get parts of module `import_string`.

        Examples:

            ```python
            ModuleRecord(..., import_string='my_module.utils.parsers').get_title_parts()
            # ['My my_module', 'utils', 'parsers']
            ModuleRecord(..., import_string='my_module.__main__').get_title_parts()
            # ['my_module', '__main__']
            ModuleRecord(..., import_string='my_module.my_lib', title='MyLibrary').get_title_parts()
            # ['my_module', 'my_lib']
            ```

        Returns:
            A list of import string parts as strings.
        """
        return self.import_string.split(".")

    def get_title_parts(self) -> List[Text]:
        """
        Get parts of module title from module import string.
        If `title` is set, last part replaced with `title`.

        Examples:

            ```python
            ModuleRecord(..., import_string='my_module.utils.parsers').get_title_parts()
            # ['My module', 'Utils', 'parsers']
            ModuleRecord(..., import_string='my_module.__main__').get_title_parts()
            # ['My module', 'Main']
            ModuleRecord(..., import_string='my_module.my_lib', title='MyLibrary').get_title_parts()
            # ['My module', 'MyLibrary']
            ```

        Returns:
            A list of title parts as strings.
        """
        parts = self.get_import_string_parts()
        result = []
        for part in parts:
            part = get_title_from_path_part(part)
            result.append(part)

        if self.title and result:
            result[-1] = self.title

        return result


class ModuleRecordList:
    """
    Aggregation of `ModuleRecord` objects.
    """

    def __init__(self) -> None:
        self.data: List[ModuleRecord] = []
        self.import_string_map: Dict[Text, Any] = {}

    def find_object(self, import_string: Text) -> Optional[ModuleObjectRecord]:
        """
        Find `ModuleObjectRecord` by it's import string.

        Arguments:
            import_string -- Object import string.

        Returns:
            Found `ModuleObjectRecord` instance or None.
        """
        return self.import_string_map.get(import_string)

    def get_output_file_names(self) -> Set[Text]:
        """
        Get all output MD file names.

        Returns:
            A set of output names as strings.
        """
        return {i.output_file_name for i in self}

    def get_package_names(self) -> Set[Text]:
        """
        Get top level import strings.

        Returns:
            A set of top level imports as strings.
        """
        return {i.import_string.split(".")[0] for i in self}

    def add(self, module_record: ModuleRecord) -> None:
        """
        Add new `ModuleRecord`.

        Arguments:
            module_record -- A new `ModuleRecord`
        """
        self.data.append(module_record)
        self.import_string_map[module_record.import_string] = module_record
        for obj in module_record.objects:
            import_string = f"{module_record.import_string}.{obj.import_string}"
            self.import_string_map[import_string] = obj

    def __iter__(self) -> Generator[ModuleRecord, None, None]:
        """
        Iterate over all added `ModuleRecord` entries.

        Returns:
            A generator iterating over `ModuleRecord` entries.
        """
        for obj in self.data:
            yield obj
