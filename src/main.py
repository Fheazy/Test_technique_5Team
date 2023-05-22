# in each round of this game, the hunter and the rabbits will move exactly 1 kilometer in the forest which represents
# 1 cell. if the rabbit encounters he can hide in it in case the burrow is empty.
# if the hunter is out of bullets he then looses and if he is no longer hungry (hunger = 0) he then wins
# if the hunter encounters a rabbit (both are in the same cell in a round) the hunter will then use a bullet
# to shoot the rabbit, and depending on the precision of the hunter and the rabbit, the rabbit could escape the shoot
# the hunter will be represented by a red colored cell and the burrows by a blue colored cell if they are not occupied
# and in yellow if they are occupied
# the trees are there to help the rabbits hide for a single round, and that occurs if the hunter encounters a rabbit
# and if the rabbit was close enough to the tree (100 meters away from any tree in the forest), the positions of the
# rabbits and the trees are more detailed for that purpose

import random
import math
import tkinter as tk

# Constants for GUI
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
CELL_SIZE = 50

def is_inside_forest(position):
    x, y = position
    return 0 <= x < forest.total_area and 0 <= y < forest.total_area

class Hunter:
    def __init__(self):
        self.bullets = random.randint(1, 10) # once the hunter expires the number of bullets he has
        # the rabbits will then be able to escape him
        self.hunger = random.randint(1, 10) # the hunter will continue hunting until
        # he is not hungry anymore e.g : hunger == 0
        self.precision = random.random()# this attribute is added to the hunter to match the rabbit's speed
        # in case they confront each other
        self.distance = 0
        self.max_distance_hunter = 20
        self.position = [0, 0] # the hunter start in the "center" of the forest,
        # therefore the distance he traveled is 0 at the start
        self.number_rabbits_hunted = 0

    def hunt(self):
        for r in Forest.rabbits:
            if int(r.position[0]) == self.position[0] and int(r.position[1]) == self.position[1]: # the hunter can
                # shoot the rabbit if they are in the sae cell
                for t in Forest.trees:
                    # in case the rabbit and the hunter are in the same cell and the rabbit is at 100 meters close
                    # to a tree when that happens, the rabbit can hen hide behind the tree for the round
                    if math.sqrt((t.position[0] - self.position[0])**2 + (t.position[1] - self.position[1])**2) < 0.1:
                        print("The rabbit found a tree where to hide for this round and the hunter didn't see him")
                        pass
                if self.bullets > 0:
                    self.bullets -= 1
                    print("Hunter shoots a bullet!")
                    if self.precision > ((r.speed / 10) + 1): # by adding +1 we make sure the rabbit will always
                        # be able to escape the hunter
                        print("The hunter caught the rabbit!")
                        Forest.rabbits.remove(r)
                        self.hunger -= 1
                        self.number_rabbits_hunted += 1
                    else:
                        print("The rabbit escapes!") # if the rabbit is fast enough he will be able
                        # to dodge the hunter's bullet
                else:
                    print("Hunter is out of bullets!")
                break

    def move(self):
        if self.distance < self.max_distance_hunter:
            self.distance += 1
            while True:
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                new_position = [self.position[0] + dx, self.position[1] + dy]
                if is_inside_forest(new_position) and 0 < (abs(dx) + abs(dy)) < 2:
                    self.position = new_position
                    break
            print(f"Hunter moves to position: {self.position}")
        else:
            print("Hunter cannot move anymore.")


class Rabbit:
    def __init__(self):
        self.position = [random.randint(0, 9) + random.random(), random.randint(0, 9) + random.random()]
        # we add a more precise position for rabbit to check if there's any tree at 50m close to him where he
        # could hide in case he encounters the hunter
        self.speed = random.randint(0, 10)
        self.color = random.choice(["white", "brown"])
        self.distance = 0
        self.max_distance_rabbit = 20 # by limiting the maximum distance traveled by both the rabbits and the hunter
        # we make sure the game has at maximum 20 moves before it ends


    def move(self):
        if self.distance < self.max_distance_rabbit:
            self.distance += 1
            while True:
                dx = random.randint(-1, 1)
                dy = random.randint(-1, 1)
                new_position = [self.position[0] + dx, self.position[1] + dy]
                if is_inside_forest(new_position) and 0 < (abs(dx) + abs(dy)) < 2:
                    self.position = new_position
                    break
            print(f"Rabbit moves to position: {[int(self.position[0]), int(self.position[1])]}")
        else:
            print("Rabbit cannot move anymore.")

    def is_near(self, position):
        return int(self.position[0] - position[0]) == 0 and int(self.position[1] - position[1]) == 0

    def seek_burrow(self): # we consider that a rabbit can hide in the burrow if they both are in the same "cell"
        for b in Forest.burrows:
            if b.occupied is False and self.is_near(b.position):
                b.occupied = True
                return True


class Burrow:
    def __init__(self, position):
        self.position = position
        self.occupied = False


class Tree:
    def __init__(self, position):
        self.position = position


class Forest:
    rabbits = []
    burrows = []
    trees = []

    def __init__(self, total_area, num_trees):
        self.total_area = total_area
        self.num_trees = num_trees

    def generate_rabbits(self, num_rabbits):
        for _ in range(num_rabbits):
            self.rabbits.append(Rabbit())

    def generate_trees(self, num_trees):
        for _ in range(num_trees):
            x = random.randint(0, 9) + random.random()
            y = random.randint(0, 9) + random.random()
            position = [x, y]
            self.trees.append(Tree(position))

    def generate_burrows(self, num_burrows):
        for _ in range(num_burrows):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            position = [x, y]
            self.burrows.append(Burrow(position))

def draw_cell(c, row, col, color):
    x1 = col * CELL_SIZE
    y1 = row * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    c.create_rectangle(x1, y1, x2, y2, fill=color)

def draw_game(h, f):
    canvas.delete("all")  # Clear the canvas before drawing for each step

    for i in range(f.total_area):
        for j in range(f.total_area):
            draw_cell(canvas, i, j, "green")

    for b in f.burrows:
        if b.occupied:
            draw_cell(canvas, b.position[0], b.position[1], "yellow")
        else:
            draw_cell(canvas, b.position[0], b.position[1], "blue")

    draw_cell(canvas, h.position[0], h.position[1], "red")

    for r in forest.rabbits:
        draw_cell(canvas, int(r.position[0]), int(r.position[1]), r.color)

hunter = Hunter()
forest = Forest(10, 5)
forest.generate_rabbits(10)
forest.generate_trees(1000)
forest.generate_burrows(10)

def next_move():
    print("----------- new round ---------------")
    hunter.hunt()
    for r in forest.rabbits:
        r.move()
        if r.seek_burrow():
            print("A rabbit has found a burrow where to hide ! He is now safe")
            Forest.rabbits.remove(r)
    # if burrow found, then the rabbit hides in it and wouldn't move
    # anymore and would be considered out of the forest from now on
    hunter.move()
    draw_game(hunter, forest)

    if len(forest.rabbits) == 0:
        print("All rabbits are gone. the game ha ended.")
        return

    if hunter.distance >= hunter.max_distance_hunter:
        print("Hunter reached the maximum distance. the game has ended.")
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
    draw_cell(canvas, burrow.position[0], burrow.position[1], "blue")

draw_cell(canvas, hunter.position[0], hunter.position[1], "red")

for rabbit in forest.rabbits:
    draw_cell(canvas, int(rabbit.position[0]), int(rabbit.position[1]), rabbit.color)

button = tk.Button(root, text="Next Move", command=next_move)
button.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
if hunter.number_rabbits_hunted != 0:
    print(f"the Hunter has has been to capture {hunter.number_rabbits_hunted} rabbits")
else:
    print("All the rabbits escaped the hunter")
