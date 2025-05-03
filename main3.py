from turtle import Screen, Turtle
import colorsys
import random


SCORE = 0
# Define number of columns
NUM_COLUMNS = 15
# Spacing between turtles
TURTLE_SPACING = 40

# Number of columns
NUM_ROWS = 1
BRICKS = []
screen = Screen()
screen.setup(680, 600)

# Generate list of unique colors
num_turtles = 4 * NUM_COLUMNS
BALL_SPEED = 4


def move_left():
    x_cor = p.xcor() - 20
    if x_cor > -305:
        p.setx(x_cor)


def move_right():
    x_cor = p.xcor() + 20
    if x_cor < 305:
        p.setx(x_cor)


# ball shouldn't start in a consistent direction all the time




def update_ball():
    # Initialize in such away that the ball starts moving down
    global b
    x = b.xcor() + b.dx
    y = b.ycor() - b.dy
    b.goto(x, y)
    if y > 290 or y < -290:
        b.dy *= -1
    elif x > 322 or x < -330:
        b.dx *= -1
    elif -270 < b.ycor() < -260 and p.xcor() - 50 < b.xcor() < p.xcor() + 50:
        b.dy *= -1
    elif b.ycor() < - 285:
        game_over()
    for brick in BRICKS:
        if brick.distance(b) < 22:
            brick.hideturtle()
            BRICKS.remove(brick)
            b.dy *= -1
            update_score()
            break
    screen.ontimer(update_ball, 20)


def game_over():
    b.hideturtle()
    b.sety(-300)
    p.hideturtle()
    over_message = Turtle()
    over_message.hideturtle()
    over_message.penup()
    over_message.color(colors[11])
    over_message.write("Game Over ", align="center", font=("Aerial", 24, "normal"))
    screen.update()


def update_score():
    global SCORE
    SCORE += 10
    score_display.clear()
    score_display.write(f"Score: {SCORE}", align="center", font=("Aerial", 24, "normal"))


# detect collision
# def detect_wall()

colors = []
for i in range(num_turtles * 3):
    hue = i / num_turtles
    color = colorsys.hsv_to_rgb(hue, 1, 1)
    colors.append(color)

color_index = 0

for row in range(NUM_ROWS):
# The first loop is of range 4, representing 4 rows, which help the second loop create entries for a single row.
    for col in range(NUM_COLUMNS):
        # Now the second loop iterates, creating a row of n number of turtle objects. When it is done, the first loop
        # triggers it again to replicate another n number of rows.
        t = Turtle("square")
        t.color(colors[color_index])
        color_index += -3
        t.penup()
        t.shapesize(stretch_len=2)
        # Our screen is (400, 300) with a center at (0, 0), so the
        # Arithmetic inside the goto function ensures the turtles are properly positioned.
        # We use row for y coordinate, ensuring y is constant for a certain amount of time the second loop runs,
        # ensuring the proper n number of turtles are placed on the row.
        # We use column for the x coordinate to ensure the turtle objects are placed for a varying number of
        # x coordinates
        TURTLE_SPACING += 4
        x = -310 + (col * TURTLE_SPACING)
        TURTLE_SPACING = 40
        TURTLE_SPACING -= 10
        y = 150 - (row * TURTLE_SPACING)
        t.goto(x, y)
        TURTLE_SPACING = 40
        BRICKS.append(t)


p = Turtle("square")
p.penup()
p.shapesize(stretch_len=5)
p.goto(0, -280)
p.color(colors[5])
screen.listen()
screen.onkey(move_right, "Right")
screen.onkey(move_left, "Left")


b = Turtle("circle")
b.penup()
b.color(colors[15])
b.dy = BALL_SPEED
b.dx = random.choice([BALL_SPEED, -BALL_SPEED])
b.goto(0, 0)

score_display = Turtle()
score_display.hideturtle()
score_display.penup()
score_display.goto(0, 260)
score_display.color(colors[15])
score_display.write(f"Score: {SCORE}", align="center", font=("Aerial", 24, "normal"))

# def ball_move_bounce():
# while True:
update_ball()




screen.mainloop()