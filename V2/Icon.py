from abc import ABC, abstractmethod #ABC = Abstract Base Class

# 抽象图标工厂
class IconFactory(ABC):
    @abstractmethod
    def get_middle_icon(self):
        pass

    @abstractmethod
    def get_leaf_icon(self):
        pass



# 具体图标工厂：扑克脸图标集
class PokerFaceIconFactory(IconFactory):
    def get_middle_icon(self):
        return "♢"

    def get_leaf_icon(self):
        return "♤"
    


# 具体图标工厂：花图标集
class FlowerIconFactory(IconFactory):
    def get_middle_icon(self):
        return "❀"

    def get_leaf_icon(self):
        return "✿"
    


# 具体图标工厂：空集
class NullIconFactory(IconFactory):
    def get_middle_icon(self):
        return ""

    def get_leaf_icon(self):
        return ""
    

    

# 命令行自定义图标工厂
class myIconFactory(IconFactory):
    def __init__(self,middle,leaf,array):
        self.middle_icon = middle
        self.leaf_icon = leaf


    def get_middle_icon(self):
        return self.middle_icon

    def get_leaf_icon(self):
        return self.leaf_icon
    
