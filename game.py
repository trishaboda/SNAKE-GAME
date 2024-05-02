import turtle
import random
import time

UNIT_LENGTH = 20


class Snake:

    def __init__(self, head_colour, body_colour):

        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(head_colour)
        self.body: list[turtle.Turtle] = []
        self.body_colour = body_colour
        self.head.penup()
        self.head.goto(0, 0)
        self.direction = "stop"
        self.score = 0

    def go_up(self):
        if self.direction != "down":
            self.direction = "up"

    def go_down(self):
        if self.direction != "up":
            self.direction = "down"

    def go_right(self):
        if self.direction != "left":
            self.direction = "right"

    def go_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move(self):

        # Moving rest of the body parts
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].goto(self.body[i - 1].xcor(),
                              self.body[i - 1].ycor())
        # Moving first body part
        if len(self.body) > 0:
            self.body[0].goto(self.head.xcor(), self.head.ycor())

        if self.direction == "up":
            self.head.sety(self.head.ycor() + UNIT_LENGTH)
        if self.direction == "down":
            self.head.sety(self.head.ycor() - UNIT_LENGTH)
        if self.direction == "right":
            self.head.setx(self.head.xcor() + UNIT_LENGTH)
        if self.direction == "left":
            self.head.setx(self.head.xcor() - UNIT_LENGTH)


class Game:

    def __init__(self, snake: Snake):

        self.screen = turtle.Screen()
        self.size = 400
        self.tick = 0.1
        self.window = True
        self.running = True

        # Snake
        self.snake = snake
        self.screen.listen()
        self.screen.onkeypress(snake.go_up, "Up")
        self.screen.onkeypress(snake.go_down, "Down")
        self.screen.onkeypress(snake.go_right, "Right")
        self.screen.onkeypress(snake.go_left, "Left")

        # Fruit
        self.fruit = turtle.Turtle()
        self.fruit.speed(0)
        self.fruit.shape("circle")
        self.fruit.color("lime")
        self.fruit.penup()

        # Scoring
        self.scoring = turtle.Turtle()
        self.scoring.speed(0)
        self.scoring.color("white")
        self.score_font = ("Courier", 24, "bold")
        self.scoring.penup()
        self.scoring.hideturtle()

        self.game_over_text = turtle.Turtle()
        self.game_over_text.hideturtle()
        self.game_over_font = ("Courier", 20, "bold")
        self.quit_text = turtle.Turtle()
        self.quit_text.penup()
        self.quit_text.hideturtle()

    def create_window(self, title, colour):

        self.screen.title(title)
        self.screen.setup(width=self.size + UNIT_LENGTH * 10,
                          height=self.size + UNIT_LENGTH * 10)
        self.screen.tracer(0)
        self.screen.bgcolor(colour)

    def place_fruit(self):

        self.fruit.goto(
            random.randrange(-self.size // 2, self.size // 2, UNIT_LENGTH),
            random.randrange(-self.size // 2, self.size // 2, UNIT_LENGTH))

    def create_play_area(self, border_colour):

        # Creating Border
        turtle.speed(0)
        turtle.pensize(UNIT_LENGTH // 4)
        turtle.penup()
        turtle.goto((-self.size // 2) - (UNIT_LENGTH // 2),
                    (-self.size // 2) - (UNIT_LENGTH // 2))
        turtle.pendown()
        turtle.color(border_colour)
        turtle.left(90)
        turtle.forward(self.size)
        turtle.right(90)
        turtle.forward(self.size)
        turtle.right(90)
        turtle.forward(self.size)
        turtle.right(90)
        turtle.forward(self.size)
        turtle.penup()
        turtle.hideturtle()

        # Placement of fruit & score
        self.place_fruit()
        self.scoring.sety(self.size // 2)
        self.scoring.write("Score: ", align="center", font=self.score_font)

    def close_window(self):
        self.window = False
        turtle.Terminator()

    def game_over(self, colour):

        self.screen.clear()
        self.screen.bgcolor(colour)
        self.game_over_text.write(
            f"Game Over! Your score is {self.snake.score}",
            align="center", font=self.game_over_font)
        self.quit_text.sety(-self.size // 2)
        self.quit_text.write("Press Escape to quit", align="center",
                             font=self.score_font)
        self.screen.onkeypress(self.close_window, "Escape")

    def main_logic(self):

        # Snake & Fruit Collision
        if self.snake.head.xcor() == self.fruit.xcor() \
                and self.snake.head.ycor() == self.fruit.ycor():
            self.place_fruit()
            self.scoring.clear()
            self.snake.score += 1
            self.scoring.write(f"Score: {self.snake.score}",
                               align="center",
                               font=self.score_font)
            old_fruit = turtle.Turtle()
            old_fruit.speed(0)
            old_fruit.shape("square")
            old_fruit.color(self.snake.body_colour)
            old_fruit.penup()
            self.snake.body.append(old_fruit)

        # Moving Snake
        self.snake.move()

        # Snake & Border Collision
        if self.snake.head.xcor() < (-self.size // 2) \
                or self.snake.head.xcor() >= (self.size // 2) \
                or self.snake.head.ycor() < (-self.size // 2) \
                or self.snake.head.ycor() >= (self.size // 2):
            self.running = False
            self.game_over("yellow")

        # Snake Head & Body Collision
        for part in self.snake.body:
            if part.xcor() == self.snake.head.xcor() \
                    and part.ycor() == self.snake.head.ycor():
                self.running = False
                self.game_over("yellow")


def main():
    snake = Snake("blue", "red")
    game = Game(snake)
    game.create_window("Python in Python", "black")
    game.create_play_area("white")
    while game.window:
        if game.running:
            game.main_logic()
        game.screen.update()
        time.sleep(game.tick)
    game.screen.bye()


if __name__ == "__main__":
    main()