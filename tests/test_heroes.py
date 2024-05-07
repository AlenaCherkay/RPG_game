import unittest
from heroes import Healer, Hero, Attacker, Tank
from monsters import MonsterBerserk, MonsterHunter


class TestHealer(unittest.TestCase):
  """
    Тесты для методов класса Healer
  """

  def setUp(self):
    """Создает объект класса"""

    self.healer = Healer("Лекарь")
    self.mob_warrior = MonsterBerserk("Вредина")
    self.mob_ranger = MonsterHunter("Рейнджер")

    self.max_hp = 150
    self.start_power = 10
    self.magic_power = self.start_power * 3
    self.madness = 1

    self.tank = Tank("Танк Пётр")
    second_tank = Attacker("Убийца Траур")
    attacker = Attacker("Убийца Ольга")
    second_healer = Healer("Лекарь Игнат")

    self.good_team = [self.tank, second_tank, attacker, second_healer, self.healer]
    self.evil_team = [self.mob_warrior, self.mob_ranger]


  def test_inheritance(self):
    """ Проверяет правильность наследования значений от родительского класса (Hero)"""

    self.assertEqual(self.healer.get_hp(), self.max_hp)
    self.assertEqual(self.healer.get_power(), self.start_power)
    self.assertTrue(Hero.is_alive(self.healer))


  def test_damage(self):
    """ Проверяет правильность работы механизма получения урона"""

    factor = 1.2

    self.healer.take_damage(self.start_power)
    self.assertEqual(self.healer.get_hp(), (self.max_hp - self.start_power * factor))
    # print(self.healer.get_hp(), (self.max_hp - power * factor))


  def test_attack(self):
    """ Проверяет правильность работы механизма нанесения урона (атака).
        Проверяет что монстр получает правильный урон от атаки героя

    """

    self.healer.attack(self.mob_warrior)
    self.assertEqual(self.mob_warrior.get_hp(), self.max_hp - self.healer.get_power() / 2 * (self.madness / 2))


  def test_healing(self):
    """ Поверяет правильность работы метода - исцеление"""

    new_hp = self.healer.get_hp() + self.magic_power
    # Лечение
    self.healer.healing(self.healer)
    self.assertEqual(self.healer.get_hp(), new_hp)
    # print(self.healer.get_hp(), new_hp)


  def test_make_move_attack(self):
    """Проверяет правильность выполнения действий"""

    # Действие - АТАКА
    # Атака лекаря на монстра self.max_hp - self.healer.get_power() / 2 * (self.madness / 2)) =  147.5 (150 - 2.5 ед здоровья)
    self.healer.make_a_move(self.good_team, self.evil_team)
    self.assertEqual(self.mob_warrior.get_hp(), 147.5)
    # Проверяет что в конце действия меняется значение magic_power
    self.assertEqual(self.healer.magic_power, self.healer.get_power() * 3)

  def test_make_move_healing(self):
    """Проверяет правильность выполнения действий"""

    # Действие - ЛЕЧЕНИЕ
    new_hp = 20
    self.tank.set_hp(new_hp)
    self.healer.make_a_move(self.good_team, self.evil_team)
    # print(self.tank.get_hp())
    self.assertEqual(self.tank.get_hp(), new_hp + self.magic_power)
    # Проверяет что в конце действия меняется значение magic_power
    self.assertEqual(self.healer.magic_power, self.healer.get_power() * 3)


if __name__ == '__main__':
  unittest.main()