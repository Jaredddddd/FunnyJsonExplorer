

# 组合模式：定义抽象组件
class Component:
    def __init__(self, name, children=None, is_last=0):
        self.name = name
        self.children = children if children is not None else []
        self.is_last = is_last

    def add(self, child):
        self.children.append(child)


# 定义叶子节点组件，继承自 Component
class Leaf(Component):
    def __init__(self, name, value, is_last=0):
        super().__init__(name, children=[], is_last=is_last)
        self.value = value

# 定义非叶子节点组件，继承自 Component
class Composite(Component):
    def __init__(self, name, is_last=0):
        super().__init__(name, children=[], is_last=is_last)