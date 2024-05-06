from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:

DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Начальный цвет
DEFAULT_COLOR = (100, 100, 100)

# Скорость движения змейки:
SPEED = 12

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_quit(event):
    """Обрабатывает закрытие игры."""
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                     and event.key == pygame.K_ESCAPE):
        pygame.quit()
        raise SystemExit


def handle_keys(game_object):
    """Обрабатывает нажатие клавиш."""
    for event in pygame.event.get():
        handle_quit(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


class GameObject:
    """Базовый класс."""

    def __init__(self, position=None, body_color=DEFAULT_COLOR) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Нарисовать объект ЦЕЛИКОМ."""
        raise NotImplementedError(
            f'Определите draw в {self.__class__.__name__}.')

    def draw_cell(self, position):
        """Нарисовать 1 ячейку"""
        self.position = position
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        return rect


class Apple(GameObject):
    """Яблоко."""

    def __init__(self) -> None:
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_positions=None):
        """Задать рандомное значение позиции яблока."""
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)
        while snake_positions is not None and self.position in snake_positions:
            self.randomize_position(snake_positions)
        return self.position

    def draw(self):
        """Нарисовать яблоко."""
        pygame.draw.rect(screen, self.body_color,
                         self.draw_cell(self.position))
        pygame.draw.rect(screen, BORDER_COLOR,
                         self.draw_cell(self.position), 1)


class Snake(GameObject):
    """Змейка."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = SNAKE_COLOR
        self.reset()

    def update_direction(self, direction):
        """Обновляет направление движения."""
        self.direction = direction

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def draw(self):
        """Отрисовка змейки."""
        pygame.draw.rect(screen, self.body_color,
                         self.draw_cell(self.get_head_position()))
        pygame.draw.rect(screen, BORDER_COLOR,
                         self.draw_cell(self.get_head_position()), 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Возвращает змейку в начальное состояние."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions = [self.position]
        self.length = 1
        self.last = None
        self.direction = RIGHT

    def move(self):
        """Метод отвечающий за передвижение змейки."""
        head_x, head_y = self.get_head_position()
    # новая_позиция = (старая_позиция + смещение) % размер окна
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

    def get_new_head(self):
        """Добавляет новую часть тела."""
        return self.positions.insert(0, self.get_head_position())


def main():
    """Главный цикл."""
    # Инициализация PyGame:
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        apple.draw()
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        snake.move()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position()
        elif snake.get_head_position() == apple.position:
            snake.get_new_head()
            apple.randomize_position()
        elif len(snake.positions) >= GRID_WIDTH * GRID_HEIGHT:
            print('Game Over, you are won')
            raise SystemExit
        pygame.display.update()


if __name__ == '__main__':
    main()
