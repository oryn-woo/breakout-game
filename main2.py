import tkinter as tk
from tkinter import ttk
from main import Score, Brick, Ball, Paddle


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


class BreakoutGame:
    def __init__(self, root):
        self.root = root
        root.title("Breakout Game")
        # use ttk style for extra space
        style = ttk.Style()
        style.theme_use("clam")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
        self.canvas.pack()

        self.score = Score(self.canvas)

        # Create paddle at bottom center
        self.paddle = Paddle(self.canvas, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        # Create ball above the paddle
        self.ball = Ball(self.canvas, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50)

        # create bricks
        self.bricks = []
        offset_x = (WINDOW_WIDTH - (BRICK_COLS * (BRICK_WIDTH + BRICK_PADDING)) + BRICK_PADDING) // 2
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = offset_x + col + (BRICK_WIDTH + BRICK_PADDING) + BRICK_WIDTH // 2
                y = 50 + row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_HEIGHT // 2
                # More hits for top row fewer hits for buttom row
                hits = 3 - row
                brick = Brick(self.canvas, x, y, hits)
                self.bricks.append(brick)

        # Bind keys for paddle Movement
        root.bind("<Left>", lambda e: self.paddle.move(-self.paddle.speed))
        root.bind("<Right>", lambda e: self.paddle.move(self.paddle.speed))

        # Start game loop
        self.game_over = False
        self.update()

    def update(self):
        if self.game_over:
            return
        ball_pos = self.ball.move()

        # Check collision with paddle
        paddle_pos = self.paddle.get_position()
        if \
        ball_pos[3] >= paddle_pos[1] and ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2] and ball_pos[3] <= paddle_pos[3] + 10:
            self.ball.reverse_y()

        # Check collision with bricks
        hit_index = None
        for index, brick in enumerate(self.bricks):
            brick_pos = self.canvas.coords(brick.item)
            if self.overlap(ball_pos, brick_pos):
                hit_index = index
                break
        if hit_index is not None:
            brick = self.bricks.pop(hit_index)
            removed = brick.hit()

            # Increase score if brick is not fully removed
            self.score.add(10)
            self.ball.reverse_y()

        # check if ball geos off the bottom
        if ball_pos[3] >= WINDOW_HEIGHT:
            self.game_over = True
            self.canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="Game Over", fill="White", font=("Aerial", 24))
            return

        self.root.after(20, self.update)

    def overlap(self, pos1, pos2):
        # pos = [x1, y1, x2, y2]
        return pos1[2] < pos2[0] or pos1[0] > pos2[2] or pos1[3] < pos2[1] or pos1[1], pos2[3]


if __name__ == "__main__":
    root = tk.Tk()
    game = BreakoutGame(root)
    root.mainloop()