from posts import TextPost, ImagePost, SalePost

class Notification:
    def __init__(self, message, notify_type):
        self.message = message
        self.notify_type = notify_type


class users:
    def __init__(self, username, password):
        if not self.is_legal(password):
            raise ValueError("The password should have a length of at least 4 characters and not exceed 8 characters.")
        self.username = username
        self.password = password
        self.connected = True
        self.followers = []
        self.following = []
        self.num_Followers = 0
        self.notifications = []
        self.posts = []

    def __str__(self):  # to string
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers) or ' '}"

    def is_legal(self, password):  # check if the password is valid
        if len(password) > 8 or len(password) < 4:
            return False
        return True

    def connect(self):   # connect the user
        self.connected = True

    def disconnect(self):  # Disconnect the user
        self.connected = False

    def print_setting(self):  # print
        s = f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers) or ' '}"
        print(s)

    def notify(self, message):  # observer pattern to notify the user
        self.notifications.append(message)

    def unfollow(self, user):
        if user in self.following:
            self.following.remove(user)
            user.followers.remove(self)
            user.num_Followers -= 1
            print(f"{self.username} unfollowed {user.username}")
            return  # Exit the method after successful unfollow
        else:
            raise Exception("already unfollowed")

    def follow(self, user):
        if user not in self.following:
            self.following.append(user)
            user.num_Followers += 1                     # increase the number of followers of the user
            user.followers.append(self)
            # Print a message indicating that the user has started following another user
            print(f"{self.username} started following {user.username}")

    def publish_post(self, post_type, *args):  # The published post
        post1 = None

        if not self.connected:
            raise Exception("User is not connected. Cannot publish post.")

        if post_type == "Sale":
            post1 = SalePost(self, *args)  # create a new sale post

        elif post_type == "Image":
            print(f"{self.username} posted a picture")
            print()

            if len(args) == 1:  # check if the number of arguments is valid
                post1 = ImagePost(self, *args)

            else:
                print("Invalid number of arguments for ImagePost")

        elif post_type == "Text":
            post1 = TextPost(self, *args)

        if post1:
            post1._owner = self  # set the owner of the post to the user
            self.posts.append(post1)

            for follower in self.followers:  # notify the followers of the user
                follower.notify(f"{self.username} has a new post")

            if post_type != "Image":
                post1.display()
                if isinstance(post1, TextPost):
                    print()

            return post1

        else:
            print(f"Invalid post type: {post_type}")
            return None

    def print_notifications(self):
        if not self.connected:
            return None

        if self.connected:     # Print user's notifications if connected
            print(f"{self.username}'s notifications:")

            for notification in self.notifications:
                if notification is not None:
                    print(notification)