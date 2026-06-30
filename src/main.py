import asyncio
import sys

import pygame

from src.database import AsyncSessionLocal
from src.models import Player
from src.game import Snake, Apple, handle_keys
import src.settings as settings

from sqlalchemy import select


pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)  # Уменьшенный шрифт


# ──────────────────────────────────────────── Работа с БД ────────────────────────────────────────────

async def get_or_create_player(name: str) -> Player:
    """Получить игрока по имени или создать нового"""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Player).filter(Player.name == name))
        player = result.scalars().first()

        if not player:
            player = Player(name=name)
            db.add(player)
            await db.commit()

        return player


async def update_score(name: str, score: int) -> int:
    """Обновить рекорд игрока. Возвращает лучший результат"""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Player).filter(Player.name == name))
        player = result.scalars().first()

        if not player:
            player = Player(name=name, high_score=0, games_played=0)
            db.add(player)

        if player.high_score is None or score > player.high_score:
            player.high_score = score
        
        player.games_played += 1
        await db.commit()
        return player.high_score


async def get_top_players(limit: int = 10) -> list[Player]:
    """Получить топ игроков по рекорду"""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(Player).order_by(Player.high_score.desc()).limit(limit)
        )
        return list(result.scalars().all())


# ──────────────────────────────────────────── Экраны ────────────────────────────────────────────

def draw_text_centered(text: str, y: int, color=settings.TEXT_COLOR) -> None:
    """Отрисовать текст по центру экрана"""
    surface = font.render(text, True, color)
    text_rect = surface.get_rect(center=(settings.SCREEN_WIDTH // 2, y))
    screen.blit(surface, text_rect)


def draw_text_top_left(text: str, x: int, y: int, color=settings.TEXT_COLOR) -> None:
    """Отрисовать текст в указанной позиции (левый верхний угол)"""
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def get_player_name() -> str:
    """Экран ввода имени игрока"""
    name = ""

    while True:
        screen.fill(settings.BOARD_BACKGROUND_COLOR)
        draw_text_centered("Введите имя:", settings.SCREEN_HEIGHT // 2 - 50)
        draw_text_centered(name + "_", settings.SCREEN_HEIGHT // 2 - 20)
        draw_text_centered("Enter - продолжить", settings.SCREEN_HEIGHT // 2 + 30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key != pygame.K_RETURN and len(name) < settings.PLAYER_NAME_LENGTH:
                    name += event.unicode

        pygame.display.update()
        clock.tick(30)

    return ""


def show_game_over(score: int, high_score: int) -> bool:
    """Экран завершения игры. Возвращает True для рестарта"""
    while True:
        screen.fill(settings.BOARD_BACKGROUND_COLOR)
        draw_text_centered("Игра окончена!", settings.SCREEN_HEIGHT // 2 - 60)
        draw_text_centered(f"Счёт: {score}", settings.SCREEN_HEIGHT // 2 - 30)
        draw_text_centered(f"Рекорд: {high_score}", settings.SCREEN_HEIGHT // 2)
        draw_text_centered("R - рестарт", settings.SCREEN_HEIGHT // 2 + 30)
        draw_text_centered("Q - выход", settings.SCREEN_HEIGHT // 2 + 55)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False

        pygame.display.update()
        clock.tick(30)

    return False


async def show_top_scores() -> None:
    """Показать таблицу рекордов"""
    top_players = await get_top_players()

    while True:
        screen.fill(settings.BOARD_BACKGROUND_COLOR)
        draw_text_centered("Таблица рекордов:", 20)

        if not top_players:
            draw_text_centered("Пока нет рекордов", settings.SCREEN_HEIGHT // 2)
        else:
            for i, player in enumerate(top_players[:10], 1):
                name_short = player.name[:20]
                text = f"{i}. {name_short}: {player.high_score}"

                # Выбираем цвет в зависимости от места
                if i == 1:
                    color = settings.GOLD_COLOR
                elif i == 2:
                    color = settings.SILVER_COLOR
                elif i == 3:
                    color = settings.BRONZE_COLOR
                else:
                    color = settings.TEXT_COLOR

                draw_text_centered(text, 30 + i * 28, color)

        draw_text_centered("Нажмите любую клавишу, чтобы играть...", settings.SCREEN_HEIGHT - 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

        pygame.display.update()
        clock.tick(30)


# ──────────────────────────────────────────── Игровой цикл ────────────────────────────────────────────

async def game_loop(player_name: str) -> None:
    """Основной игровой цикл"""
    await show_top_scores()

    while True:
        snake = Snake()
        apple = Apple()
        apple.randomize_position(snake.positions)
        score = 0
        speed = settings.SPEED

        running = True
        while running:
            clock.tick(speed)
            handle_keys(snake)
            snake.update_direction()
            snake.move()
            score = snake.length - 1
            
            # Ускорение каждые 10 очков, максимум SPEED + 10
            speed = settings.SPEED + min(score // 10, 10)

            # Проверка на съедание яблока
            if snake.get_head_position() == apple.position:
                snake.grow_flag = True
                snake.darken()
                apple.randomize_position(snake.positions)

            # Отрисовка
            screen.fill(settings.BOARD_BACKGROUND_COLOR)
            snake.draw(screen)
            apple.draw(screen)

            # Счёт в левом верхнем углу
            draw_text_top_left(f"{player_name}: {score}", 5, 5)

            pygame.display.update()

            # Конец игры при столкновении
            if snake.collision:
                running = False

        # Сохранение результата
        high_score = await update_score(player_name, score)

        # Экран Game Over
        if not show_game_over(score, high_score):
            break


def main() -> None:
    """Точка входа"""
    player_name = get_player_name()
    asyncio.run(game_loop(player_name))


if __name__ == '__main__':
    main()
