from abc import ABC, abstractmethod



# 定义容器和叶子类(叶子是特殊的容器)
class StyleFactory(ABC):
    """
    抽象基类，用于定义节点（容器）和叶子节点的共同接口。
    """
    def __init__(self, name, icon_factory):
        self.name = name
        self.icon_factory = icon_factory
        self.children = []

    def add(self, component):
        # 添加子组件到 children 列表中
        self.children.append(component)

    @abstractmethod
    def display(self, level=0, is_last=False, arg_list=[]):
        # 抽象方法，子类必须实现
        pass




