
import random

# Constants for the game window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Game parameters
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 10
BALL_SIZE = 10
BRICK_ROWS = 3
BRICK_COLS = 7
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_PADDING = 5


class Brick:
    COLORS = {3: "#8FE1A2", 2: "#ED639E", 1: "#4535AA"}

    def __init__(self, canvas, x, y, hits):

        self.canvas = canvas
        self.hits = hits
        x1 = x - BRICK_WIDTH // 2
        y1 = y - BRICK_HEIGHT // 2
        x2 = x1 + BRICK_WIDTH
        y2 = y1 + BRICK_HEIGHT
        self.item = canvas.create_rectangle(x1, y1, x2, y2, fill=Brick.COLORS[hits], width=1)

    def hit(self):
        self.hits -= 1
        if self.hits <= 0:
            self.canvas.delete(self.item)
            return True  # Brick removed
        else:
            self.canvas.itemconfig(self.item, fill=Brick.COLORS[self.hits])
            return False


class Paddle:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        x1 = x - self.width // 2
        y1 = y - self.height // 2
        x2 = x1 + self.width
        y2 = y1 + self.height
        self.item = canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
        self.speed = 15

    def move(self, dx):
        pos = self.canvas.coords(self.item)
        if pos[0] + dx >= 0 and pos[2] + dx <= WINDOW_WIDTH:
            self.canvas.move(self.item, dx, 0)

    def get_position(self):
        return self.canvas.coords(self.item)


class Ball:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.size = BALL_SIZE
        x1 = x - self.size // 2
        y1 = y - self.size // 2
        x2 = x1 - self.size
        y2 = y1 - self.size
        self.item = canvas.create_oval(x1, y1, x2, y2, fill="red")
        #  initial ball direction
        self.dx = random.choice([-3, 3])
        self.dy = -3

    def move(self):
        self.canvas.move(self.item, self.dx, self.dy)
        pos = self.canvas.coords(self.item)
        # Bounce off left/right walls
        if pos[0] <= 0 or pos[2] >= WINDOW_WIDTH:
            self.dx = -self.dx
        # Bounce off top wall
        if pos[1] <= 0:
            self.dy = -self.dy
        return pos

    def reverse_y(self):
        self.dy = -self.dy

    def get_position(self):
        return self.canvas.coords(self.item)

    def reset(self, x, y):
        self.canvas.coords(self.item, x - self.size // 2, y - self.size // 2, x + self.size // 2, y + self.size // 2)
        self.dx = random.choice([-3, 3])
        self.dy = -3


class Score:
    def __init__(self, canvas):
        self.canvas = canvas
        self.value = 0
        self.text_item = canvas.create_text(50, 20, text=f"Score: {self.value}", fill="white", font=("Aerial", 16))

    def add(self, points):
        self.value += points
        self.canvas.itemconfig(self.text_item, text=f"Score: {self.value}")


