import json

from typing import Optional, Union


class Edge:

    def __init__(self,
                 source: str,
                 target: str,
                 id: Optional[str] = None,
                 attributes: Optional[dict] = None):

        self.source = source
        self.target = target
        self.id = id
        self.attributes = attributes or {}

    def get_dict(self) -> dict:
        optionals = {
            k: self.__getattribute__(k)
            for k in ['id', 'attributes'] if self.__getattribute__(k)
        }
        return {
            'type': 'edge',
            'source': self.source,
            'target': self.target,
            **optionals
        }


class Node:

    def __init__(self,
                 id: str,
                 attributes: Optional[dict] = None):
        self.id = id
        self.attributes = attributes or {}

    def get_dict(self) -> dict:
        if self.attributes:
            optionals = {'attributes': self.attributes}
        else:
            optionals = {}
        return {
            'type': 'node',
            'id': self.id,
            **optionals
        }


class Jelm:

    def __init__(self,
                 metadata: Optional[dict]=None,
                 objects: Optional[list]=None,
                 **kwargs):

        #  TODO: add validation
        self.metadata = metadata or {}
        self.objects = objects or []

        if kwargs:
            raise ValueError("Tried to create jelm object with additional kwargs {}"
                             .format(kwargs.keys()))

    def dict(self) -> dict:
        return {
            'metadata': self.metadata,
            'objects': self.objects
        }

    def json_dumps(self) -> str:
        return json.dumps(self.dict())

    def json_dump(self, fp) -> None:
        try:
            json.dump(self.dict(),
                      fp)
        except AttributeError:
            if isinstance(fp, str):
                json.dump(self.dict(),
                          open(fp, 'w'))
            else:
                raise TypeError("""either pass something with a .write() method, 
                or a string pointing to a valid path to Jelm.json_dump""")

    def add_object(self, obj: Union[dict, Edge, Node]):

        if isinstance(obj, dict):

            try:
                obj_type = obj.pop('type')
            except KeyError:
                raise ValueError("if dict is given, 'type' key needs to be set! (to either node or edge)")

            if obj_type == 'edge':
                parsed_obj = Edge(**obj).get_dict()
            elif obj_type == 'node':
                parsed_obj = Node(**obj).get_dict()
            else:
                raise ValueError("object type needs to be either node or edge it is {}".format(obj_type))
        else:
            parsed_obj = obj.get_dict()

        self.objects.append(parsed_obj)

    def add_edge(self,
                 source: str,
                 target: str,
                 id: Optional[str] = None,
                 attributes: Optional[dict] = None):

        parsed_obj = Edge(source,
                          target,
                          id,
                          attributes).get_dict()
        self.objects.append(parsed_obj)

    def add_node(self,
                 id: str,
                 attributes: Optional[dict] = None):

        parsed_obj = Node(id, attributes).get_dict()

        self.objects.append(parsed_obj)

    def __iter__(self) -> Union[Edge, Node]:

        for o in self.objects:

            jelm_object_init_kwargs = o.copy()
            obj_type = jelm_object_init_kwargs.pop('type')
            if obj_type == 'edge':
                yield Edge(**jelm_object_init_kwargs)
            elif obj_type == 'node':
                yield Node(**jelm_object_init_kwargs)
