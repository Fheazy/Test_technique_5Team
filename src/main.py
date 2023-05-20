import random
import tkinter as tk

# Constants for GUI
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
CELL_SIZE = 50

class Hunter:
    def __init__(self):
        self.bullets = random.randint(1, 10)
        self.hunger = random.randint(1, 10) # the hunter will continue hunting until he is not hungry anymore e.g : hunger == 0
        self.distance = 0
        self.max_distance_hunter = 20
        self.position = [0, 0] # the hunter start for the "center" of the forest, therefore the distance he traveled is 0 at the start

    def hunt(self):
        for lapin in Forest.rabbits:
            if lapin.position == self.position:
                if self.bullets > 0:
                    self.bullets -= 1
                    Forest.rabbits.remove(lapin)
                    print("Hunter shot a rabbit!")
                    self.hunger -= 1
                else:
                    print("Hunter is out of bullets!")
                break

    def move(self):
        if self.distance < self.max_distance_hunter:
            self.distance += 1
            self.position[0] += random.randint(-1, 1)
            self.position[1] += random.randint(-1, 1)
            print(f"Hunter moves to position: {self.position}")
        else:
            print("Hunter cannot move anymore.")

class Rabbit:
    def __init__(self):
        self.speed = random.randint(0, 10)
        self.color = random.choice(["white", "brown"])
        self.distance = 0
        self.max_distance_rabbit = 20
        self.position = [random.randint(-10, 10), random.randint(-10, 10)]

    def move(self):
        if self.distance < self.max_distance_rabbit:
            self.distance += 1
            while True:
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                new_position = [self.position[0] + dx, self.position[1] + dy]
                if is_inside_forest(new_position):
                    self.position = new_position
                    break
            print(f"Rabbit moves to position: {self.position}")
        else:
            print("Rabbit cannot move anymore.")

    def is_near(self, position): # we consider that a rabbit can hide in the burrow if it is at the same position of it
        return (self.position[0] - position[0]) == 0 and (self.position[1] - position[1]) == 0

    def seek_burrow(self):
        for burrow in Forest.burrows:
            if burrow.occupied is False and self.is_near(burrow.position):
                burrow.occupied = True
                print("Rabbit found refuge in a burrow! It is now safe")
                forest.rabbits -= 1

class Burrow:
    def __init__(self, position):
        self.position = position
        self.occupied = False

class Forest:
    rabbits = []
    burrows = []

    def __init__(self, total_area, num_trees):
        self.total_area = total_area
        self.num_trees = num_trees

    def generate_lapins(self, num_lapins):
        for _ in range(num_lapins):
            self.rabbits.append(Rabbit())

    def generate_burrows(self, num_burrows):
        for _ in range(num_burrows):
            position = generate_random_position()
            self.burrows.append(Burrow(position))
def generate_random_position():
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    return [x, y]

def is_inside_forest(position):
    x, y = position
    return 0 <= x < forest.total_area and 0 <= y < forest.total_area

def draw_cell(canvas, row, col, color):
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill=color)


def draw_game(hunter, forest):
    canvas.delete("all")  # Clear the canvas before drawing for each step

    for i in range(forest.total_area):
        for j in range(forest.total_area):
            draw_cell(canvas, i, j, "green")

    for burrow in forest.burrows:
        draw_cell(canvas, burrow.position[0], burrow.position[1], "brown")

    draw_cell(canvas, hunter.position[0], hunter.position[1], "red")

    for rabbit in forest.rabbits:
        draw_cell(canvas, rabbit.position[0], rabbit.position[1], rabbit.color)

hunter = Hunter()
forest = Forest(10, 5)
forest.generate_lapins(3)
forest.generate_burrows(2)

def next_move():
    hunter.hunt()
    for rabbit in forest.rabbits:
        rabbit.move()
        rabbit.seek_burrow()
    hunter.move()
    draw_game(hunter, forest)

    if len(forest.burrows) == 0:
        print("All rabbits are gone. Hunter lost.")
        return

    if hunter.distance >= hunter.max_distance_hunter:
        print("Hunter reached the maximum distance. Hunter lost.")
        return

    if hunter.hunger == 0:
        print("Hunter is not hungry anymore. Hunter won.")
        return

root = tk.Tk()
root.title("Hunter vs. Rabbits")
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack()

for i in range(forest.total_area):
    for j in range(forest.total_area):
        draw_cell(canvas, i, j, "green")

for burrow in forest.burrows:
    draw_cell(canvas, burrow.position[0], burrow.position[1], "brown")

draw_cell(canvas, hunter.position[0], hunter.position[1], "red")

for rabbit in forest.rabbits:
    draw_cell(canvas, rabbit.position[0], rabbit.position[1], rabbit.color)

button = tk.Button(root, text="Next Move", command=next_move)
button.pack(side=tk.BOTTOM)

root.mainloop()
print("the Hunt has ended the rabbits are safe now")

# Draw the game on the GUI
#draw_game(hunter, forest, forest.rabbits)
