"""Модуль с исключениями."""


class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи."""


class NotEnoughMoney(Exception):
    """Ошибка, когда не хватает монет для покупки."""


class InvalidItemError(Exception):
    """Ошибка при использовании неподходящего предмета."""


class NoItemInInventory(Exception):
    """В инвентаре нет нужного предмета (еды/лекарства)."""


class ItemIndexError(Exception):
    """Ошибка индекса предмета."""
