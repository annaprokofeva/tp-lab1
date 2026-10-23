"""Основные классы пошаговой стратегии. Имена методов сохранены из задания."""

from abc import ABC, abstractmethod
from itertools import count


class Attacker(ABC):
    """Интерфейс объектов, способных атаковать юнитов."""

    @abstractmethod
    def attack(self, unit: "Unit") -> None:
        pass


class Moveable(ABC):
    """Интерфейс перемещения в указанные координаты."""

    @abstractmethod
    def move(self, x: int, y: int) -> None:
        pass


class GameObject:
    _ids = count(1)

    def __init__(self, name: str, x: int, y: int):
        self._id = next(GameObject._ids)
        self._name = name
        self._x = x
        self._y = y

    def getId(self) -> int:
        return self._id

    def getName(self) -> str:
        return self._name

    def getX(self) -> int:
        return self._x

    def getY(self) -> int:
        return self._y


class Unit(GameObject):
    def __init__(self, name: str, x: int, y: int, hp: float = 100.0):
        super().__init__(name, x, y)
        if hp <= 0:
            raise ValueError("Начальное здоровье должно быть положительным")
        self._hp = float(hp)

    def isAlive(self) -> bool:
        return self._hp > 0

    def getHp(self) -> float:
        return self._hp

    def receiveDamage(self, damage: float) -> None:
        if damage < 0:
            raise ValueError("Урон не может быть отрицательным")
        self._hp = max(0.0, self._hp - damage)


class Archer(Unit, Attacker, Moveable):
    def __init__(self, name: str, x: int, y: int,
                 hp: float = 100.0, damage: float = 20.0):
        super().__init__(name, x, y, hp)
        if damage < 0:
            raise ValueError("Урон не может быть отрицательным")
        self._damage = float(damage)

    def attack(self, unit: Unit) -> None:
        if not self.isAlive():
            raise ValueError("Погибший лучник не может атаковать")
        unit.receiveDamage(self._damage)

    def move(self, x: int, y: int) -> None:
        if not self.isAlive():
            raise ValueError("Погибший лучник не может двигаться")
        self._x = x
        self._y = y


class Building(GameObject):
    def __init__(self, name: str, x: int, y: int, built: bool = False):
        super().__init__(name, x, y)
        self._built = built

    def isBuilt(self) -> bool:
        return self._built

    def build(self) -> None:
        self._built = True


class Fort(Building, Attacker):
    def __init__(self, name: str, x: int, y: int,
                 built: bool = False, damage: float = 40.0):
        super().__init__(name, x, y, built)
        if damage < 0:
            raise ValueError("Урон не может быть отрицательным")
        self._damage = float(damage)

    def attack(self, unit: Unit) -> None:
        if not self.isBuilt():
            raise ValueError("Сначала нужно построить крепость")
        unit.receiveDamage(self._damage)


class MobileHouse(Building, Moveable):
    def move(self, x: int, y: int) -> None:
        if not self.isBuilt():
            raise ValueError("Сначала нужно построить дом")
        self._x = x
        self._y = y
