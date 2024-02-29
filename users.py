from posts import TextPost, ImagePost, SalePost


class users:
    def __init__(self, username, password):
        if not self.is_legal(password):
            raise ValueError("The password should have a length of at least 4 characters and not exceed 8 characters.")
        self.username = username
        self.password = password
        self.connected = True
        self.followers = []
        self.following = []
        self.posts = []
        self.notifications = []

    def __str__(self):
        return f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers) or ' '}"

    def is_legal(self, password):
        if len(password) > 8 or len(password) < 4:
            return False
        return True

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def print_setting(self):
        s = f"User name: {self.username}, Number of posts: {len(self.posts)}, Number of followers: {len(self.followers) or ' '}"
        print(s)

    def notify(self, message):
        self.notifications.append(message)

    def follow(self, user):
        if user not in self.following:
            self.following.append(user)
            user.followers.append(self)
            print(f"{self.username} started following {user.username}")

    def unfollow(self, user):
        if user in self.following:
            self.following.remove(user)
            user.followers.remove(self)
            print(f"{self.username} unfollowed {user.username}")

    def publish_post(self, post_type, *args):
        post = None
        if not self.connected:
            print("User is not connected. Cannot publish post.")
            return None

        if post_type == "Text":
            post = TextPost(self, *args)
        elif post_type == "Image":
            if len(args) == 1:
                post = ImagePost(self, args[0])
            else:
                print("Invalid number of arguments for ImagePost")
        elif post_type == "Sale":
            post = SalePost(self, *args)

        if post:
            post._owner = self
            self.posts.append(post)

            for follower in self.followers:
                follower.notify(f"{self.username} has a new post")

            if post_type != "Image":
                post.display()
                if isinstance(post, TextPost):
                    print()

            return post
        else:
            print(f"Invalid post type: {post_type}")
            return None

    def print_notifications(self):
        if self.connected:
            print(f"{self.username}'s notifications:")
            for notification in self.notifications:
                if notification is not None:
                    print(notification)
