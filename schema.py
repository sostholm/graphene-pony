import graphene
from models import Student
from graphene_pony import PonyObjectType
from graphene.relay import Node
from pony.orm import select, db_session

class StudentNode(PonyObjectType):
    class Meta:
        model = Student
        interfaces = (Node,)

class Query(graphene.ObjectType):

    students  = graphene.List(StudentNode)

    def resolve_students(self, info):
        with db_session:
            students = select(s for s in Student)[:]
        return students


schema = graphene.Schema(query=Query)
#, mutation=Mutation

query = """
query {
    students {
        record
        name
    }
}
"""

print(schema.execute(query))