from users import users


class SocialNetwork:
    _net = False

    def __init__(self, name):
        if SocialNetwork._net:
            raise RuntimeError("Another instance of SocialNetwork already exists")  # singelton design pattern
        self.users = []
        self.posts = []
        self.name = name
        SocialNetwork._net = True
        print(f"The social network {self.name} was created!")

    def __str__(self): # to string
        print(f"{self.name} social network:")
        return f"{self.display() or ''}"  # print the social network

    def print(self):  # print the profil of the users
        for user in self.users:
            print(f"User name: {user}, Number of posts: {user.posts.size}, Number of followers: {user.followers.size}")

    def add_post(self, post):
        self.posts.append(post)  # add new post

    def sign_up(self, username, password):
        if any(user.username == username for user in self.users):  # check if the username is already taken
            print(f"Username '{username}' is already taken. Please choose a different username.")
            return None

        new_user = users(username, password)  # Create a new user
        if new_user.is_legal(new_user.password):  # check if the password is valid
            self.users.append(new_user)  # add the new user to the list of users
            return new_user
        else:
            print(
                "The password must be at least 4 characters long and not more than 8 characters long. Please try again.")
            return None

    def display(self):
        for user in self.users:  # print all the users in the social network
            print(user)

    def log_out(self, username):
        user = None  # initialize user
        for u in self.users:  # check if the user is in the social network
            if u.username == username:
                user = u
                break
        if user:
            if user.connected:  # check if the user is connected
                user.disconnect()  # disconnect the user
                print(f"{username} disconnected")
            else:
                print(f"{username} is already logged out.")
        else:
            print(f"{username} not found in the social network.")

    def log_in(self, username, password):
        user = None  # initialize user
        for u in self.users:  # check if the user is in the social network
            if u.username == username:
                user = u  # set the user to the user in the social network
                break
        if user:
            user.connect()  # connect the user
            print(f"{username} connected")
        else:
            print(f"{username} not found in the social network.")

