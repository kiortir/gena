from tortoise.models import Model
from tortoise import fields
import repository.models.profile


class Hobby(Model):
    
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    
    profiles: fields.ManyToManyRelation["repository.models.profile.Profile"] = fields.ManyToManyField(
        "models.Profile", related_name="hobbies", through="hobby_profile"
    )
