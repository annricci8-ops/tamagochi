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
from game.constants import STATUS_TEMPLATE, MENU_TEMPLATE, SICK_WARNING
from game.exceptions import (
    InvalidItemError,
    NotEnoughMoney,
    ItemIndexError,
    TamagochiIsGone
)


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

    while True:
        os.system('clear')

        print(f'Сумка с едой: {game.food}')
        print(f'Сумка с лекарствами: {game.medicine}')
        print(STATUS_TEMPLATE.format(**game.get_status()))

        if game.tamagochi.is_sick():
            menu_text = f'{SICK_WARNING}{MENU_TEMPLATE}'
        else:
            menu_text = MENU_TEMPLATE
        print(menu_text)

        choice = input('Выберите действие: ')
        output = ''

        try:
            match choice:
                case '1':
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                case '2':
                    game.show_food_shop()
                    try:
                        idx = int(input('Введите индекс еды для покупки: '))
                        game.buy_food(idx)
                        output = 'Еда куплена.'
                    except (InvalidItemError, NotEnoughMoney) as e:
                        output = f'Ошибка:{e}'
                case '3':
                    game.show_medicine_shop()
                    try:
                        idx = int(
                            input('Введите индекс лекарства для покупки:')
                        )
                        game.buy_medicine(idx)
                        output = 'Лекарство куплено.'
                    except (InvalidItemError, NotEnoughMoney) as e:
                        output = f'Ошибка: {e}'
                case '4':
                    game.show_inventory_food()
                    try:
                        idx = int(input('Введите индекс еды из инвентаря:'))
                        game.feed_tamagochi(idx)
                        output = 'Питомец накормлен'
                    except ItemIndexError as e:
                        output = f'Ошибка: {e}'

                case '5':
                    game.show_inventory_medicine()
                    try:
                        idx = int(
                            input('Введите индекс лекарства из инвентаря:')
                        )
                        game.heal_tamagochi(idx)
                        output = "Питомец вылечен"
                    except ItemIndexError as e:
                        output = f'Ошибка: {e}'
                case '6':
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                case '7':
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                case '0':
                    print('Выход из игры.')
                    return
                case _:
                    output = 'Неверная команда'
        except TamagochiIsGone as e:
            output = f'Игра окончена: {e}'
            print(output)
            break

        if game.tamagochi.is_alive():
            game.tamagochi.update()

        if not game.tamagochi.is_alive():
            print('\n💀 Ваш тамагочи умер. Игра окончена.')
            break

        print(output)


if __name__ == "__main__":
    main()
