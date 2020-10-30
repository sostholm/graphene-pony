import graphene
from datetime import date, datetime, time
import uuid

from graphene.types.json import JSONString
from pony.orm.ormtypes import Json
from pony.orm.core import Entity

from .utils import get_field_description

# singledispatch = import_single_dispatch()


class MongoEngineConversionError(Exception):
    pass

def convert_pony_field(field, registry=None):
    py_type = field.py_type

    return_type = None
# ( description=get_field_description(field, registry), required=field.is_required )
    if issubclass(py_type, int):
        return_type = graphene.Int

    if issubclass(py_type, str):
        return_type = graphene.String

    if issubclass(py_type, float):
        return_type = graphene.Float

    if issubclass(py_type, bool):
        return_type = graphene.Boolean

    if issubclass(py_type, date):
        return_type = graphene.Date

    if issubclass(py_type, datetime):
        return_type = graphene.DateTime

    if issubclass(py_type, time):
        return_type = graphene.Time

    if issubclass(py_type, Json):
        return_type = graphene.JSONString

    if return_type:
        return return_type(description=get_field_description(field, registry), required=field.is_required)

    if issubclass(py_type, Entity):
        if field.is_collection:
            base_type = convert_pony_field(field.field, registry=registry)
            if isinstance(base_type, graphene.Field):
                return graphene.List(
                    base_type._type,
                    description=get_field_description(field, registry),
                    required=field.required
                )

        elif field.is_relation:
            _type = registry.get_type_for_model(py_type)
            if not _type:
                return None
            return graphene.Field(_type, description=get_field_description(field, registry))

    # if isinstance(py_type, graphene.Field):
    #     return graphene.List(
    #         base_type._type,
    #         description=get_field_description(field, registry),
    #         required=field.required
    #     )
    # if isinstance(base_type, (graphene.Dynamic)):
    #     base_type = base_type.get_type()
    #     if base_type is None:
    #         return
    #     base_type = base_type._type

    if graphene.is_node(py_type):
        return py_type._meta.connection_field_class(py_type)

    # Non-relationship field
    if not isinstance(py_type, (graphene.List, graphene.NonNull)) and not field.is_collection:

        return graphene.List(
            py_type,
            description=get_field_description(field, registry),
            required=field.required,
        )



# @singledispatch
# def convert_mongoengine_field(field, registry=None):
#     raise MongoEngineConversionError(
#         "Don't know how to convert the MongoEngine field %s (%s)"
#         % (field, field.__class__)
#     )

# @convert_mongoengine_field.register(mongoengine.ListField)
# @convert_mongoengine_field.register(mongoengine.EmbeddedDocumentListField)
# def convert_field_to_list(field, registry=None):
#     base_type = convert_mongoengine_field(field.field, registry=registry)
#     if isinstance(base_type, graphene.Field):
#         return graphene.List(
#             base_type._type,
#             description=get_field_description(field, registry),
#             required=field.required
#         )
#     if isinstance(base_type, (graphene.Dynamic)):
#         base_type = base_type.get_type()
#         if base_type is None:
#             return
#         base_type = base_type._type

#     if graphene.is_node(base_type):
#         return base_type._meta.connection_field_class(base_type)

#     # Non-relationship field
#     relations = (mongoengine.ReferenceField, mongoengine.EmbeddedDocumentField)
#     if not isinstance(base_type, (graphene.List, graphene.NonNull)) and not isinstance(
#         field.field, relations
#     ):
#         base_type = type(base_type)

#     return graphene.List(
#         base_type,
#         description=get_field_description(field, registry),
#         required=field.required,
#     )


# @convert_mongoengine_field.register(mongoengine.GenericEmbeddedDocumentField)
# @convert_mongoengine_field.register(mongoengine.GenericReferenceField)
# def convert_field_to_union(field, registry=None):

#     _types = []
#     for choice in field.choices:
#         if isinstance(field, mongoengine.GenericReferenceField):
#             _field = mongoengine.ReferenceField(get_document(choice))
#         elif isinstance(field, mongoengine.GenericEmbeddedDocumentField):
#             _field = mongoengine.EmbeddedDocumentField(choice)

#         _field = convert_mongoengine_field(_field, registry)
#         _type = _field.get_type()
#         if _type:
#             _types.append(_type.type)
#         else:
#             # TODO: Register type auto-matically here.
#             pass

#     if len(_types) == 0:
#         return None

#     # XXX: Use uuid to avoid duplicate name
#     name = "{}_{}_union_{}".format(
#         field._owner_document.__name__,
#         field.db_field,
#         str(uuid.uuid1()).replace("-", ""),
#     )
#     Meta = type("Meta", (object,), {"types": tuple(_types)})
#     _union = type(name, (graphene.Union,), {"Meta": Meta})
#     return graphene.Field(_union)


# @convert_mongoengine_field.register(mongoengine.EmbeddedDocumentField)
# @convert_mongoengine_field.register(mongoengine.ReferenceField)
# @convert_mongoengine_field.register(mongoengine.CachedReferenceField)
# def convert_field_to_dynamic(field, registry=None):
#     model = field.document_type

#     def dynamic_type():
#         _type = registry.get_type_for_model(model)
#         if not _type:
#             return None
#         return graphene.Field(_type, description=get_field_description(field, registry))

#     return graphene.Dynamic(dynamic_type)


# @convert_mongoengine_field.register(mongoengine.LazyReferenceField)
# def convert_lazy_field_to_dynamic(field, registry=None):
#     model = field.document_type

#     def lazy_resolver(root, *args, **kwargs):
#         if getattr(root, field.name or field.db_name):
#             return getattr(root, field.name or field.db_name).fetch()

#     def dynamic_type():
#         _type = registry.get_type_for_model(model)
#         if not _type:
#             return None
#         return graphene.Field(
#             _type,
#             resolver=lazy_resolver,
#             description=get_field_description(field, registry),
#         )

#     return graphene.Dynamic(dynamic_type)
