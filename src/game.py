from abc import ABC, abstractmethod
from random import randint, choice

import pygame

import src.settings as settings


class GameObject(ABC):
    """Абстрактный базовый класс для игровых объектов"""

    def __init__(self, body_color: pygame.Color):
        self.position = ((settings.SCREEN_WIDTH // 2), (settings.SCREEN_HEIGHT // 2))
        self.body_color = body_color

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        raise NotImplementedError


class Apple(GameObject):
    """Класс Яблоко"""

    def __init__(self):
        super().__init__(settings.APPLE_COLOR)
        self.position = (0, 0)

    def randomize_position(self, occupied_positions=None):
        """Сгенерировать позицию, не занятую змейкой"""
        while True:
            position = (
                randint(0, settings.GRID_WIDTH - 1) * settings.GRID_SIZE,
                randint(0, settings.GRID_HEIGHT - 1) * settings.GRID_SIZE
            )
            if occupied_positions is None or position not in occupied_positions:
                self.position = position
                return

    def draw(self, surface):
        """Отобразить яблоко на игровом поле"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (settings.GRID_SIZE, settings.GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, settings.BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Змейка"""

    def __init__(self, body_color=settings.SNAKE_BODY_COLOR) -> None:
        super().__init__(body_color)
        self.positions: list[tuple[int, int]] = [self.position]
        self.direction: tuple[int, int] = settings.RIGHT
        self.next_direction: tuple[int, int] | None = None
        self.length: int = 1
        self.tail_to_delete: tuple[int, int] | None = None
        self.grow_flag: bool = False
        self.collision: bool = False

    def update_direction(self):
        """Задать новое направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Отвечает за логику движения змейки"""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        head_new_position = (
            (head_x + (direction_x * settings.GRID_SIZE)) % settings.SCREEN_WIDTH,
            (head_y + (direction_y * settings.GRID_SIZE)) % settings.SCREEN_HEIGHT
        )

        self.positions.insert(0, head_new_position)

        if head_new_position in self.positions[1:]:
            self.collision = True
            return

        if not self.grow_flag:
            self.tail_to_delete = self.positions.pop()
        else:
            self.tail_to_delete = None
            self.grow_flag = False
            self.length += 1

    def get_head_position(self):
        """Получить координаты головы змейки"""
        return self.positions[0]

    def reset(self):
        """Вернуть змейку в исходное состояние"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([settings.UP, settings.DOWN, settings.LEFT, settings.RIGHT])
        self.collision = False
        self.body_color = settings.SNAKE_BODY_COLOR

    def draw(self, surface):
        """Отобразить змейку на игровом поле"""
        for position in self.positions[1:]:
            rect = pygame.Rect(
                (position[0], position[1]),
                (settings.GRID_SIZE, settings.GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, settings.BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (settings.GRID_SIZE, settings.GRID_SIZE))
        pygame.draw.rect(surface, settings.SNAKE_HEAD_COLOR, head_rect)
        pygame.draw.rect(surface, settings.BORDER_COLOR, head_rect, 1)

        if self.tail_to_delete:
            last_rect = pygame.Rect(
                (self.tail_to_delete[0], self.tail_to_delete[1]),
                (settings.GRID_SIZE, settings.GRID_SIZE)
            )
            pygame.draw.rect(surface, settings.BOARD_BACKGROUND_COLOR, last_rect)

    def darken(self) -> None:
        """Затемнить цвет змейки на 1 тон"""
        # Уменьшаем каждый канал на 6, но не ниже 0
        r = max(0, self.body_color.r - 6)
        g = max(0, self.body_color.g - 6)
        b = max(0, self.body_color.b - 6)
        self.body_color = pygame.Color(r, g, b)


def handle_keys(snake: Snake) -> None:
    """Обработка действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != settings.DOWN:
                snake.next_direction = settings.UP
            elif event.key == pygame.K_DOWN and snake.direction != settings.UP:
                snake.next_direction = settings.DOWN
            elif event.key == pygame.K_LEFT and snake.direction != settings.RIGHT:
                snake.next_direction = settings.LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != settings.LEFT:
                snake.next_direction = settings.RIGHT
