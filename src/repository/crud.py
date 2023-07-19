
import repository.profile
import entity.profile

async def create_or_update_profile(profile: entity.profile.Profile) -> repository.profile.Profile:

    p, _ = await repository.profile.Profile.update_or_create(defaults=profile.model_dump(), telegram_id=profile.telegram_id)
    return p
    
    
async def get_profile(tg_id: int) -> entity.profile.Profile | None:
    p = await repository.profile.Profile.get_or_none(telegram_id=tg_id)
    if not p:
        return None
    return entity.profile.Profile.model_validate(p, from_attributes=True)
    
async def get_profile_sex(sex: entity.profile.Sex = entity.profile.Sex.MALE) -> entity.profile.Profile | None:
    p = await repository.profile.Profile.get_or_none(sex=sex)
    return p and entity.profile.Profile.model_validate(p, from_attributes=True)


async def  yield_another(tg_id: int):
    user_profile = await repository.profile.Profile.get_or_none(telegram_id=tg_id)
    if not user_profile:
        raise ValueError()
    
    option = await repository.profile.Profile.filter(sex=user_profile.kogo_ishu, gorod=user_profile.gorod).filter()