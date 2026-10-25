"""
Точка входа в игру «Тамагочи с кликером».

Запускает игровой цикл: показывает меню, обрабатывает ввод игрока,
обновляет состояние тамагочи и выводит текущий статус.
"""

import os

from game.models import Food, Medicine
from game.tamagochi import ConcreteTamagochi
from game.clicker import ConcreteClicker
from game.game import Game


def main():
    """
    Инициализирует компоненты игры и запускает бесконечный игровой цикл.

    Создаёт тамагочи, кликер, каталог товаров и экземпляр игры.
    В цикле выводит меню, принимает ввод пользователя, вызывает действия
    и обновляет состояние питомца. Завершает работу при смерти тамагочи.
    """
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]

    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = ConcreteTamagochi(name="Пушистик")
    clicker = ConcreteClicker(10, 20)
    game = Game(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        print(output)

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()
        print(
            f"\nСтатус: голод {status['hunger']}, здоровье {status['hp']}, "
            f"энергия {status['energy']}, монет {status['coins']}\n"
        )
        if game.tamagochi.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")
        print("1. Пойти на работу")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить")
        print("5. Вылечить")
        print("6. Играть")
        print("7. Отдых")
        print("0. Выход")

        match input("Выберите действие: "):
            case "1":
                income = game.work()
                output = f'Вы заработали {income} монет'
                game.tamagochi.update()
            case "2":
                game.buy_food()
            case "3":
                game.buy_medicine()
            case "4":
                game.feed_tamagochi()

            case "5":
                game.heal_tamagochi()
            case "6":
                game.play_with_tamagochi()
                output = 'Вы поиграли с питомцем'
            case "7":
                game.rest_tamagochi()
                output = 'Питомец отдохнул'
            case "0":
                return
            case _:
                output = "Неверная команда"

        # os.system('clear')


if __name__ == "__main__":
    main()
