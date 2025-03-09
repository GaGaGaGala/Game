"""
Базовый класс башни и его наследники для разных типов башен, содержит логику стрельбы,
поиска цели и улучшения.
Каждая башня имеет следующие характеристики:
- Позиция: координаты расположения на игровом поле.
- Урон: величина урона, наносимого врагам.
- Дальность: максимальное расстояние, на которое башня может атаковать.
- Скорострельность: время между выстрелами.
"""
import pygame
from bullet import Bullet
import math
from settings import Settings


class Tower(pygame.sprite.Sprite):
    """Базовый класс для всех башен, его методы включают инициализацию, отрисовку, обновление, стрельбу, поворот
к цели и поиск цели."""
    def __init__(self, position, game):
        super().__init__()
        self.settings = Settings()
        self.position = pygame.math.Vector2(position)
        self.game = game

        # Характеристики башни
        self.image = None
        self.rect = None
        self.tower_range = 0  # Радиус действия башни
        self.damage = 0   # Урон
        self.rate_of_fire = 0    # Скорострельность в миллисекундах (интервал между выстрелами)
        self.last_shot_time = pygame.time.get_ticks()  # Время последнего выстрела
        self.level = 1  # Уровень башни

        self.original_image = self.image
        self.rotation_angle = 0

    def upgrade_cost(self):
        return 100 * self.level

    def upgrade(self):
        """
        Улучшение уровня башни. Увеличивает урон и скорострельность на 20%.
        """
        # Проверяем, достаточно ли денег для улучшения
        if self.game.settings.starting_money >= self.upgrade_cost():
            # Списываем деньги
            self.game.settings.starting_money -= self.upgrade_cost()

            # Увеличиваем уровень башни
            self.level += 1

            # Увеличиваем характеристики башни
            self.damage = int(self.damage * 1.2)  # Увеличиваем урон на 20%
            self.rate_of_fire = int(self.rate_of_fire * 0.8)  # Увеличиваем скорострельность (уменьшение интервала)

            print(f"Башня улучшена до уровня {self.level}. Новый урон: {self.damage}, "
                  f"новая скорострельность: {self.rate_of_fire} мс.")
        else:
            print("Недостаточно денег для улучшения башни.")

    def is_hovered(self, mouse_pos):
        """
        Проверяет, находится ли курсор мыши над башней.
        :param mouse_pos: Позиция мыши.
        :return: True, если курсор над башней, иначе False.
        """
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)  #Отображение информации о башне на экране.
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            level_text = self.game.font.render(f"Level: {self.level}", True, (255, 255, 255))
            upgrade_cost_text = self.game.font.render(f"Upgrade: ${self.upgrade_cost()  }", True, (255, 255, 255))

            level_text_pos = (self.rect.centerx, self.rect.top - 20)
            upgrade_cost_text_pos = (self.rect.centerx, self.rect.top - 40)

            screen.blit(level_text, level_text_pos)
            screen.blit(upgrade_cost_text, upgrade_cost_text_pos)

    def update(self, enemies, current_time, bullets_group):

        # Ищем ближайшую цель
        target = self.find_target(enemies)
        if target:
            self.rotate_towards(target.position)
        # Проверяем, может ли башня стрелять
            if current_time - self.last_shot_time >= self.rate_of_fire:
                self.last_shot_time = current_time
                self.shoot(target, bullets_group)
                bullet = Bullet(self.position, target.position, self.damage, self.game)
                bullets_group.add(bullet)

    def shoot(self, target, bullets_group):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.rate_of_fire:
            self.last_shot_time = current_time
            target.take_damage(self.damage)

    def rotate_towards(self, target_position):
        dx = target_position.x - self.position.x
        dy = target_position.y - self.position.y
        # Вычисляем угол в радианах
        self.rotation_angle = (180 / math.pi) * -math.atan2(dy, dx)
        # Преобразуем радианы в градусы
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(center=self.position)

    def find_target(self, enemies):
        nearest_enemy = None
        min_distance = float('inf')
        for enemy in enemies:
            distance = self.position.distance_to(enemy.position)
            if distance < min_distance and distance <= self.tower_range:
                nearest_enemy = enemy
                min_distance = distance
        return nearest_enemy


class BasicTower(Tower):
    """ Реализации башен, расширяющие базовый класс."""
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/basic_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 150 #диапазон
        self.damage = 20 #повреждения
        self.rate_of_fire = 1000 #скорострельность

    def shoot(self, target, bullets_group):
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class SniperTower(Tower):
    """ Снайперская башня имеет собственный алгоритм выбора цели."""
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/sniper_tower.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.tower_range = 300
        self.damage = 40
        self.rate_of_fire = 2000

    def find_target(self, enemies):
        healthiest_enemy = None
        max_health = 0
        for enemy in enemies:
            if self.position.distance_to(enemy.position) <= self.tower_range and enemy.health > max_health:
                healthiest_enemy = enemy
                max_health = enemy.health
        return healthiest_enemy

    def shoot(self, target, bullets_group):
        new_bullet = Bullet(self.position, target.position, self.damage, self.game)
        bullets_group.add(new_bullet)


class MoneyTower(Tower):
    """Класс денежной башни, генерирующей деньги для игрока с заданной скоростью."""
    def __init__(self, position, game):
        super().__init__(position, game)
        self.image = pygame.image.load('assets/towers/money_tower.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.money_generation_rate = 10  # Количество генерируемых денег
        self.generation_interval = 1000  # Интервал генерации в миллисекундах
        self.last_generation_time = pygame.time.get_ticks()

    def update(self, enemies, current_time, bullets_group):
        if current_time - self.last_generation_time > self.generation_interval:
            self.generate_money()
            self.last_generation_time = current_time

    def generate_money(self):
        """
        Генерирует деньги для игрока, увеличивая его текущую сумму денег.
        """
        self.game.settings.starting_money += self.money_generation_rate
