from spydrnet import Element, InnerPin, OuterPin, Wire, Netlist, Library, Definition, Instance, Port
from spydrnet.global_state.global_service import lookup
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern

import abc


def get_ports(obj, *args, **kwargs):
    """
    get_ports(obj, ...)

    Get ports *within* an object.

    Parameters:
    -----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_ports(definition, ...) would
        return all of the ports associated with the provided definition that match the additional criteria.
    patterns : str, Iterable - optional, positional or named, default: wildcard
        The search patterns. Patterns can be a single string or an Iterable collection of strings. Patterns can be
        absolute or they can contain wildcards or regular expressions. If `patterns` is not provided, then it defaults
        to a wildcard. Patterns are queried against the object property value stored under a specified key. Fast lookups
        are only attempted on absolute patterns that are not regular expressions and contain no wildcards.
    key : str, optional, default: ".NAME"
        This is the key that controls which value is being searched.
    is_case : bool - optional, named, default: True
        Specify if patterns should be treated as case sensitive. Only applies to patterns. Does not alter fast lookup
        behavior (if namespace policy uses case insensitive indexing, this parameter will not prevent a fast lookup
        from returning a matching object even if the case is not an exact match).
    is_re: bool - optional, named, default: False
        Specify if patterns are regular expressions. If `False`, a pattern can still contain `*` and `?` wildcards. A
        `*` matches zero or more characters. A `?` matches upto a single character.
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all
        matching virtual instances are returned. Otherwise, virtual instances that cause the filter function to evaluate
        to true are the only items returned.
    Returns the ports associated with a particular object or collection of objects.
    :return:
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_ports() got multiple values for argument 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'key', 'filter', 'is_case', 'is_re'} for x in kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")

    # Default values
    filter_func = kwargs.get('filter', lambda x: True)
    is_case = kwargs.get('is_case', True)
    is_re = kwargs.get('is_re', False)
    patterns = args[0] if len(args) == 1 else kwargs.get('patterns', ".*" if is_re else "*")
    key = kwargs.get('key', ".NAME")

    if isinstance(obj, (Element, InnerPin, OuterPin, Wire)) is False:
        try:
            object_collection = list(iter(obj))
        except TypeError:
            object_collection = (obj,)
    else:
        object_collection = (obj,)
    if all(isinstance(x, (Netlist, Library, Definition, Instance)) for x in object_collection) is False:
        raise TypeError("get_ports() only supports netlists, libraries, definitions, and instances, or a collection of "
                        "these as the object searched")

    if isinstance(patterns, str):
        patterns = (patterns,)

    return _get_ports(object_collection, patterns, key, is_case, is_re, filter_func)


def _get_ports(object_collection, patterns, key, is_case, is_re, filter_func):
    unique_results = set()
    for result in filter(filter_func, _get_ports_raw(object_collection, patterns, key, is_case, is_re)):
        if result not in unique_results:
            unique_results.add(result)
            yield result


def _get_ports_raw(object_collection, patterns, key, is_case, is_re):
    for pattern in patterns:
        pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
        for parent in _get_port_parents(object_collection):
            if pattern_is_absolute:
                result = lookup(parent, Port, key, pattern)
                if result is not None:
                    yield result
            else:
                for port in parent.ports:
                    if key in port:
                        value = port[key]
                        if _value_matches_pattern(value, pattern, is_case, is_re):
                            yield port


def _get_port_parents(object_collection):
    for obj in object_collection:
        if isinstance(obj, Netlist):
            for library in obj.libraries:
                for definition in library.definitions:
                    yield definition
        elif isinstance(obj, Library):
            for definition in obj.definitions:
                yield definition
        elif isinstance(obj, Instance):
            reference = obj.reference
            if reference is not None:
                yield reference
        else:
            yield obj
