class Playyer:
    def __init__(self):
        self.users = {}

    def add_user(self, name, surname):
        username = f"{name}.{surname}"
        self.users[username] = 0
        print(f"{username} è entrato nella stanza")

    def remove_user(self, username):
        del self.users[username]
        print(f"{username} ha lasciato la stanza")

    def add_points(self, username, points):
        self.users[username] += points

    def get_user_points(self, username):
        return self.users.get(username, 0)

    def __str__(self):
        sorted_users = sorted(self.users.items(), key=lambda x: x[1], reverse=True)
        user_points_str = "\n".join([f"{user}: {points}" for user, points in sorted_users])
        return f"Classifica:\n{user_points_str}"