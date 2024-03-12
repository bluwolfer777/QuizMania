class Player:

    def __init__(self, name, surname, addpointer):
        self.name = name
        self.surname = surname
        self.points = addpointer
        self.addpointer = addpointer

    def add_points(self, points):
        self.points += points
        return self.points

    def __str__(self):
        username = f"{self.name}.{self.surname}"
        if (self.points == 0):
            return f"{username}"
        else:    
            return f"{username} - {self.points}"

try1 = Player("Bobo", "Debobbis", 0)
try1.add_points(0)
print(try1)

class Playyer:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        #if username not in self.users:
        self.users[username] = 0
        print(f"{username} è entrato nella stanza")

    def remove_user(self, username):
        #if username in self.users:
        del self.users[username]
        print(f"{username} ha lasciato la stanza")

    def add_points(self, username, points):
        #if username in self.users:
        self.users[username] += points

    def get_user_points(self, username):
        return self.users.get(username, 0)

    def __str__(self):
        return f"Utenti: {', '.join(self.users.keys())}"

room = Playyer()
user1 = "Bobo"
room.add_user(user1)

print(room)

room.add_points(user1, 10)

print(f"{user1}: {room.get_user_points(user1)}")
