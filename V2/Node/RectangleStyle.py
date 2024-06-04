from StyleFactory import StyleFactory
from abc import abstractmethod

max_width = 60
#-----------------------矩形容器和叶子类-----------------------

class RectangleFactory(StyleFactory):
    """
    矩形结构的抽象工厂类，继承自 StyleFactory。
    """
    def __init__(self, name, icon_factory):
        # self.name = name
        # self.icon_factory = icon_factory
        super().__init__(name, icon_factory)

    @abstractmethod
    def display(self, level=0, is_last=False, arg_list=[]):
        pass

class Rectangle_Leaf(RectangleFactory):
    """
    矩形结构的叶子节点类，继承自 RectangleFactory。
    """
    def __init__(self, name, value, icon_factory):
        self.name = name
        self.icon_factory = icon_factory
        self.value = value
        
    def display(self, level=0, is_last=False, arg_list=[]):
        icon = self.icon_factory.get_leaf_icon()
        is_top = arg_list[0]
        
        # 设置前缀和后缀
        if level == 1 and is_top:
            prefix = '┌'
            suffix = '┐'
        else:
            prefix = '├─ '
            suffix = '┤'

        # 构建输出行
        line = "│  " * (level - 1) + prefix + icon + ' ' + self.name
        if self.value is None:
            line += ' '
        else:
            line += ': ' + str(self.value) + ' '

        # 计算剩余宽度，确保对齐
        line_width = len(line)
        remain_width = max_width - line_width - 1
        print(line + '─' * remain_width + suffix)

class Rectangle_Node(RectangleFactory):
    """
    矩形结构的容器节点类，继承自 RectangleFactory。
    """
    def display(self, level=0, is_last=False, arg_list=[]):
        icon = self.icon_factory.get_middle_icon()
        
        if level > 0:
            is_top = arg_list[0]
            if level == 1 and is_top:
                prefix = '┌'
                suffix = '┐'
            else:
                prefix = '├─ '
                suffix = '┤'

            # 构建输出行
            line = "│  " * (level - 1) + prefix + icon + ' ' + self.name + ' '
            line_width = len(line)
            remain_width = max_width - 1 - line_width
            print(line + '─' * remain_width + suffix)

        # 递归显示子节点
        for i, child in enumerate(self.children):
            child_is_last = i == len(self.children) - 1
            is_top = i == 0
            arg_list.insert(0, is_top)
            child.display(level + 1, child_is_last, arg_list)

        # 矩形最后一行封上
        if level == 0:
            print('└' + '─' * (max_width - 2) + '┘')