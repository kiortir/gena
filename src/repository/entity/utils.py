from enum import Enum


class Sex(str, Enum):
    Male = "M"
    Female = "F"


class ZodiacOptions(str, Enum):
    Овен = "Овен"
    Телец = "Телец"
    Близнецы = "Близнецы"
    Рак = "Рак"
    Лев = "Лев"
    Дева = "Дева"
    Весы = "Весы"
    Скорпион = "Скорпион"
    Стрелец = "Стрелец"
    Козерог = "Козерог"
    Водолей = "Водолей"
    Рыбы = "Рыбы"


ZODIAC_RANGES = list(
    zip(
        ZodiacOptions,
        [
            ((21, 3), (19, 4)),
            ((20, 4), (20, 5)),
            ((21, 5), (20, 6)),
            ((21, 6), (22, 7)),
            ((23, 7), (22, 8)),
            ((23, 8), (22, 9)),
            ((23, 9), (22, 10)),
            ((23, 10), (21, 11)),
            ((22, 11), (21, 12)),
            ((22, 12), (19, 1)),
            ((20, 1), (18, 2)),
            ((19, 2), (20, 3)),
        ],
    )
)
