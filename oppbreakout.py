import json
import os.path
from turtle import Screen, Turtle
import colorsys
import tkinter
from tkinter import messagebox
NUM_COLUMNS = 15
NUM_ROWS = 5
TURTLE_SPACING = 40
BALL_SPEED = 3
root = tkinter.Tk()
root.withdraw()


class Paddle(Turtle):
    def __init__(self, color):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_len=5)
        self.penup()
        self.goto(0, -280)
        self.move_distance = 20
        self.is_moving_left = False
        self.is_moving_right = False

    def move_left(self):
        self.is_moving_left = True

    def move_right(self):
        self.is_moving_right = True

    def stop_left(self):
        self.is_moving_left = False

    def stop_right(self):
        self.is_moving_right = False

    def update_paddle(self):
        if self.is_moving_left:
            x = self.xcor() - self.move_distance
            if x > -370:
                self.setx(x)
        if self.is_moving_right:
            x = self.xcor() + self.move_distance
            if x < 370:
                self.setx(x)
        self.screen.ontimer(self.update_paddle, 50)


    # def move_left(self):
    #     x_cor = self.xcor() - 20
    #     if x_cor > -305:
    #         self.setx(x_cor)
    #
    # def move_right(self):
    #     x_cor = self.xcor() + 20
    #     if x_cor < 305:
    #         self.setx(x_cor)


class Ball(Turtle):
    def __init__(self, color, speed):
        super().__init__()
        self.shape("circle")
        self.color(color)
        self.penup()
        self.goto(0, 0)
        self.dx = speed
        self.dy = speed

    def update_position(self, paddle, bricks, update_score):
        x = self.xcor() + self.dx
        y = self.ycor() - self.dy
        self.goto(x, y)
        # Check for collision with wall
        if y > 290 or y < -290:
            self.dy *= -1
        elif x > 322 or x < -330:
            self.dx *= -1
        elif -270 < self.ycor() < -260 and paddle.xcor() - 60 < self.xcor() < paddle.xcor() + 60:
            self.dy *= -1
        elif self.ycor() < -280:
            # clear bricks befor displaying game over message
            for brick in bricks:
                brick.hideturtle()
            return False  # False


        # Check collision with bricks
        # for brick in bricks:
        #     brick_left_edge_cor = brick.xcor() - 20  # Left boundary of brick
        #     brick_right_edge_cor = brick.xcor() + 20  # Right boundary of brick
        #     brick_top_edge_cor = brick.ycor() - 10  # Top boundary of brick
        #     brick_bottom_edge_cor = brick.xcor() - 10  # Bottom boundary of brick
        #
        #     ball_left_edge_cor = self.xcor() - 10  # Left boundary of brick
        #     ball_right_edge_cor = self.xcor() + 10  # Right boundary of brick
        #     ball_top_edge_cor = self.ycor() + 10  # Bottom boundary of brick
        #     ball_bottom_edge_cor = self.ycor() - 10  # Bottom boundary of brick
        #
        #     Check if ball and brick rectangles overlap
            # if (ball_right_edge_cor > brick_left_edge_cor and ball_left_edge_cor < brick_right_edge_cor) and (ball_top_edge_cor > brick_bottom_edge_cor and ball_bottom_edge_cor < brick_top_edge_cor):
            #     brick.hideturtle()
            #     bricks.remove(brick)
            #     update_score()

                # hit_from_top_bottom = (ball_bottom_edge_cor <= brick_top_edge_cor and self.dy > 0) or (ball_top_edge_cor >= brick_bottom_edge_cor and self.dy < 0)
                # hit_from_sides = (ball_right_edge_cor >= brick_left_edge_cor and self.dx > 0) or (ball_left_edge_cor <= brick_right_edge_cor and self.dx < 0)
                # if hit_from_top_bottom:
                #     self.dy *= -1
                # elif hit_from_sides:
                #     self.dx *= -1
                # diff_x = abs(self.xcor() - brick.xcor())
                # diff_y = abs(self.ycor() - brick.ycor())
                #
                # if diff_x > diff_y:
                #     brick.hideturtle()
                #     bricks.remove(brick)
                #     update_score()
                #
                #     self.dx *= -1
                # else:
                #     brick.hideturtle()
                #     bricks.remove(brick)
                #     update_score()
                #
                #     self.dy *= -1
        for brick in bricks:
            if brick.distance(self) < 30:
                brick.hideturtle()
                bricks.remove(brick)
                self.dy *= -1
                update_score()
                break
        if not bricks:
            return False #Win condition
        return True


class Brick(Turtle):
    def __init__(self, color, position):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.penup()
        self.shapesize(stretch_len=2)
        self.goto(position)


class Game:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(680, 600)
        self.screen.title("Breakout Game")
        self.screen.bgcolor("black")
        self.screen.tracer(0, 0)  # Stops update after while setting up the game
        self.score = 0
        self.paddle = Paddle("indigo")
        self.ball = Ball("red", BALL_SPEED)
        self.bricks = []
        self.colors = self.generate_colors()
        self.create_bricks()
        self.screen.listen()
        self.screen.onkeypress(self.paddle.move_right, "Right")
        self.screen.onkeypress(self.paddle.move_left, "Left")
        self.screen.onkeyrelease(self.paddle.stop_left, "Left")
        self.screen.onkeyrelease(self.paddle.stop_right, "Right")
        self.paddle.update_paddle()
        self.score_display = self.create_score_display()
        self.screen.update()  # Draw everything at once
        self.screen.tracer(1)  # Re-enable normal updates
        self.screen.ontimer(self.start_game, 1000)  # Delay start for 1s
        self.over_message = None

    def generate_colors(self):
        num_turtle = NUM_ROWS * NUM_COLUMNS
        colors = []
        for i in range(num_turtle * 2):
            hue = i / num_turtle
            color = colorsys.hsv_to_rgb(hue, 1, 1)
            colors.append(color)
        return colors

    def create_bricks(self):
        center_row = NUM_ROWS / 2
        center_col = NUM_COLUMNS / 2
        radius = min(NUM_ROWS, NUM_COLUMNS) / 2
        global TURTLE_SPACING
        color_index = 0
        for row in range(NUM_ROWS):
            for col in range(NUM_COLUMNS):
                distance = ((row - center_row) ** 2 + (col - center_col) ** 2) ** 0.5
                if distance < radius:
                    TURTLE_SPACING += 4
                    x = -310 + (col * TURTLE_SPACING)
                    TURTLE_SPACING = 40
                    TURTLE_SPACING -= 10
                    y = 150 - (row * TURTLE_SPACING)
                    position = (x, y)
                    brick = Brick(self.colors[color_index], position=position)
                    color_index += -2
                    TURTLE_SPACING = 40
                    self.bricks.append(brick)

    def create_score_display(self):
        score_display = Turtle()
        score_display.hideturtle()
        score_display.penup()
        score_display.goto(0, 260)
        score_display.color("indigo")
        score_display.write(f"Score: {self.score}", align="center", font=("Aerial", 24, "normal"))
        return score_display

    def update_score(self):
        self.score += 10
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}", align="center", font=("Aerial", 24, "normal"))

    def save_score(self):
        # with open("Scores.json", "w") as file:
        #     json.dump({"score": self.score}, file)
        score_file = "scores.json"
        if os.path.exists(score_file):
            with open(score_file, "r") as file:
                scores_data = json.load(file)
        else:
            score_data = {"Score": []}
            score_data["scores"].append({"score": self.score})
        with open(score_file, "w") as file:
            json.dump(scores_data, file, indent=4)

    def game_over(self):
        self.ball.hideturtle()
        self.ball.goto(-300, 0)
        self.paddle.hideturtle()
        self.over_message = Turtle()
        self.over_message.hideturtle()
        self.over_message.penup()
        self.over_message.color("red")
        self.over_message.write("Game Over\nPress 'R' to Restart\nPress 'Q' to Quite", align="center", font=("Aerial", 24, "normal"))
        self.save_score()
        self.screen.update()
        # answer = messagebox.askyesno("Game Over", "Would you like to play again?")
        # if answer:
        #     self.reset_game()
        # else:

        #     self.screen.bye()
        self.screen.onkey(self.reset_game, "r")
        self.screen.onkey(self.screen.bye, "q")
        self.screen.listen()

    def reset_game(self):
        self.score = 0
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}", align="center", font=("Aerial", 24, "normal"))
        self.over_message.clear()

        self.paddle.showturtle()
        self.paddle.goto(0, -280)

        self.ball.showturtle()
        self.ball.goto(0, 0)
        self.ball.dx = BALL_SPEED
        self.ball.dy = BALL_SPEED

        for brick in self.bricks:
            brick.hideturtle()
        self.bricks.clear()

        self.create_bricks()
        # self.screen.update()  # Draw everything at once
        # self.screen.tracer(1)
        # self.screen.ontimer(self.start_game, 1000)
        self.start_game()

    def start_game(self):
        self.play()

    def play(self):
        game_continues = self.ball.update_position(
            paddle=self.paddle, bricks=self.bricks, update_score=self.update_score
        )
        if game_continues:
            self.screen.update()  # Ensure movement is visible
            self.screen.ontimer(self.play, 20)
        else:
            self.game_over()


if __name__ == "__main__":
    game = Game()
    game.screen.mainloop()