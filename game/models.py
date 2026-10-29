"""Модуль с моделями."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """Модель объекта еды."""

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """Метод для красивого принтинга объекта."""
        return (
            f'{self.name} стоимость: {self.price}, '
            f'утоляет голод на {self.satiety} единиц'
        )


@dataclass
class Medicine:
    """Модель объекта лекарства."""

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """Проверяет, осталось ли еще лекарство."""
        return self.uses >= self.number_of_uses

    def use(self) -> bool:
        """Считает применения лекарств."""
        if self.is_empty():
            return False
        self.uses -= 1
        return True

    def __repr__(self) -> str:
        """Метод для красивого принтинга объекта."""
        uses_for_print = self.number_of_uses - self.uses
        return (
            f'{self.name} стоимость: {self.price}, '
            f'лечит на {self.heal_hp} HP, '
            f'использований: {uses_for_print}'
        )
