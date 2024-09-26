"""
Some meta code for the model.

Explaination:
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, fields
from typing import Self, Callable, Iterable, Iterator, SupportsIndex, Type, get_type_hints, Any

@dataclass
class Node:
    # Subscription
    _subscribers: list[Callable] = field(default_factory=list, init=False)
    def subscribe(self, callback: Callable) -> None:
        """
        Subscribe to a node (part of the model)
        In other words, register a call back function that gets called when 
        a node or any of its children change. 
        """
        self._subscribers.append(callback) # sub self 
        for v in self.__dict__.values(): # sub children
            if isinstance(v, Node) or isinstance(v, ListNode):
                v.subscribe(callback)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, Node) or isinstance(v, ListNode):
                        item.subscribe(callback)

    def notify_subscribers(self) -> None:
        for subscriber in self._subscribers:
            subscriber(self.to_dict())

    # Overide dot operator, for fields / attrs, use set for lists, dicts and other mutable types 
    def __setattr__(self, key: str, value: Any) -> None:
        super().__setattr__(key, value)
        self.notify_subscribers()

    def set(self, key: str, value: Any) -> None:
        setattr(self, key, value)
        self.notify_subscribers()

    # From dict / to dict
    def to_dict(self) -> dict:
        children = self.__dict__
        name = self.__class__.__name__
        output_dict = {}
        for k, v in children.items():
            if k[0] == '_':
                continue
            elif isinstance(v, ListNode):
                output_dict[k] = v.to_dict()
            elif isinstance(v, list):
                sub_list = []
                for item in v:
                    if isinstance(item, Node):
                        sub_list.append(item.to_dict())
                    else:
                        sub_list.append(item)
                output_dict[k] = sub_list
            elif isinstance(v, Node):
                output_dict[k] = v.to_dict()
            else:
                output_dict[k] = v
        return {name: output_dict}
    
    @classmethod
    def from_dict(cls: Type['Node'], data: dict[str, Any]) -> 'Node':
        _, content = next(iter(data.items()))
        field_values = {}
        type_hints = get_type_hints(cls)

        for field in fields(cls):
            field_name = field.name
            if field_name in content:
                value = content[field_name]
                field_type = type_hints[field_name]

                if isinstance(field_type, type) and issubclass(field_type, (ListNode, Node)):
                    field_values[field_name] = field_type.from_dict(value)
                elif isinstance(value, list):
                    elem_type = field_type.__args__[0]
                    field_values[field_name] = [elem_type.from_dict(v) if isinstance(v, dict) else v for v in value]
                else:
                    field_values[field_name] = value
        return cls(**field_values)

class ListNode(list):
    def __init__(self, *args: Node):
        self._subscribers: list[Callable] = []
        super().__init__(*args)

    # Subscription
    def subscribe(self, callback: Callable) -> None:
        self._subscribers.append(callback)
        for k, v in self.__dict__.items():
            if isinstance(v, Node) or isinstance(v, ListNode):
                v.subscribe(callback)
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, Node) or isinstance(item, ListNode):
                        item.subscribe(callback)

    def notify_subscribers(self) -> None:
        for subscriber in self._subscribers:
            subscriber(self.to_dict())

    # Wrapping list functionality
    def __iter__(self) -> Iterator[Node]:
        return super().__iter__()
    
    def append(self, object: Any) -> None:
        super().append(object)
        self.notify_subscribers()

    def remove(self, object: Any) -> None:
        super().remove(object)
        self.notify_subscribers()

    def insert(self, index: SupportsIndex, objects: Any) -> None:
        super().insert(index, objects)
        self.notify_subscribers()

    def clear(self) -> None:
        super().clear()
        self.notify_subscribers()

    def extend(self, iterable: Iterable) -> None:
        super().extend(iterable)
        self.notify_subscribers()
        
    def pop(self, index: SupportsIndex = -1) -> Node:
        node = super().pop(index)
        self.notify_subscribers()
        return node

    # from dict / to dict
    def to_dict(self) -> dict:
        name = self.__class__.__name__
        if len(self) > 0:
            assert all(isinstance(x, type(self[0])) for x in self), 'Not all elements are the same type'
            return {name:[node.to_dict() for node in self]}
        else:
            return {name: []}

    @classmethod
    def from_dict(cls, d:dict) -> Self:
        assert len(d) == 1, 'ListNode Dictionary should only have a single key value pair'
        items_as_dict: dict = list(d.values())[0]
        items = [cls.type.from_dict(item) for item in items_as_dict]
        return cls(items)
    