from Iterator import Collection, Iterator
# 组合模式：定义抽象组件
class Component:  
    def __init__(self, name, children=None, is_last=0):
        self.name = name
        self.children = children if children is not None else []
        self.is_last = is_last

    def add(self, child):
        self.children.append(child)

    def __iter__(self):
        return iter(ComponentCollection(self))


class Leaf(Component):
    def __init__(self, name, value, is_last=0):
        super().__init__(name, children=[], is_last=is_last)
        self.value = value


class Composite(Component):
    def __init__(self, name, is_last=0):
        super().__init__(name, children=[], is_last=is_last)
        
class ComponentCollection(Collection):
    def __init__(self, root):
        self.iterator = ComponentIterator(root)

    def __iter__(self):
        return self.iterator

    def __next__(self):
        return next(self.iterator)


class ComponentIterator(Iterator):
    def __init__(self, root):
        self.stack = [(root, 0, False, False)]  # (node, level, is_last)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration

        node, level, is_last, is_top = self.stack.pop()
        if isinstance(node, Composite):
            for i, child in enumerate(reversed(node.children)):
                self.stack.append((child, level + 1, i == 0, i == len(node.children) - 1))
        return node, level, is_last, is_top