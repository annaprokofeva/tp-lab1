"""Запуск: python main.py из папки lab2."""

from game import Archer, Attacker, Fort, GameObject, MobileHouse, Moveable


def describe(obj: GameObject) -> None:
    print(f"#{obj.getId()} {obj.getName()}: ({obj.getX()}, {obj.getY()})")


def main() -> None:
    archer = Archer("Лучник", 0, 0)
    enemy = Archer("Вражеский лучник", 5, 5)
    fort = Fort("Крепость", 10, 10)
    house = MobileHouse("Дом на колёсах", 2, 2)

    print("Игровые объекты:")
    for obj in (archer, enemy, fort, house):
        describe(obj)

    print(f"Крепость построена: {fort.isBuilt()}")
    fort.build()
    house.build()
    print(f"Крепость после build(): {fort.isBuilt()}")

    print("\nПеремещение через общий интерфейс Moveable:")
    movers: list[Moveable] = [archer, house]
    for mover in movers:
        mover.move(3, 4)
    describe(archer)
    describe(house)

    print("\nАтаки через общий интерфейс Attacker:")
    attackers: list[Attacker] = [archer, fort]
    for attacker in attackers:
        attacker.attack(enemy)
        print(f"Здоровье противника: {enemy.getHp()}")

    fort.attack(enemy)
    print(f"После последнего выстрела: HP={enemy.getHp()}, жив={enemy.isAlive()}")


if __name__ == "__main__":
    main()
