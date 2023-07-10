from tortoise.models import Model
from tortoise import fields
from entity.profile import Sex


class Profile(Model):
    telegram_id = fields.IntField(pk=True)
    name = fields.TextField()
    last_name = fields.TextField()
    birthday = fields.DateField()
    sex = fields.CharEnumField(Sex)
    gorod = fields.TextField()
    kogo_ishu = fields.CharEnumField(Sex) 
    photo = fields.TextField()

    def __repr__(self):
        return self.name

class Acknowledged(Model):
    acknowledged_by = fields.ForeignKeyField('models.Profile')
    acknowledged_who = fields.ForeignKeyField('models.Profile', related_name='acknowledged')
    id = fields.IntField(pk=True)
