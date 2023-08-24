from marshmallow import fields, Schema
from marshmallow import validates_schema


class BoardSchema(Schema):
    name = fields.Str()
    description = fields.Str()


class BoardCreateSchema(BoardSchema):

    @validates_schema
    def validate_creation(self):
        print(self.name)
        print(self.description)
        pass


class BoardInfoSchema(BoardSchema):
    admin = fields.Str(required=True)

    @validates_schema
    def validate_info(self):
        print(f"{self.__name__}")
        pass

