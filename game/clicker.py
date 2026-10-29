"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def click(self) -> int:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик."""
        raise NotImplementedError


class ConcreteClicker(AbstractClicker):
    """Реализация кликера.

    Этот класс генерирует случайный доход в заданном диапазоне.
    Диапазон задается при инициализации.
    """

    def __init__(self, min_income: int, max_income: int) -> None:
        """Инициализатор кликера."""
        if min_income < 0 or max_income < 0:
            raise ValueError('Доход не может быть отрицательным.')
        if min_income > max_income:
            raise ValueError('min_income не может быть больше max_income.')

        self._min_income = min_income
        self._max_income = max_income
        self._current_income = 0
        self._click_count = 0
        self.clicks = 0

    def click(self) -> int:
        """Выполняет клик."""
        self._current_income = randint(self._min_income, self._max_income)
        self.clicks += 1
        return self._current_income

    @property
    def income_per_click(self) -> int:
        """Возвращает доход за последний клик."""
        return self._current_income
