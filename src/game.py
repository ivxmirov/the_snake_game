from abc import ABC, abstractmethod
import sys
from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 360, 360
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона и цвета игровых объектов
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (248, 24, 148)
SNAKE_BODY_COLOR = (0, 255, 0)
SNAKE_HEAD_COLOR = (0, 100, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject(ABC):
    """Абстрактный базовый класс для классов игровых объектов"""

    def __init__(self, body_color: pygame.Color):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        """Отобрази объект на игровом поле"""
        raise NotImplementedError


class Apple(GameObject):
    """Класс Яблоко."""
    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = (0, 0)  # Временная позиция до генерации случайной позиции

    def randomize_position(self, occupied_positions=None):
        """Сгенерировать позицию, не занятую змейкой"""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if occupied_positions is None or position not in occupied_positions:
                self.position = position
                return

    def draw(self, surface):
        """Отобразить яблоко на игровом поле"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Змейка"""

    def __init__(self, body_color=SNAKE_BODY_COLOR) -> None:
        super().__init__(body_color)
        self.positions: list[tuple[int, int]] = [self.position]
        self.direction: tuple[int, int] = RIGHT
        self.next_direction: tuple[int, int] | None = None
        self.length: int = 1
        # Это координаты хвоста, который нужно стереть с экрана
        self.tail_to_delete: tuple[int, int] | None = None
        self.grow_flag: bool = False

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
            (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        )

        # На каждом ходу добавляем новую голову в начало списка
        self.positions.insert(0, head_new_position)

        # Если голова змейки врезалась в туловище, то сбросить змейку к начальному состоянию
        if head_new_position in self.positions[1:]:
            self.reset()
            return

        # Если змейка не выросла на текущем ходу, то удаляем хвост
        if not self.grow_flag:
            self.tail_to_delete = self.positions.pop()
        # Если змейка выросла на текущем ходу, то хвост не удаляем
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
        self.direction = choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        """Отобразить змейку на игровом поле"""
        for position in self.positions[1:]:
            rect = pygame.Rect(
                (position[0], position[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, SNAKE_HEAD_COLOR, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.tail_to_delete:
            last_rect = pygame.Rect(
                (self.tail_to_delete[0], self.tail_to_delete[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def grows(self, apple: Apple):
        """Проверить, съела ли змейка яблоко. Сгенерировать новое яблоко"""
        head_pos = self.get_head_position()
        if head_pos == apple.position:
            self.grow_flag = True
            apple.randomize_position(self.positions)


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Логика игры"""
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.grows(apple)

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
