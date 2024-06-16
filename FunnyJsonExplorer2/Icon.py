from abc import ABC, abstractmethod
class IconFactory(ABC):
    @abstractmethod
    def get_middle_icon(self):
        pass

    @abstractmethod
    def get_leaf_icon(self):
        pass


class PokerFaceIconFactory(IconFactory):
    def get_middle_icon(self):
        return "♢"

    def get_leaf_icon(self):
        return "♤"


class FlowerIconFactory(IconFactory):
    def get_middle_icon(self):
        return "❀"

    def get_leaf_icon(self):
        return "✿"


class NullIconFactory(IconFactory):
    def get_middle_icon(self):
        return ""

    def get_leaf_icon(self):
        return ""


class MyIconFactory(IconFactory):
    def __init__(self, middle, leaf):
        self.middle_icon = middle
        self.leaf_icon = leaf

    def get_middle_icon(self):
        return self.middle_icon

    def get_leaf_icon(self):
        return self.leaf_icon