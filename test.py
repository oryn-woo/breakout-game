from turtle import Turtle, Screen


def move_left():
    x = t.xcor() - 20
    if x > -362:
        t.setx(x)


def move_right():
    x = t.xcor() + 20
    if x < 362:
        t.setx(x)


screen = Screen()
screen.setup(width=800, height=600)
t = Turtle("square")
t.shapesize(stretch_len=5)
t.penup()
t.goto(0, -260)

screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

screen.mainloop()