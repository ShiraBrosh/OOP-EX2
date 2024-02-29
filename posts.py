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
        if user != self._owner:
            self.comments.append(user)
            print(f"notification to {self._owner.username}: {user.username} commented on your post: {text}")
            self._owner.notify(f"{user.username} commented on your post")
        else:
            self.comments.append(user)

    def like(self, user):
        if user != self._owner:
            if user not in self.likes:
                self.likes.append(user)
                print(f"notification to {self._owner.username}: {user.username} liked your post")
                self._owner.notify(f"{user.username} liked your post")
        else:
            self.comments.append(user)

    @abstractmethod
    def display(self):
        pass

    def __str__(self):
        if self.type == "Image":
            return f"{self._owner.username} posted a picture\n"
        else:
            return f"{self.display() or ''}"

class TextPost(Post):
    def __init__(self, name, text):
        super().__init__(name ,"text")
        self.text = text
    def display(self):
        print(f"{self._owner.username} published a post:\n\"{self.text}\"")
class SalePost(Post):
    def __init__(self, owner, product, price_in_NIS, location):
        super().__init__(owner, "sale")
        self.product = product
        self.price_in_NIS = price_in_NIS
        self.pick_up_location = location
        self.is_sold = False

    def sold(self, password):
        if self._owner.password == password:
            self.is_sold = True
            print(f"{self._owner.username}'s product is sold")

    def discount(self, percent, password):
        if self._owner.password == password and not self.is_sold:
            update = self.price_in_NIS * (percent / 100)
            self.price_in_NIS -= update
            print(f"Discount on {self._owner.username}'s product! The new price is: {self.price_in_NIS}")
        else:
            print("Invalid discount percentage. Please provide a valid number.")

    def display(self):
        if self.is_sold:
            print(f"{self._owner.username} posted a product for sale:\nSold! {self.product}, price: {self.price_in_NIS}, pickup from: {self.pick_up_location}")
        else:
            print(f"{self._owner.username} posted a product for sale:\nFor Sale! {self.product}, price: {self.price_in_NIS}, pickup from: {self.pick_up_location}\n")


class ImagePost(Post):
    def __init__(self, name, image_location):
        super().__init__(name, "Image")
        self.location_image = image_location

    def display(self):
        print("Shows picture")
        try:
            # Displaying image using Matplotlib
            img_matplotlib = plt.imread(self.location_image)
            plt.imshow(img_matplotlib)
            plt.axis('off')  # Turn off axis labels
            plt.show()

            # Displaying image using Pillow
            img_pillow = Image.open(self.location_image)
            img_pillow.show()

            return "Displayed an image."
        except FileNotFoundError:
            return "Failed to display image."

