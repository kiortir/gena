from tortoise import fields
from tortoise.models import Model

import repository.models.hobby
import repository.models.preferences
import repository.models.profile


# class Ack(Model):
#     id = fields.IntField(pk=True)

#     whom: fields.ForeignKeyRelation[
#         "repository.models.profile.Profile"
#     ] = fields.ForeignKeyField("models.Profile", related_name="acked_by")

#     by: fields.ForeignKeyRelation[
#         "repository.models.profile.Profile"
#     ] = fields.ForeignKeyField("models.Profile", related_name="acked")

#     is_approved = fields.BooleanField()


class Ack(Model):
    
    u1: fields.ForeignKeyRelation[
        "repository.models.profile.Profile"
    ] = fields.ForeignKeyField("models.Profile", related_name="acked_first")
    
    u2: fields.ForeignKeyRelation[
        "repository.models.profile.Profile"
    ] = fields.ForeignKeyField("models.Profile", related_name="acked_second")
    
    u1_reaction = fields.BooleanField(null=True)
    u2_reaction = fields.BooleanField(null=True)
    