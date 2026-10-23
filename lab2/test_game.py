import unittest

from game import Archer, Attacker, Fort, GameObject, MobileHouse, Moveable


class GameTests(unittest.TestCase):
    def test_identity_and_coordinates(self):
        first = GameObject("Первый", 2, 3)
        second = GameObject("Второй", 0, 0)
        self.assertNotEqual(first.getId(), second.getId())
        self.assertEqual((first.getName(), first.getX(), first.getY()),
                         ("Первый", 2, 3))

    def test_damage_and_death(self):
        attacker = Archer("Лучник", 0, 0, damage=25)
        target = Archer("Цель", 1, 1, hp=30)
        attacker.attack(target)
        self.assertEqual(target.getHp(), 5.0)
        attacker.attack(target)
        self.assertEqual(target.getHp(), 0.0)
        self.assertFalse(target.isAlive())
        with self.assertRaises(ValueError):
            target.move(2, 2)
        with self.assertRaises(ValueError):
            target.attack(attacker)

    def test_negative_damage_does_not_heal(self):
        unit = Archer("Лучник", 0, 0)
        with self.assertRaises(ValueError):
            unit.receiveDamage(-10)
        self.assertEqual(unit.getHp(), 100.0)

    def test_buildings_require_construction(self):
        fort = Fort("Крепость", 0, 0)
        house = MobileHouse("Дом", 1, 1)
        target = Archer("Цель", 5, 5)
        self.assertFalse(fort.isBuilt())
        with self.assertRaises(ValueError):
            fort.attack(target)
        with self.assertRaises(ValueError):
            house.move(2, 3)
        fort.build()
        house.build()
        fort.attack(target)
        house.move(2, 3)
        self.assertEqual(target.getHp(), 60.0)
        self.assertEqual((house.getX(), house.getY()), (2, 3))

    def test_interfaces_and_polymorphism(self):
        archer = Archer("Лучник", 0, 0)
        fort = Fort("Крепость", 1, 1, built=True)
        house = MobileHouse("Дом", 2, 2, built=True)
        target = Archer("Цель", 3, 3)
        for attacker in (archer, fort):
            self.assertIsInstance(attacker, Attacker)
            attacker.attack(target)
        self.assertEqual(target.getHp(), 40.0)
        for mover in (archer, house):
            self.assertIsInstance(mover, Moveable)
            mover.move(7, 8)
            self.assertEqual((mover.getX(), mover.getY()), (7, 8))
        self.assertNotIsInstance(fort, Moveable)
        self.assertNotIsInstance(house, Attacker)
        for interface in (Attacker, Moveable):
            with self.assertRaises(TypeError):
                interface()


if __name__ == "__main__":
    unittest.main()
