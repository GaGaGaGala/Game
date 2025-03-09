"""Файл настроек, содержит параметры конфигурации игры, такие как размеры экрана, стоимость и параметры башен,
пути к ресурсам и т.д."""
import random


class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.rows = 10
        self.cols = 15
        self.grid_size = (64, 64)

        self.tower_costs = {
            'basic': 100,
            'sniper': 150,
            'money': 200,
        }
        self.tower_upgrade_cost = 150
        self.tower_sell_percentage = 0.75
        self.enemy_path1 =  [
            (50, 400), (300, 400), (300, 200), (600, 200),
            (600, 600),(900, 600), (900, 300), (1150, 300)
        ]

        """Дополнительные пути врага."""
        self.enemy_path2 = [
            (0, 200), (150, 200), (150, 100), (300, 100),
            (300, 300), (450, 300), (900, 300), (1150, 300)
        ]
        self.enemy_path3 = [
            (0, 400), (150, 400), (150, 500), (500, 500),
            (500, 600), (800, 600), (800, 500), (1150, 500)
        ]
        self.enemy_path4 = [
            (100, 900), (100, 600), (600, 600), (600, 300),
            (1000, 300), (1000, 700), (1400, 700), (1400, 900)

        ]
        self.enemy_path5 = [
            (500, 50), (500, 400), (900, 400), (900, 600),
            (400, 600), (400, 300), (200, 300), (200, 900)

        ]

        self.tower_sprites = {
            'basic': 'assets/towers/basic_tower.png',
            'sniper': 'assets/towers/sniper_tower.png',
            'money': 'asserts/towers/money_tower.png',
        }
        self.enemy_sprites = {
            'base': 'assets/enemies/basic_enemy.png',
            'fast': 'assets/enemies/fast_enemy.png',
            'strong': 'assets/enemies/strong_enemy.png',
            'boss': 'assets/enemies/boss_enemy.png',
        }
        self.bullet_sprite = 'assets/bullets/basic_bullet.png'
        self.background_image = 'assets/backgrounds/bg.jpg'#game_background.png'

        self.shoot_sound = 'assets/sounds/shoot.wav'
        self.upgrade_sound = 'assets/sounds/upgrade.wav'
        self.sell_sound = 'assets/sounds/sell.wav'
        self.enemy_hit_sound = 'assets/sounds/enemy_hit.wav'
        self.background_music = 'assets/sounds/background_music.mp3'
        self.spawn_sound = 'assets/sounds/spawn.wav'
        self.starting_money = 3000
        self.lives = 20

        self.tower_positions = [(x * self.grid_size[0] + self.grid_size[0] // 2, y * self.grid_size[1] + self.grid_size[1] // 2)
                                for x in range(1, self.cols) for y in range(3, self.rows)]
