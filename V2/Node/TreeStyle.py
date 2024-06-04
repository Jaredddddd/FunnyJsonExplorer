from StyleFactory import StyleFactory
from abc import abstractmethod
#-----------------------树型容器和叶子类-----------------------
class TreeFactory(StyleFactory):
    """
    树形结构的抽象工厂类，继承自 StyleFactory。
    """
    def __init__(self, name, icon_factory):
        # self.name = name
        # self.icon_factory = icon_factory
        super().__init__(name, icon_factory)
        

    @abstractmethod
    def display(self, level=0, is_last=False, arg_list=[]):
        pass

class Tree_Leaf(TreeFactory):
    """
    树形结构的叶子节点类，继承自 TreeFactory
    """
    def __init__(self, name, value, icon_factory):
        self.name = name
        self.icon_factory = icon_factory
        self.value = value

    def display(self, level=0, is_last=False, arg_list=[]):
        icon = self.icon_factory.get_leaf_icon()
        prefix = ''
        # 添加树形前缀
        for i in range(1, level):
            if i in arg_list:
                prefix += '│  '
            else:
                prefix += '   '
                
        prefix += '└─ ' if is_last else '├─ '
        # 打印叶子节点
        if self.value is None:
            line = prefix + icon + ' ' + self.name + ' '
        else:
            line = prefix + icon + ' ' + self.name + ': ' + str(self.value) + ' '
        print(line)

class Tree_Node(TreeFactory):
    """
    树形结构的容器节点类，继承自 TreeFactory
    """
    def display(self, level=0, is_last=False, arg_list=[]):
        icon = self.icon_factory.get_middle_icon()

        # 处理树形前缀
        if is_last and level in arg_list:
            arg_list.remove(level)
        if not is_last and level > 0:
            arg_list.append(level)
            
        if level > 0: # 根节点root不打印
            prefix = ''
            for i in range(1, level):
                if i in arg_list:
                    prefix += '│  '
                else:
                    prefix += '   '

            prefix += '└─ ' if is_last else '├─ '
            line = prefix + icon + ' ' + self.name
            print(line)
        
        
        # 递归显示子节点
        for i, child in enumerate(self.children):
            child_is_last = i == len(self.children) - 1
            child.display(level + 1, child_is_last, arg_list)
