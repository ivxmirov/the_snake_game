# Размеры поля и сетки
import pygame


SCREEN_HEIGHT = 360
SCREEN_WIDTH = 360
PANEL_HEIGHT = 60  # Панель для текста снизу
WINDOW_HEIGHT = SCREEN_HEIGHT + PANEL_HEIGHT

GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = pygame.Color(0, 0, 0)
BORDER_COLOR = pygame.Color(93, 216, 228)
APPLE_COLOR = pygame.Color(248, 24, 148)
SNAKE_BODY_COLOR = pygame.Color(0, 255, 0)
SNAKE_HEAD_COLOR = pygame.Color(0, 100, 0)
TEXT_COLOR = pygame.Color(255, 255, 255)
PANEL_COLOR = pygame.Color(30, 30, 30)
GOLD_COLOR = pygame.Color(255, 215, 0)
SILVER_COLOR = pygame.Color(192, 192, 192)
BRONZE_COLOR = pygame.Color(205, 127, 50)

# Скорость
SPEED = 10
