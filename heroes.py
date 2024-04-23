import random


class Hero:
    """
    Базовый класс
    """
    # У каждого наследника будут атрибуты:
    # - Имя
    # - Здоровье
    # - Сила
    # - Жив ли объект
    # Каждый наследник будет уметь:
    # - Атаковать
    # - Получать урон
    # - Выбирать действие для выполнения
    # - Описывать своё состояние

    max_hp = 150
    start_power = 10

    def __init__(self, name):
        """
        Конструктор класса
        :param name:
        """
        self.name = name
        self.__hp = self.max_hp
        self.__power = self.start_power
        self.__is_alive = True

    def get_hp(self):
        """
        геттер - возвращает значение
        :return: self.__hp
        """
        return self.__hp

    def set_hp(self, new_value):
        """
        сеттер - изменяет значение
        :param new_value:
        """
        self.__hp = max(new_value, 0)

    def get_power(self):
        """
        геттер - возвращает значение
        :return: self.__power
        """
        return self.__power

    def set_power(self, new_power):
        """
        сеттер - изменяет значение
        :param new_power:
        """
        self.__power = new_power

    def is_alive(self):
        """
        геттер - возвращает состояние
        :return: self.__is_alive
        """
        return self.__is_alive

    # Все наследники должны будут переопределять каждый метод базового класса (кроме геттеров/сеттеров)
    # Переопределенные методы должны вызывать методы базового класса (при помощи super).
    # Методы attack и __str__ базового класса можно не вызывать (т.к. в них нету кода).
    # Они нужны исключительно для наглядности.
    # Метод make_a_move базового класса могут вызывать только герои, не монстры.
    def attack(self, target):
        """
        Описывает действие при атаке
        :param target:
        """
        # Каждый наследник будет наносить урон согласно правилам своего класса
        raise NotImplementedError("Вы забыли переопределить метод Attack!")

    def take_damage(self, damage):
        """
        Выводит сообщение с оставшемся здоровьем, проверяет состояние  self.__is_alive
        :param damage:
        """
        # Каждый наследник будет получать урон согласно правилам своего класса
        # При этом у всех наследников есть общая логика, которая определяет жив ли объект.
        print("\t", self.name, "Получил удар с силой равной = ", round(damage), ". Осталось здоровья - ", round(self.get_hp()))
        # Дополнительные принты помогут вам внимательнее следить за боем и изменять стратегию, чтобы улучшить выживаемость героев
        if self.get_hp() <= 0:
            self.__is_alive = False

    def make_a_move(self, friends, enemies):
        """
        Увеличивает значение силы
        :param friends:
        :param enemies:
        """
        # С каждым днём герои становятся всё сильнее.
        self.set_power(self.get_power() + 0.1)

    def __str__(self):
        """
        Выводит информацию о состоянии персонажа
        """
        # Каждый наследник должен выводить информацию о своём состоянии, чтобы вы могли отслеживать ход сражения
        raise NotImplementedError("Вы забыли переопределить метод __str__!")


class Healer(Hero):
    """
    Дочерний класс, наследуется от Hero
    """
    # Целитель:
    # Атрибуты:
    # - магическая сила - равна значению НАЧАЛЬНОГО показателя силы умноженному на 3 (self.__power * 3)
    # Методы:
    # - атака - может атаковать врага, но атакует только в половину силы self.__power
    # - получение урона - т.к. защита целителя слаба - он получает на 20% больше урона (1.2 * damage)
    # - исцеление - увеличивает здоровье цели на величину равную своей магической силе
    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет ОДНО из действий (атака,
    # исцеление) на выбранную им цель
    def __init__(self, name):
        """Инициализация атрибутов класса"""
        super().__init__(name)
        self.magic_power = self.get_power() * 3

    def __str__(self):
        """
        Выводит информацию о состоянии персонажа
        """
        if self.is_alive() == True:
            is_alive = 'Жив'
        else:
            is_alive = 'Мертв'
        return 'имя {}, здоровье {},  магическая сила  {}, сила  {}, состояние {}'.format(
            self.name, self.get_hp(), self.magic_power, self.get_power(),  is_alive
        )

    # - атака
    def attack(self, target):
        """
        Наносит урон врагу
        :param target:
        """
        target.take_damage(self.get_power()/2)

    # - получение урона
    def take_damage(self, power):
        """
        Изменяет значение здоровья
        :param power:
        """
        self.set_hp(self.get_hp() - power * 1.2)
        super().take_damage(power)

    # - исцеление
    def healing(self, target):
        """
        Увеличивает здоровье цели
        :param target:
        :return:
        """
        target.set_hp(target.get_hp() + self.magic_power)


    def make_a_move(self, friends, enemies):
        """
        выбор действия - получает на вход всех союзников и всех врагов
        и на основе своей стратегии выполняет ОДНО из действий (атака,исцеление) на выбранную им цель
        :param friends:
        :param enemies:
        """
        print(self.name, end=' ')
        target_of_potion = friends[0]

        min_health = target_of_potion.get_hp()
        for friend in friends:
            if friend.get_hp() < min_health:
                target_of_potion = friend
                min_health = target_of_potion.get_hp()

        if min_health <= 80:
            print("Исцеляю", target_of_potion.name)
            self.healing(target_of_potion)
        else:
            if not enemies:
                return
            print("Атакую ближнего -", enemies[0].name)
            self.attack(enemies[0])
        print('\n')
        super().make_a_move(self, friends)
        self.magic_power = self.get_power() * 3



class Tank(Hero):
    """
    Дочерний класс, наследуется от Hero
    """
    # Танк:
    # Атрибуты:
    # - показатель защиты - изначально равен 1, может увеличиваться и уменьшаться
    # - поднят ли щит - танк может поднимать щит, этот атрибут должен показывать поднят ли щит в данный момент
    # Методы:
    # - атака - атакует, но т.к. доспехи очень тяжелые - наносит половину урона (self.__power)
    # - получение урона - весь входящий урон делится на показатель защиты (damage/self.defense) и только потом отнимается от здоровья
    # - поднять щит - если щит не поднят - поднимает щит. Это увеличивает показатель брони в 2 раза, но уменьшает показатель силы в 2 раза.
    # - опустить щит - если щит поднят - опускает щит. Это уменьшает показатель брони в 2 раза, но увеличивает показатель силы в 2 раза.
    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет ОДНО из действий (атака,
    # поднять щит/опустить щит) на выбранную им цель
    def __init__(self, name):
        """Инициализация атрибутов класса"""
        super().__init__(name)
        # показатель защиты
        self.defense = 1
        # поднят ли щит
        self.block = False

    def __str__(self):
        """
        Выводит информацию о состоянии персонажа
        """
        if self.is_alive() == True:
            is_alive = 'Жив'
        else:
            is_alive = 'Мертв'
        if  self.block == False:
            is_block = 'Опущен'
        else:
            is_block = 'Поднят'
        return 'имя {}, здоровье {},  сила  {}, показатель защиты: {}, щит:{}, состояние {}'.format(
            self.name, self.get_hp(), self.get_power(), self.defense, is_block, is_alive
        )

    # - атака
    def attack(self, target):
        """
        Наносит урон врагу
        :param target:
        """
        target.take_damage(self.get_power()/2)
        self.defense += 1

    # - получение урона
    # - получение урона - весь входящий урон делится на показатель защиты (damage/self.defense) и только потом отнимается от здоровья
    def take_damage(self, power):
        """
        Изменяет значение здоровья
        :param power:
        """
        # self.set_hp(self.get_power()/self.defense)
        self.set_hp(self.get_hp() - (power/self.defense))
        super().take_damage(power)

    # - поднять щит
    # - поднять щит - если щит не поднят - поднимает щит. Это увеличивает показатель брони в 2 раза, но
    # уменьшает показатель силы в 2 раза.
    def raise_the_shield(self):
        """
        Проверяет значение self.block, если щит не поднят - поднимает щит. Это увеличивает показатель брони в 2 раза, но
        уменьшает показатель силы в 2 раза
        """
        if self.block == False:
            self.block = True
            self.defense *= 2
            self.set_power(self.get_power()/2)

    # - опустить щит
    # - опустить щит - если щит поднят - опускает щит. Это уменьшает показатель брони в 2 раза,
    # но увеличивает показатель силы в 2 раза.
    def lower_the_shield(self):
        """
        Проверяет значение self.block, если щит поднят - опускает щит. Это уменьшает показатель брони в 2 раза,
        но увеличивает показатель силы в 2 раза.
        :return:
        """
        if self.block == True:
            self.block = False
            self.defense /= 2
            self.set_power(self.get_power() * 2)

    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет ОДНО из действий (атака,
    # поднять щит/опустить щит) на выбранную им цель
    def make_a_move(self, friends, enemies):
        """
        выбор действия - получает на вход всех союзников и всех врагов
        и на основе своей стратегии выполняет ОДНО из действий (атака,
        поднять щит/опустить щит) на выбранную им цель
        :param friends:
        :param enemies:
        """
        print(self.name, end=' ')
        if self.get_hp() < 70:
            self.raise_the_shield()
        else:
            if self.block == True:
                self.lower_the_shield()
                if enemies:
                    target = random.choice(enemies)
                    print(" Случайно атакую -", target.name)
                    print()
                    self.attack(target)
        super().make_a_move(self, friends)


class Attacker(Hero):
    """
    Дочерний класс, наследуется от Hero
    """
    # Убийца:
    # Атрибуты:
    # - коэффициент усиления урона (входящего и исходящего)
    # Методы:
    # - атака - наносит урон равный показателю силы (self.__power) умноженному на коэффициент усиления урона (self.power_multiply)
    # после нанесения урона - вызывается метод ослабления power_down.
    # - получение урона - получает урон равный входящему урона умноженному на половину коэффициента усиления урона - damage * (
    # self.power_multiply / 2)
    # - усиление (power_up) - увеличивает коэффициента усиления урона в 2 раза
    # - ослабление (power_down) - уменьшает коэффициента усиления урона в 2 раза
    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет
    # ОДНО из действий (атака,
    # усиление, ослабление) на выбранную им цель

    def __init__(self, name):
        """Инициализация атрибутов класса"""
        super().__init__(name)
        self.power_multiply = 2


    def __str__(self):
        """
        Выводит информацию о состоянии персонажа
        """
        if self.is_alive() == True:
            is_alive = 'Жив'
        else:
            is_alive = 'Мертв'

        return 'имя {}, здоровье {},  сила  {}, коэффициент усиления урона {}, состояние {}'.format(
            self.name, self.get_hp(), self.get_power(), self.power_multiply, is_alive
        )

    # - атака - наносит урон равный показателю силы (self.__power) умноженному на коэффициент усиления урона (self.power_multiply)
    # после нанесения урона - вызывается метод ослабления power_down.
    def attack(self, target):
        """
        Наносит урон врагу
        :param target:
        """
        target.take_damage(self.get_power() * self.power_multiply)
        self.power_down()

    # - получение урона - получает урон равный входящему урона умноженному на половину коэффициента усиления урона - damage * (
    # self.power_multiply / 2)
    def take_damage(self, power):
        """
        Изменяет значение здоровья
        :param power:
        """
        # self.set_hp(self.get_power()/self.defense)
        self.set_hp(self.get_hp() - (power * self.power_multiply / 2))
        super().take_damage(power)

    # - усиление (power_up) - увеличивает коэффициента усиления урона в 2 раза
    def power_up(self):
        """
        Увеличивает коэффициента усиления урона в 2 раза
        """
        self.power_multiply *= 2

    # - ослабление (power_down) - уменьшает коэффициента усиления урона в 2 раза
    def power_down(self):
        """
        Уменьшает коэффициента усиления урона в 2 раза
        """
        self.power_multiply /= 2


    # def make_a_move(self, friends, enemies):
    #     print(self.name, end=' ')
    #     choise = random.randint(1,2)
    #     if choise == 1:
    #         target = random.choice(friends)
    #         print(" Случайно услилваю -", target.name)
    #         print()
    #         self.power_up(target)
    #     else:
    #         target = random.choice(enemies)
    #         print(" Случайно ослабляю -", target.name)
    #         print()
    #         self.attack(target)

    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет
    # ОДНО из действий (атака,
    # усиление, ослабление) на выбранную им цель
    def make_a_move(self, friends, enemies):
        """
        выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет
        ОДНО из действий (атака,
        усиление, ослабление) на выбранную им цель
        :param friends:
        :param enemies:
        """
        print(self.name, end=' ')
        if self.power_multiply < 2:
            self.power_up()
            print(" Увеличиваю коэффициент усиления -", self.power_multiply)
        else:
            count_enemies = len(enemies) - 1
            print(count_enemies)
            target = enemies[count_enemies]
            print(" Атакую -", target.name)
            print()
            self.attack(target)
        super().make_a_move(self, friends)
        #     target = random.choice(enemies)
        #     print(" Случайно атакую -", target.name)
        #     print()
        #     self.attack(target)
        #     print('\n')
