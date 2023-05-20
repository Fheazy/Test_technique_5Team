import random
import tkinter as tk

# Constants for GUI
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500
CELL_SIZE = 50


class Hunter:
    def __init__(self):
        self.bullet_count = random.randint(0, 10)
        self.hunger_level = random.randint(0, 10)
        self.distance_traveled = 0
        self.position = [0, 0]

    def hunt(self):
        if self.bullet_count > 0:
            self.bullet_count -= 1
            print("Hunter shoots a bullet!")
        else:
            print("Hunter is out of bullets!")

        self.hunger_level += 1
        self.distance_traveled += 1

    def move(self, x, y):
        self.distance_traveled += 1
        self.position[0] += x
        self.position[1] += y
        print(f"Hunter moves to position: {self.position}")


class Rabbit:
    def __init__(self):
        self.speed = random.randint(0, 10)
        self.color = random.choice(["white", "brown"])
        self.distance_traveled = 0
        self.position = [random.randint(-10, 10), random.randint(-10, 10)]

    def flee(self):
        self.distance_traveled += 1
        print("Rabbit flees!")


class Burrow:
    def __init__(self):
        self.position = [random.randint(-10, 10), random.randint(-10, 10)]
        self.occupied = False


class Forest:
    def __init__(self, square_kilometers, max_trees):
        self.burrows = []
        self.rabbits = []
        self.square_kilometers = square_kilometers
        self.max_trees = max_trees

    def add_burrow(self, burrow):
        self.burrows.append(burrow)

    def add_rabbit(self, rabbit):
        self.rabbits.append(rabbit)


def draw_cell(canvas, row, col, color):
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill=color)


def draw_game(hunter, forest, rabbits):
    root = tk.Tk()
    root.title("Hunter vs. Rabbits")
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    canvas.pack()

    for i in range(forest.square_kilometers):
        for j in range(forest.square_kilometers):
            draw_cell(canvas, i, j, "green")

    for burrow in forest.burrows:
        draw_cell(canvas, burrow.position[0], burrow.position[1], "brown")

    draw_cell(canvas, hunter.position[0], hunter.position[1], "red")

    for rabbit in rabbits:
        draw_cell(canvas, rabbit.position[0], rabbit.position[1], rabbit.color)

    root.mainloop()


# Instantiate the hunter, forest, and rabbits
hunter = Hunter()
forest = Forest(10, 100)
burrow = Burrow()
forest.add_burrow(burrow)

rabbits = []
for _ in range(5):
    rabbit = Rabbit()
    forest.add_rabbit(rabbit)
    rabbits.append(rabbit)

# Start the chase
for rabbit in rabbits:
    while True:
        if hunter.position == rabbit.position:
            hunter.hunt()
        elif rabbit.position == burrow.position and not burrow.occupied:
            burrow.occupied = True
            print("Rabbit finds a burrow and escapes!")
            break
        elif rabbit.speed < random.randint(0, 10):
            rabbit.flee()
            rabbit.position = [random.randint(-10, 10), random.randint(-10, 10)]

        if hunter.distance_traveled >= 10 or rabbit.distance_traveled >= 10:
            print("Max distance reached. Game over!")
            break

# Draw the game on the GUI
draw_game(hunter, forest, rabbits)
