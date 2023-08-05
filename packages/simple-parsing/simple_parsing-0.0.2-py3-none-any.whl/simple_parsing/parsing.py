"""Simple, Elegant Argument parsing.
@author: Fabrice Normandin
"""
import argparse
import collections
import dataclasses
import enum
import inspect
from collections import namedtuple
import typing
from typing import *

from . import utils
from . import docstring


class InconsistentArgumentError(RuntimeError):
    """
    Error raised when the number of arguments provided is inconsistent when parsing multiple instances from command line.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ParseableFromCommandLine():
    """
    When applied to a dataclass, this enables creating an instance of that class and populating the attributes from the command-line.
    Each class is visually separated into a different argument group. The class docstring is used for the group description, while the 'attribute docstrings'
    are used for the help text of the arguments. See the example script for a more visual description.

    Example:
    ```
    @dataclass()
    class Options(ParseableFromCommandLine):
        a: int
        b: int = 10

    parser = argparse.ArgumentParser()
    Options.add_arguments(parser)

    args = parser.parse_args("--a 5")
    options = Options.from_args(args)
    print(options) 
    >>> Options(a=5, b=10)
    ```
    """

    @classmethod
    def add_arguments(cls, parser: argparse.ArgumentParser, multiple=False) -> None:
        """
        Adds corresponding command-line arguments for this class to the given parser.

        Arguments:
            parser {argparse.ArgumentParser} -- The base argument parser to use
            multiple {bool} -- Wether we wish to eventually parse multiple instances of this class or not.
        
        
        #TODO: Double-Check this mechanism, just to make sure this is natural and makes sense.
        
        NOTE: about boolean (flag-like) arguments:
        If the argument is present with no value, then the opposite of the default value should be used.
        For example, say there is an argument called "--no-cache", with a default value of False.
        - When we don't pass the argument, (i.e, $> python example.py) the value should be False.
        - When we pass the argument, (i.e, $> python example.py --no-cache), the value should be True.
        - When we pass the argument with a value, ex: "--no-cache true" or "--no-cache false", the given value should be used 
        """
        group = parser.add_argument_group(cls.__qualname__, description=cls.__doc__)
        for f in dataclasses.fields(cls):
            name = f"--{f.name}"
            arg_options: Dict[str, Any] = { 
                "type": f.type,
            }

            doc = docstring.get_attribute_docstring(cls, f.name)
            if doc is not None:
                if doc.docstring_below:
                    arg_options["help"] = doc.docstring_below
                elif doc.comment_above:
                    arg_options["help"] = doc.comment_above
                elif doc.comment_inline:
                    arg_options["help"] = doc.comment_inline
            
            if f.default is not dataclasses.MISSING:
                arg_options["default"] = f.default
            elif f.default_factory is not dataclasses.MISSING: # type: ignore
                arg_options["default"] = f.default_factory() # type: ignore
            else:
                arg_options["required"] = True
            
            # print(f"adding argument for field {f.name} with type {f.type}. Multiple is {multiple}, default value is {arg_options.get('default', None)}, required is {arg_options.get('required', None)}")
            # print("arg_options so far:", arg_options)
            
            if enum.Enum in f.type.mro():
                arg_options["choices"] = list(e.name for e in f.type)
                arg_options["type"] = str # otherwise we can't parse the enum, as we get a string.
                if "default" in arg_options:
                    default_value = arg_options["default"]
                    # if the default value is the Enum object, we make it a string
                    if isinstance(default_value, enum.Enum):
                        arg_options["default"] = default_value.name
            
            elif utils.is_tuple_or_list(f.type):
                # Check if typing.List or typing.Tuple was used as an annotation, in which case we can automatically convert items to the desired item type.
                # NOTE: we only support tuples with a single type, for simplicity's sake. 
                T = utils.get_argparse_container_type(f.type)
                arg_options["nargs"] = "*"
                if multiple:
                    arg_options["type"] = utils._parse_multiple_containers(f.type)
                else:
                    # TODO: Supporting the `--a '1 2 3'`, `--a [1,2,3]`, and `--a 1 2 3` at the same time is syntax is kinda hard, and I'm not sure if it's really necessary.
                    # right now, we support --a '1 2 3' '4 5 6' and --a [1,2,3] [4,5,6] only when parsing multiple instances.
                    # arg_options["type"] = utils._parse_container(f.type)
                    arg_options["type"] = T
            
            elif f.type is bool:
                arg_options["default"] = False if f.default is dataclasses.MISSING else f.default
                arg_options["type"] = utils.str2bool
                arg_options["nargs"] = "*" if multiple else "?"
                if f.default is dataclasses.MISSING:
                    arg_options["required"] = True
            
            elif multiple:
                required = arg_options.get("required", False)
                if required:
                    arg_options["nargs"] = "+"
                else:
                    arg_options["nargs"] = "*"
            
            group.add_argument(name, **arg_options)
    
    @classmethod
    def from_args(cls, args: argparse.Namespace):
        """Creates an instance of this class using results of `parser.parse_args()`
        
        Arguments:
            args {argparse.Namespace} -- The result of a call to `parser.parse_args()`
        
        Returns:
            object -- an instance of this class
        """
        args_dict = vars(args) 
        # print("args dict:", args_dict)
        constructor_args: Dict[str, Any] = {}
        for f in dataclasses.fields(cls):
            if enum.Enum in f.type.mro():
                constructor_args[f.name] = f.type[args_dict[f.name]]
            
            elif utils.is_tuple(f.type):
                constructor_args[f.name] = tuple(args_dict[f.name])
            
            elif utils.is_list(f.type):
                constructor_args[f.name] = list(args_dict[f.name])

            elif f.type is bool:
                value = args_dict[f.name]
                constructor_args[f.name] = value
                default_value = False if f.default is dataclasses.MISSING else f.default
                if value is None:
                    constructor_args[f.name] = not default_value
                elif isinstance(value, bool):
                    constructor_args[f.name] = value
                else:
                    raise argparse.ArgumentTypeError(f"bool argument {f.name} isn't bool: {value}")

            else:
                constructor_args[f.name] = args_dict[f.name]
        return cls(**constructor_args) #type: ignore

    @classmethod
    def from_args_multiple(cls, args: argparse.Namespace, num_instances_to_parse: int):
        """Parses multiple instances of this class from the command line, and returns them.
        Each argument may have either 0 values (when applicable), 1, or {num_instances_to_parse}. 
        NOTE: If only one value is provided, every instance will be populated with the same value.

        Arguments:
            args {argparse.Namespace} -- The
            num_instances_to_parse {int} -- Number of instances that are to be created from the given parsedarguments
        
        Raises:
            cls.InconsistentArgumentError: [description]
        
        Returns:
            List -- A list of populated instances of this class.
        """
        args_dict: Dict[str, Any] = vars(args)
        # keep the arguments and values relevant to this class.
        constructor_arguments: Dict[str, Union[Any, List]] = {}
        for f in dataclasses.fields(cls):
            constructor_arguments[f.name] = args_dict[f.name]
        
        arguments_per_instance: List[Dict[str, Any]] = []
        for i in range(num_instances_to_parse):
            
            instance_arguments: Dict[str, Any] = {}

            for field_name, field_values in constructor_arguments.items():
                if not isinstance(field_values, list):
                    instance_arguments[field_name] = field_values
                elif isinstance(field_values, (list, tuple)) and len(field_values) == 0:
                    instance_arguments[field_name] = field_values
                elif len(field_values) == 1:
                    instance_arguments[field_name] = field_values[0]
                elif len(field_values) == num_instances_to_parse:
                    instance_arguments[field_name] = field_values[i]
                else:
                    raise InconsistentArgumentError(
                        f"The field '{field_name}' contains {len(field_values)} values, but either 1 or {num_instances_to_parse} values were expected.")
            arguments_per_instance.append(instance_arguments)

        return list(
            cls(**arguments_dict) #type: ignore
            for arguments_dict in arguments_per_instance
        )
    
    def asdict(self) -> Dict[str, Any]:
        """Returns a dictionary constructed from this dataclass' values.
        
        Returns:
            Dict[str, Any] -- A dictionary
        """
        d = dataclasses.asdict(self)
        return d
    
    def attribute_docstrings(self) -> Dict[str, docstring.AttributeDocString]:
        """Returns a dictionary of all the attribute docstrings in this dataclass.
        
        Returns:
            Dict[str, docstring.AttributeDocString] -- A dictionary where the keys are the attribute names, and the values are `docstring.AttributeDocString` instances. 
        """
        docs = {}
        for field in dataclasses.fields(self):
            doc = docstring.get_attribute_docstring(self.__class__, field.name)
            if doc is not None:
                docs[field.name] = doc
        return docs

