from tortoise import fields
from tortoise.models import Model

import repository.models.ack
import repository.models.hobby
import repository.models.preferences
from repository.entity.utils import Sex


class Image(Model):
    id = fields.IntField(pk=True)
    image_id = fields.CharField(max_length=255, unique=True)

    profile: fields.ForeignKeyRelation["Profile"] = fields.ForeignKeyField(
        "models.Profile", related_name="images"
    )


class Profile(Model):
    telegram_id = fields.IntField(pk=True)
    telegram_tag = fields.CharField(max_length=255, unique=True)

    name = fields.TextField()
    last_name = fields.TextField()

    acked_first = fields.ReverseRelation["repository.models.ack.Ack"]
    acked_second = fields.ReverseRelation["repository.models.ack.Ack"]
    
    birthday = fields.DateField()
    zodiac: fields.ForeignKeyRelation[
        "repository.models.preferences.Zodiac"
    ] = fields.ForeignKeyField("models.Zodiac", related_name="profiles")
    
    sex = fields.CharEnumField(Sex)
    hobbies: fields.ManyToManyRelation[
        "repository.models.hobby.Hobby"
    ] 
    
    images: fields.ReverseRelation["Image"]
    preferences: fields.BackwardOneToOneRelation["repository.models.preferences.Preferences"]