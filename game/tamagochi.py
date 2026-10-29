"""Модуль с интерфейсом и реализациями класса тамагочи."""

from abc import ABC, abstractmethod
from typing import Any
from .constants import (
    HUNGER_INC,
    HAPPINESS_DEC,
    ENERGY_DEC,
    SICK_THRESHOLD,
    SICK_GAIN_BAD,
    SICK_DEC_GOOD,
    HP_DEC_SICK,
    HP_DEC_HEALTHY,
    HUNGER_DEATH,
    LOW_HUNGER,
    LOW_SICK,
    MAX_ENERGY,
    MAX_HAPPINESS,
    MAX_HP
)

from .exceptions import InvalidItemError, TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Абстрактное свойство для доступа ко всем состояниям тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Абстрактный метод для проверки жив ли тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Абстрактный метод для проверки, не заболел ли тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.

        Должен использоваться после каждого взаимодействия с тамагочи.
        """
        raise NotImplementedError


class ConcreteTamagochi(AbstractTamagochi):
    """
    Базовая реализация тамагочи.

    Состояния:
      - hunger: голод (0 = сыт, растёт со временем)
      - happiness: настроение (100 = счастлив, падает со временем)
      - energy: энергия (100 = полон сил, падает при действиях)
      - hp: здоровье (100 = здоров, падает от болезни/старости)
      - sick_progress: прогресс болезни (0–100, при 100 становится больным)

    Логика смерти: если hp <= 0 или hunger >= 120 - тамагочи умирает.
    Логика болезни: если sick_progress >= 100 - становится больным,
    hp начинает падать быстрее.
    """

    def __init__(self, name='Pufik') -> None:
        """Инициализирует нового тамагочи."""
        self._name = name
        self._hunger = LOW_HUNGER
        self._happiness = MAX_HAPPINESS
        self._energy = MAX_ENERGY
        self._hp = MAX_HP
        self._sick_progress = LOW_SICK
        self._is_sick = False
        self._is_dead = False

    def feed(self, food: Food) -> None:
        """Реализация метода кормления тамагочи."""
        if self._is_dead:
            raise TamagochiIsGone(
                f'{self._name} уже умер, '
                f'его нельзя кормить.'
            )
        self._hunger = max(0, self._hunger - food.satiety)
        self._happiness = min(MAX_HAPPINESS, self._happiness + 5)

    def play(self) -> None:
        """Реализация игры с тамагочи."""
        if self._is_dead:
            raise TamagochiIsGone(
                f'{self._name} уже умер, '
                f'с ним нельзя играть.'
            )
        if self._energy < 10:
            self._happiness = max(0, self._happiness - 5)
        else:
            self._energy = max(0, self._energy - 15)
            self._happiness = min(MAX_HAPPINESS, self._happiness + 10)

    def rest(self) -> None:
        """Реализация отдыха тамагочи."""
        if self._is_dead:
            raise TamagochiIsGone(f'{self._name} уже умер. Вечный отдых.')
        self._energy = min(MAX_ENERGY, self._energy + 20)
        self._hp = min(MAX_HP, self._hp + 5)

    def heal(self, medicine: Medicine) -> None:
        """Реализация лечения тамагочи."""
        if self._is_dead:
            raise TamagochiIsGone(
                f'{self._name} уже умер, '
                f'поздно пить Боржоми.'
            )
        if not medicine.use():
            raise InvalidItemError('Лекарство закончилось.')
        heal_amount = medicine.heal_hp
        self._hp = min(MAX_HP, self._hp + heal_amount)
        if heal_amount > 0 and self._is_sick:
            self._is_sick = False
            self._sick_progress = 0

    @property
    def status(self) -> dict[str, Any]:
        """Получение статуса тамагочи."""
        return {
            'name': self._name,
            'hunger': self._hunger,
            'happiness': self._happiness,
            'energy': self._energy,
            'hp': self._hp,
            'sick_progress': self._sick_progress,
            'is_sick': 1 if self._is_sick else 0,
            'is_dead': 1 if self._is_dead else 0
        }

    def is_alive(self) -> bool:
        """Проверка, жив ли тамагочи."""
        return not self._is_dead

    def is_sick(self) -> bool:
        """Проверка, болеет ли тамагочи."""
        return self._is_sick

    def update(self) -> None:
        """Обновление состояний тамагочи."""
        if self._is_dead:
            raise TamagochiIsGone('Тамагочи умер :(')

        self._hunger += HUNGER_INC
        self._happiness = max(0, self._happiness - HAPPINESS_DEC)
        self._energy = max(0, self._energy - ENERGY_DEC)

        if not self._is_sick:
            if self._happiness < 30 and self._energy < 30:
                self._sick_progress += SICK_GAIN_BAD
            else:
                self._sick_progress = max(
                    0, self._sick_progress - SICK_DEC_GOOD
                )

            if self._sick_progress >= SICK_THRESHOLD:
                self._is_sick = True
                self._sick_progress = SICK_THRESHOLD

        if self._is_sick:
            self._hp = max(0, self._hp - HP_DEC_SICK)
            self._sick_progress = min(
                SICK_THRESHOLD,
                self._sick_progress + 1
            )
        else:
            self._hp = max(0, self._hp - HP_DEC_HEALTHY)
        if self._hp <= 0 or self._hunger >= HUNGER_DEATH:
            self._is_dead = True
            self._hp = 0
            self._hunger = HUNGER_DEATH
