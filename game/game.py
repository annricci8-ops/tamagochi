"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import InvalidItemError, TamagochiIsGone
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """Абстрактный метод инициализации класса игры."""
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine

    @abstractmethod
    def work(self) -> int:
        """Абстрактный метод для логики действия "работа."""
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """Абстрактный метод для получения всех характеристик тамагочи."""
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """Абстрактное свойство для доступа к сумке с едой."""
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """Абстрактное свойство для доступа к сумке с лекарствами."""
        raise NotImplementedError


class Game(AbstractGame):
    """
    Основная реализация игрового цикла и логики взаимодействия с тамагочи.

    Класс управляет экономикой (монеты, покупки), инвентарём (еда, лекарства)
    и действиями тамагочи (кормление, лечение, отдых, игра).
    """

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ) -> None:
        """Инициализация пользовательского класса игры."""
        super().__init__(tamagochi, clicker, all_food, all_medicine)
        self._inventory_food: list[Food] = []
        self._inventory_medicine: list[Medicine] = []
        self._coins: int = 100
        if len(self._all_food) < 2:
            while len(self._all_food) < 2:
                self._all_food.append(
                    Food(
                        name=f"Доп-еда-{len(self._all_food)}",
                        satiety=10, price=0
                    )
                )

        if len(self._all_medicine) < 2:
            while len(self._all_medicine) < 2:
                self._all_medicine.append(
                    Medicine(
                        name=f"Доп-лекарство-{len(self._all_medicine)}",
                        price=0, heal_hp=5, number_of_uses=1
                    )
                )

    def work(self) -> int:
        """Метод класса для зарабатывания монет."""
        earned = self._clicker.click()
        if earned is None:
            earned = 7
        if not isinstance(earned, int):
            earned = 7
        self._coins += earned
        return earned

    def buy_food(self) -> None:
        """Метод покупки еды."""
        if not self._all_food:
            return
        selected = self._all_food[0]
        if self._coins >= selected.price:
            self._coins -= selected.price
            self._inventory_food.append(selected)

    def buy_medicine(self) -> None:
        """Метод покупки лекарств."""
        if not self._all_medicine:
            return
        selected = self._all_medicine[0]
        if self._coins >= selected.price:
            self._coins -= selected.price
            self._inventory_medicine.append(selected)

    def feed_tamagochi(self) -> None:
        """Метод осуществляет кормление тамагочи."""
        if not self._inventory_food:
            print('У вас нет еды в сумке!')
            return
        food_item = self._inventory_food.pop(0)
        try:
            self._tamagochi.feed(food_item)
            print(f'Вы покормили питомца {food_item.name}.')
        except TamagochiIsGone as e:
            print(e)
        except InvalidItemError as e:
            print(e)

    def heal_tamagochi(self) -> None:
        """Метод осуществляет лечение тамогочи."""
        if not self._inventory_medicine:
            print('У вас нет лекарств в сумке!')
            return
        med_item = self._inventory_medicine.pop(0)
        try:
            self._tamagochi.heal(med_item)
            print(f'Вы полечили питомца {med_item.name}.')
        except TamagochiIsGone as e:
            print(e)
        except InvalidItemError as e:
            print(e)

    def rest_tamagochi(self) -> None:
        """Дает тамагочи отдохнуть."""
        self._tamagochi.rest()

    def play_with_tamagochi(self):
        """Играет с тамагочи."""
        self._tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        """Возврашает статус игры: параметры тамагочи + монеты + инвентарь."""
        base_status = self._tamagochi.status
        base_status.update({
            "coins": self._coins,
            "inventory_food_count": len(self._inventory_food),
            "inventory_medicine_count": len(self._inventory_medicine),
        })
        return base_status

    @property
    def food(self) -> list[Food]:
        """Возвращает список еды в инвентаре."""
        return self._inventory_food

    @property
    def medicine(self) -> list[Medicine]:
        """Возвращает список лекарств в интентаре."""
        return self._inventory_medicine

    @property
    def tamagochi(self):
        """Возврашает экземпляр тамагочи, которым управляет игра."""
        return self._tamagochi
