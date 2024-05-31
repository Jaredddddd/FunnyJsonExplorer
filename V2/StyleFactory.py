from abc import ABC, abstractmethod

max_width = 60

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

#-----------------------树型容器和叶子类-----------------------
class TreeFactory(StyleFactory):
    """
    树形结构的抽象工厂类，继承自 StyleFactory。
    """
    def __init__(self, name, icon_factory):
        super().__init__(name, icon_factory)

    @abstractmethod
    def display(self, level=0, is_last=False, arg_list=[]):
        pass

class Tree_Leaf(StyleFactory):
    """
    树形结构的叶子节点类，继承自 StyleFactory。
    """
    def __init__(self, name, value, icon_factory):
        super().__init__(name, icon_factory)
        self.value = value

    def display(self, level=0, is_last=False, arg_list=[]):
        icon = self.icon_factory.get_leaf_icon()
        prefix = '└─ ' if is_last else '├─ '
        
        # 打印树形前缀
        for i in range(1, level):
            if i in arg_list:
                print('│  ', end='')
            else:
                print('   ', end='')

        # 打印叶子节点
        if self.value is None:
            line = prefix + icon + ' ' + self.name + ' '
        else:
            line = prefix + icon + ' ' + self.name + ': ' + str(self.value) + ' '
        print(line)

class Tree_Node(StyleFactory):
    """
    树形结构的容器节点类，继承自 StyleFactory。
    """
    def display(self, level=0, is_last=False, arg_list=[]):
        icon = self.icon_factory.get_middle_icon()
        prefix = '└─ ' if is_last else '├─ '

        # 删除多余竖线
        if is_last and level in arg_list:
            arg_list.remove(level)
            
        for i in range(1, level):
            if i in arg_list:
                print('│  ', end='')
            else:
                print('   ', end='')

        # 打印树节点
        if level > 0:
            print(prefix + icon + ' ' + self.name)   
        if not is_last and level > 0:
            arg_list.append(level)
            
        # 递归显示子节点
        for i, child in enumerate(self.children):
            child_is_last = i == len(self.children) - 1
            child.display(level + 1, child_is_last, arg_list)

#-----------------------矩形容器和叶子类-----------------------

class RectangleFactory(StyleFactory):
    """
    矩形结构的抽象工厂类，继承自 StyleFactory。
    """
    def __init__(self, name, icon_factory):
        super().__init__(name, icon_factory)

    @abstractmethod
    def display(self, level=0, is_last=False, arg_list=[]):
        pass

class Rectangle_Leaf(RectangleFactory):
    """
    矩形结构的叶子节点类，继承自 RectangleFactory。
    """
    def __init__(self, name, value, icon_factory):
        super().__init__(name, icon_factory)
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
        remaining_width = max_width - line_width - 1
        print(line + '─' * remaining_width + suffix)

class Rectangle_Node(RectangleFactory):
    """
    矩形结构的容器节点类，继承自 RectangleFactory。
    """
    def display(self, level=0, is_last=False, arg_list=[]):
        icon = self.icon_factory.get_middle_icon()
        
        if level != 0:
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
            remaining_width = max_width - 1 - line_width
            print(line + '─' * remaining_width + suffix)

        # 递归显示子节点
        for i, child in enumerate(self.children):
            child_is_last = i == len(self.children) - 1
            is_top = i == 0
            arg_list.insert(0, is_top)
            child.display(level + 1, child_is_last, arg_list)

        # 矩形容器的最后一行
        if level == 0:
            print('└' + '─' * (max_width - 2) + '┘')

