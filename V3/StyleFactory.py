from abc import ABC, abstractmethod
# 工厂方法：定义风格类
class StyleFactory(ABC):
    def __init__(self, icon_factory):
        self.icon_factory = icon_factory

    @abstractmethod
    def displayComposite(self, node, level, is_last, arg_list):
        pass

    @abstractmethod
    def displayLeaf(self, node, level, is_last, arg_list):
        pass

    def display(self, node, level=0, is_last=False, arg_list=[]):
        pass