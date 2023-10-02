from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.postgres.fields import ArrayField


from repository.entity.utils import Sex, ZodiacOptions
import repository.models.profile


class Zodiac(Model):
    id = fields.IntField(pk=True)

    name = fields.CharEnumField(ZodiacOptions, unique=True)

    profiles: fields.ReverseRelation["repository.models.profile.Profile"]
    preferenced_by: fields.ManyToManyRelation[
        "Preferences"
    ] = fields.ManyToManyField(
        "models.Preferences",
        related_name="zodiacs",
        through="preference_zodiac",
    )


class Preferences(Model):
    id = fields.IntField(pk=True)

    profile: fields.OneToOneRelation[
        "repository.models.profile.Profile"
    ] = fields.OneToOneField(
        "models.Profile", on_delete=fields.CASCADE, related_name="preferences"
    )

    sex = fields.CharEnumField(Sex, null=True)
    zodiacs: fields.ManyToManyRelation[Zodiac]

