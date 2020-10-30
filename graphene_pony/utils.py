from __future__ import unicode_literals

import inspect
from collections import OrderedDict

from pony.orm.core import Entity, Attribute
from graphene import Node
from graphene.utils.trim_docstring import trim_docstring


def get_model_fields(model, excluding=None):
    excluding = excluding or []
    attributes = dict()
    for attr_name in model._adict_.keys():
        if attr_name in excluding:
            continue
        attributes[attr_name] = getattr(model, attr_name)
    return OrderedDict(sorted(attributes.items()))


def get_model_reference_fields(model, excluding=None):
    excluding = excluding or []
    attributes = dict()
    for attr_name in model._columns_:
        attr = getattr(model, attr_name)
        if attr_name in excluding or not attr.is_relation:
            continue
        attributes[attr_name] = attr
    return attributes


def is_valid_pony_orm_model(model):
    return inspect.isclass(model) and (
        issubclass(model, Entity)
    )


# noqa

def get_field_description(field, registry=None):
    """
    Common metadata includes verbose_name and help_text.

    http://docs.mongoengine.org/apireference.html#fields
    """
    parts = []
    # if hasattr(field, "document_type"):
    #     doc = trim_docstring(field.document_type.__doc__)
    #     if doc:
    #         parts.append(doc)
    # if hasattr(field, "verbose_name"):
    #     parts.append(field.verbose_name.title())
    # if hasattr(field, "help_text"):
    #     parts.append(field.help_text)
    if field.column != field.name:
        name_format = "(%s)" if parts else "%s"
        parts.append(name_format % field.column)

    return "\n".join(parts)
    # return ''


def get_node_from_global_id(node, info, global_id):
    try:
        for interface in node._meta.interfaces:
            if issubclass(interface, Node):
                return interface.get_node_from_global_id(info, global_id)
    except AttributeError:
        return Node.get_node_from_global_id(info, global_id)
