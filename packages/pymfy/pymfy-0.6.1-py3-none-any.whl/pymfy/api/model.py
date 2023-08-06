from typing import Dict, Union, List, Any


class Site(dict):
    __slots__ = 'id', 'label'

    def __init__(self, json: Dict[str, str]):
        self.id = json.get('id')
        self.label = json.get('label')
        dict.__init__(self, id=self.id, label=self.label)


class Device(dict):
    __slots__ = 'id', 'name', 'type', 'site_id', 'states', 'capabilities', \
                'categories'

    def __init__(self, json: Dict[str, Any]):
        self.id = json.get('id')
        self.name = json.get('name')
        self.type = json.get('type')
        self.site_id = json.get('site_id')
        self.categories = json.get('categories')
        self.states = [State(s) for s in json.get('states')]
        self.capabilities = [Capability(c) for c in json.get('capabilities')]
        dict.__init__(self, id=self.id, name=self.name, type=self.type,
                      site_id=self.site_id, categories=self.categories,
                      states=self.states, capabilities=self.capabilities)


class State(dict):
    __slots__ = 'name', 'value', 'type'

    def __init__(self, json: Dict[str, str]):
        self.name = json.get('name')
        self.value = json.get('value')
        self.type = json.get('type')
        dict.__init__(self, name=self.name, value=self.value, type=self.type)


class Capability(dict):
    __slots__ = 'name', 'parameters'

    def __init__(self, json: Dict[str, str]):
        self.name = json.get('name')
        self.parameters = [ParameterDescription(p) for p in
                           json.get('parameters')]
        dict.__init__(self, name=self.name, parameters=self.parameters)


class ParameterDescription(dict):
    __slots__ = 'name', 'type'

    def __init__(self, json: Dict[str, str]):
        self.name = json.get('name')
        self.type = json.get('type')
        dict.__init__(self, name=self.name, type=self.type)


class Command(dict):
    __slots__ = 'name', 'parameters'

    def __init__(self, name: str, parameters: Union[
            List[Dict[str, str]], Dict[str, str]] = None):
        if parameters is None:
            parameters = []
        if not isinstance(parameters, list):
            parameters = [parameters]
        self.name = name
        self.parameters = parameters
        dict.__init__(self, name=name, parameters=parameters)


class Parameter(dict):
    __slots__ = 'name', 'value'

    def __init__(self, name: str, value: Union[str, int]):
        self.name = name
        self.value = value
        dict.__init__(self, name=name, value=value)
