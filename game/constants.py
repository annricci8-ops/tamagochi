"""Модуль с константами."""


LOW_HUNGER = 0
LOW_SICK = 0
MAX_HP = 100
MAX_HAPPINESS = 100
MAX_ENERGY = 100

HUNGER_INC = 2
HAPPINESS_DEC = 1
ENERGY_DEC = 1

SICK_THRESHOLD = 100
SICK_GAIN_BAD = 3
SICK_DEC_GOOD = 1

HP_DEC_SICK = 3
HP_DEC_HEALTHY = 1

HUNGER_DEATH = 120

FULL_COINS = 100

STATUS_TEMPLATE = (
    "\nСтатус: голод {hunger}, здоровье {hp}, "
    "энергия {energy}, монет {coins}\n"
)

MENU_ITEMS = [
    "1. Пойти на работу",
    "2. Купить еду",
    "3. Купить лекарство",
    "4. Покормить",
    "5. Вылечить",
    "6. Играть",
    "7. Отдых",
    "0. Выход"
]
MENU_TEMPLATE = "\n".join(MENU_ITEMS)

SICK_WARNING = (
    "=======Тамагочи болеет======\n"
    "=======Отдых действует менее эффективно======\n"
)
