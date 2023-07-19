from tortoise.models import Model
from tortoise import fields
from entity.profile import Sex


class Profile(Model):
    # telegram_tag = fields.TextField()
    telegram_id = fields.IntField(pk=True)
    name = fields.TextField()
    last_name = fields.TextField()
    birthday = fields.DateField()
    sex = fields.CharEnumField(Sex)
    gorod = fields.TextField()
    kogo_ishu = fields.CharEnumField(Sex) 
    photo = fields.TextField()
    
    profiles_acknowledged: fields.ManyToManyRelation["Acknowledged"]
    acknowledged_by: fields.ManyToManyRelation["Acknowledged"]

    def __repr__(self):
        return self.name

class Acknowledged(Model):
    acknowledged_by: fields.ForeignKeyRelation[Profile] = fields.ForeignKeyField('models.Profile', related_name='profiles_acknowledged')
    acknowledged_who: fields.ForeignKeyRelation[Profile] = fields.ForeignKeyField('models.Profile', related_name="acknowledged_by")
    id = fields.IntField(pk=True)
    
    is_attracted: fields.BooleanField
    acknowledged_when: fields.DatetimeField 