from abc import ABC, abstractmethod
from PIL import Image
import matplotlib.pyplot as plt


class Post(ABC):
    def __init__(self, nameofowner, post_type):
        self.likes = []
        self.comments = []
        self._owner = nameofowner
        self.type = post_type
        self.is_sold = True

    def comment(self, user, text):
        if user != self._owner:  # check if the user is the owner of the post
            self.comments.append(user)  # add the user to the end of the  comment list
            print(
                f"notification to {self._owner.username}: {user.username} commented on your post: {text}")  # if the user is not the owner of the post print the notification
            self._owner.notify(
                f"{user.username} commented on your post")  # add the notification to the owner of the post
        else:
            self.comments.append(user)  # if the user is the owner of the post only add the user to the end of the comment list but dont print the notofication

    def like(self, user):
        if user != self._owner:  # check if the user is the owner of the post
            if user not in self.likes:  # check if the user is not in the list of likes
                self.likes.append(user)  # add the user to the end of the list of likes
                print(
                    f"notification to {self._owner.username}: {user.username} liked your post")  # if the user is not the owner of the post print the notification
                self._owner.notify(f"{user.username} liked your post")
        else:
            self.like.append(user)  # if the user is the owner of the post only add the user to the end of the list of likes but dont print the notificatoin

    def __str__(self):
        if self.type == "Image":
            return f"{self._owner.username} posted a picture\n"
        else:
            return f"{self.display() or ''}"

    @abstractmethod
    def display(self):
        pass


class ImagePost(Post):
    def __init__(self, name, image_location):
        super().__init__(name, "Image")
        self.location_image = image_location

    def display(self):  # display the image
        print("Shows picture")
        try:
            img_matplotlib = plt.imread(self.location_image)  # read the image
            plt.imshow(img_matplotlib)  # display the image
            plt.axis('off')  # remove the axis
            plt.show()

            img_pillow = Image.open(self.location_image)  # open the image
            img_pillow.show()  # display the image

            return "Displayed an image."
        except FileNotFoundError:  # if the file is not found print the following message
            return "Failed to display image."


class TextPost(Post):
    def __init__(self, name, text):
        super().__init__(name, "text")
        self.text = text

    def display(self):
        print(f"{self._owner.username} published a post:\n\"{self.text}\"")


class SalePost(Post):
    def __init__(self, owner, product, price_in_NIS, location):
        super().__init__(owner, "sale")
        self.product = product
        self.price_in_NIS = price_in_NIS
        self.pick_up_location = location
        self.is_bought = False

    def sold(self, password):
        if self._owner.password == password:  # check if the password is correct
            self.is_bought = True  # change the status of the product to sold
            print(f"{self._owner.username}'s product is sold")

    def discount(self, percent, password):
        if self._owner.password == password and not self.is_bought:  # check if the password is correct and the product is not sold
            after_update = self.price_in_NIS * (percent / 100)  # calculate the new price after the discount
            self.price_in_NIS -= after_update
            print(f"Discount on {self._owner.username} product! the new price is: {self.price_in_NIS}")
        else:
            print("Invalid discount percentage. Please provide a valid number.")

    def display(self):
        if self.is_bought:
            print(
                f"{self._owner.username} posted a product for sale:\nSold! {self.product}, price: {self.price_in_NIS}, pickup from: {self.pick_up_location}")  # print the product is sold
        else:
            print(
                f"{self._owner.username} posted a product for sale:\nFor sale! {self.product}, price: {self.price_in_NIS}, pickup from: {self.pick_up_location}\n")


class PostFactory:  # factory design pattern
    TEXT = "text"
    IMAGE = "image"
    SALE = "sale"

    @staticmethod
    def create_post(post_type, **kwargs):
        if post_type == PostFactory.TEXT:  # check the type of the post
            content = kwargs.get('content', None)  # check the content of the post
            return TextPost(content)
        elif post_type == PostFactory.IMAGE:
            image_path = kwargs.get('image_path', None)
            return ImagePost(image_path)
        elif post_type == PostFactory.SALE:
            product = kwargs.get('product', None)
            price = kwargs.get('price', None)
            location = kwargs.get('location', None)
            return SalePost(product, price, location)
        else:
            raise ValueError(f"Invalid post type: {post_type}")
