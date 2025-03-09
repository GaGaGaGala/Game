import pygame
from enemy import EnemyBase, FastEnemy, StrongEnemy, BossEnemy
from tower import BasicTower, SniperTower, MoneyTower
import random

"""содержит логику уровня, управление волнами врагов, их спавн, а также расстановку башен и обработку коллизий."""


class LevelBase:
    """Базовый класс для уровней игры.Управляет уровнем игры, волнами врагов и расстановкой башен."""
    def __init__(self, game):
        """Инициализирует уровень игры."""
        self.game = game
        self.enemies = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        # Определяется в наследниках
        self.enemy_paths = []
        self.random_path = [self.game.settings.enemy_path1, self.game.settings.enemy_path2, self.game.settings.enemy_path3,
                            self.game.settings.enemy_path4, self.game.settings.enemy_path5]
        self.waves = [
            [{'path': random.choice(self.random_path), 'speed': 1, 'health': 100,
              'image_path': 'assets/enemies/basic_enemy.png'}] * 5,
            [{'path': random.choice(self.random_path), 'speed': 1.5, 'health': 150,
              'image_path': 'assets/enemies/fast_enemy.png'}] * 7,
            [{'path': random.choice(self.random_path), 'speed': 0.75, 'health': 200,
              'image_path': 'assets/enemies/strong_enemy.png'}] * 4,
            [{'path': random.choice(self.random_path), 'speed': 2, 'health': 1000,
              'image_path': 'assets/enemies/boss_enemy.png'}] * 10,
        ]

        self.current_wave = 0
        self.spawned_enemies = 0
        self.spawn_delay = 1000
        self.last_spawn_time = pygame.time.get_ticks()
        self.all_waves_complete = False
        self.start_next_wave()
        self.spawn_sound = pygame.mixer.Sound("assets/sounds/spawn.wav")
        self.font = pygame.font.SysFont("Arial", 24)
        self.start_next_wave()

    def start_next_wave(self):
        """Запускает следующую волну врагов."""
        if self.current_wave < len(self.waves):
            self.spawned_enemies = 0
            self.spawn_next_enemy()

    def spawn_next_enemy(self):
        """Генерирует следующего врага текущей волны."""
        if self.spawned_enemies < len(self.waves[self.current_wave]):
            enemy_info = self.waves[self.current_wave][self.spawned_enemies]
            new_enemy = EnemyBase(**enemy_info, game=self.game)
            self.enemies.add(new_enemy)
            self.spawned_enemies += 1

    def attempt_place_tower(self, mouse_pos, tower_type):
        """Пытается разместить башню выбранного типа в позиции курсора."""
        tower_classes = {'basic': BasicTower, 'sniper': SniperTower, 'money': MoneyTower}
        if tower_type in tower_classes and self.game.settings.starting_money >= self.game.settings.tower_costs[tower_type]:
            grid_pos = self.game.grid.get_grid_position(mouse_pos)
            if self.game.grid.is_spot_available(grid_pos):
                self.game.settings.starting_money -= self.game.settings.tower_costs[tower_type]
                new_tower = tower_classes[tower_type](grid_pos, self.game)
                self.towers.add(new_tower)
                print("Tower placed.")
            else:
                print("Invalid position for tower.")
        else:
            print("Not enough money or unknown tower type.")

    def update(self):
        """Обновляет состояние уровня, врагов, башен и пуль."""
        current_time = pygame.time.get_ticks()

        """Генерирует врагов."""
        if self.current_wave < len(self.waves) and self.spawned_enemies < len(self.waves[self.current_wave]):
            if current_time - self.last_spawn_time > self.spawn_delay:
                enemy_info = self.waves[self.current_wave][self.spawned_enemies].copy()
                enemy_info['game'] = self.game
                new_enemy = EnemyBase(**enemy_info)
                self.enemies.add(new_enemy)
                self.spawned_enemies += 1
                self.last_spawn_time = current_time

        """Обработка столкновений пуль и врагов."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, False)
        for bullet in collisions:
            for enemy in collisions[bullet]:
                enemy.take_damage(bullet.damage)

        """Обновление врагов, башен и пуль."""
        self.enemies.update()
        for tower in self.towers:
            tower.update(self.enemies, current_time, self.bullets)
        self.bullets.update()

        """Проверка завершения волны."""
        if len(self.enemies) == 0 and self.current_wave < len(self.waves) - 1:
            self.current_wave += 1
            self.start_next_wave()
        elif len(self.enemies) == 0 and self.current_wave == len(self.waves) - 1:
            self.all_waves_complete = True

    def draw(self, screen):
        """Отрисовывает уровень, включая врагов, башни и пули."""
        #pygame.draw.lines(screen, (0, 128, 0), False, random.choice(self.random_path), 5)
        pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path1, 5)
        pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path2, 5)
        pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path3, 5)
        pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path4, 5)
        pygame.draw.lines(screen, (0, 128, 0), False, self.game.settings.enemy_path5, 5)

        self.enemies.draw(screen)
        self.towers.draw(screen)
        self.bullets.draw(screen)
        mouse_pos = pygame.mouse.get_pos()
        for tower in self.towers:
            tower.draw(screen)
            if tower.is_hovered(mouse_pos):
                tower_stats_text = self.font.render(f"Damage: {tower.damage}, Range: {tower.tower_range}", True,
                                                    (255, 255, 255))
                screen.blit(tower_stats_text, (tower.rect.x, tower.rect.y - 20))


class Level1(LevelBase):
    def __init__(self, game):
        super().__init__(game)
        self.enemy_paths = self.random_path
        self.waves = [
            [{'path': random.choice(self.enemy_paths), 'speed': 1, 'health': 100, 'image_path': 'assets/enemies/basic_enemy.png', 'reward': 10}] * 5,
            [{'path': random.choice(self.enemy_paths), 'speed': 2, 'health': 50, 'image_path': 'assets/enemies/fast_enemy.png', 'reward': 15}] * 10,
            [{'path': random.choice(self.enemy_paths), 'speed': 1, 'health': 200, 'image_path': 'assets/enemies/strong_enemy.png', 'reward': 30}] * 4,
            [{'path': random.choice(self.enemy_paths), 'speed': 1, 'health': 300, 'image_path': 'assets/enemies/strong_enemy.png', 'reward': 40}] * 3,
            [{'path': random.choice(self.enemy_paths), 'speed': 0.5, 'health': 500, 'image_path': 'assets/enemies/boss_enemy.png', 'reward': 100}] * 1,
        ]


class Level2(LevelBase):
    def __init__(self, game):
        super().__init__(game)
        self.enemy_paths = self.random_path
        self.waves = [
            [{'path': random.choice(self.enemy_paths), 'speed': 3, 'health': 50, 'image_path': 'assets/enemies/fast_enemy.png', 'reward': 15}] * 8,
            [{'path': random.choice(self.enemy_paths), 'speed': 1, 'health': 200, 'image_path': 'assets/enemies/strong_enemy.png', 'reward': 30}] * 6,
            [{'path': random.choice(self.enemy_paths), 'speed': 1.5, 'health': 150, 'image_path': 'assets/enemies/strong_enemy.png', 'reward': 25}] * 5,
            [{'path': random.choice(self.enemy_paths), 'speed': 0.8, 'health': 400, 'image_path': 'assets/enemies/boss_enemy.png', 'reward': 100}] * 2,
        ]


class Level3(LevelBase):
    def __init__(self, game):
        super().__init__(game)
        self.enemy_paths = self.random_path
        self.waves = [
            [{'path': random.choice(self.enemy_paths), 'speed': 1.3, 'health': 100, 'image_path': 'assets/enemies/basic_enemy.png', 'reward': 10}] * 5,
            [{'path': random.choice(self.enemy_paths), 'speed': 3, 'health': 50, 'image_path': 'assets/enemies/fast_enemy.png', 'reward': 15}] * 6,
            [{'path': random.choice(self.enemy_paths), 'speed': 1.5, 'health': 200, 'image_path': 'assets/enemies/strong_enemy.png', 'reward': 30}] * 4,
            [{'path': random.choice(self.enemy_paths), 'speed': 0.5, 'health': 500, 'image_path': 'assets/enemies/boss_enemy.png', 'reward': 100}] * 1,
            [{'path': random.choice(self.enemy_paths), 'speed': 2, 'health': 150, 'image_path': 'assets/enemies/fast_enemy.png', 'reward': 20}] * 5,
        ]