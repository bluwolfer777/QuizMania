class Player:
    def __init__(self, name, surname, point):
        self.name = name
        self.surname = surname
        self.point = point

    def __str__(self):
        username = self.name + "." + self.surname
        return f"{username} - {self.point}"
    
try1 = Player("Giorgio", "Giovanna", 69)
print(try1)