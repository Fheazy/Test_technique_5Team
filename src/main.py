import random

class Hunter:
    def __init__(self):
        self.bullets = random.randint(0, 10)
        self.hunger = random.randint(0, 10)
        self.distance = 0
        self.position = [0, 0] # the hunter start for the "center" of the forest, therefore the distance he traveled is 0 at the start

    def hunt(self):
        for lapin in Forest.rabbits:
            if lapin.position == self.position:
                if self.bullets > 0:
                    self.bullets -= 1
                    Forest.rabbits.remove(lapin)
                    print("Hunter shot a rabbit!")
                else:
                    print("Hunter is out of bullets!")
                break

    def move(self):
        if self.distance < 10:
            self.distance += 1
            self.position[0] += random.randint(-1, 1)
            self.position[1] += random.randint(-1, 1)
            print("Hunter moved to", self.position)
        else:
            print("Hunter cannot move anymore.")

class Rabbit:
    def __init__(self):
        self.speed = random.randint(0, 10)
        self.color = random.choice(["white", "brown"])
        self.distance = 0
        self.position = [random.randint(-10, 10), random.randint(-10, 10)]

    def move(self):
        if self.distance < 10:
            self.distance += 1
            self.position[0] += random.randint(-1, 1)
            self.position[1] += random.randint(-1, 1)
            print("Rabbit moved to", self.position)
        else:
            print("Rabbit cannot move anymore.")

    def seek_burrow(self):
        for burrow in Forest.burrows:
            if burrow.occupied == False and self.is_near(burrow.position):
                burrow.occupied = True
                print("Rabbit found refuge in a burrow!")
                return

    def is_near(self, position):
        return abs(self.position[0] - position[0]) <= 1 and abs(self.position[1] - position[1]) <= 1

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
            self.burrows.append(Burrow([random.randint(-10, 10), random.randint(-10, 10)]))

# Instantiate a hunter, forest, and several rabbits and burrow
hunter = Hunter()
forest = Forest(10, 5)
forest.generate_lapins(3)
forest.generate_burrows(2)

# Game loop
while True:
    hunter.hunt()
    for rabbit in forest.rabbits:
        rabbit.move()
        rabbit.seek_burrow()
    hunter.move()

    if len(forest.burrows) == 0:
        print("All rabbits are gone. Hunter lost.")
        break

    if hunter.distance >= 10:
        print("Hunter reached the maximum distance. Hunter lost.")
        break