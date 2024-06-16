from Component import Composite, Leaf
from abc import ABC, abstractmethod
import json
class DisplayStrategy(ABC):
    def __init__(self, icon_factory):
        self.icon_factory = icon_factory

    @abstractmethod
    def display(self, node, level, is_last, arg_list):
        pass


class TreeStrategy(DisplayStrategy):
    def display(self, node, level, is_last, arg_list):
        arg_list.pop(0)  # 移除根节点的is_top
        if isinstance(node, Composite):
            icon = self.icon_factory.get_middle_icon()
        else:
            icon = self.icon_factory.get_leaf_icon()
        if(level > 0):
            prefix = ''
            for i in range(1, level):
                if i in arg_list:
                    prefix += '│  '
                else:
                    prefix += '   '
            prefix += '└─ ' if is_last else '├─ '

            line = prefix + icon + ' ' + node.name
            if isinstance(node, Leaf) and node.value is not None:
                line += ': ' + str(node.value)
            print(line)

            if not is_last and level > 0 and level not in arg_list:
                arg_list.append(level)
            if is_last and level in arg_list:
                arg_list.remove(level)

    def displayEnd(self):
        return
        # print('└' + '─' * 60 + '┘')


class RectangleStrategy(DisplayStrategy):
    max_width = 60

    def display(self, node, level, is_last, arg_list):
        if isinstance(node, Composite):
            icon = self.icon_factory.get_middle_icon()
        else:
            icon = self.icon_factory.get_leaf_icon()

        prefix = "│  " * (level - 1)
        if level > 0:
            is_top = arg_list[0]
            # is_top = is_last
            if level == 1 and is_top:
                prefix += '┌'
                suffix = '┐'
            else:
                prefix += '├─ '
                suffix = '┤'
            line = prefix + icon + ' ' + node.name
            if isinstance(node, Leaf) and node.value is not None:
                line += ':' + str(node.value)
            line_width = len(line)
            remain_width = self.max_width - 1 - line_width
            print(line + '─' * remain_width + suffix)

        # if level == 0 and is_last:
        #     print('└' + '─' * (self.max_width - 2) + '┘')
    def displayEnd(self):
        print('└' + '─' * (self.max_width - 2) + '┘')


class Context:
    def __init__(self, json_file):
        with open(json_file, 'r') as f:
            self.json_data = json.load(f)
        self.strategy = None

    def setStrategy(self, style, icon_factory):
        self.strategy = style(icon_factory)
        return self

    def executeStrategy(self):
        root = self.build('root', self.json_data)
        arg_list = []
        for node, level, is_last, is_top in root:  # 使用迭代器遍历
            arg_list.insert(0, is_top)
            self.strategy.display(node, level, is_last, arg_list)
        self.strategy.displayEnd()

    def build(self, name, data, is_last=False):
        if isinstance(data, dict) or isinstance(data, list):
            composite = Composite(name, is_last=is_last)
            if isinstance(data, dict):
                for i, (key, value) in enumerate(data.items()):
                    child_is_last = i == len(data) - 1
                    composite.add(self.build(key, value, is_last=child_is_last))
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    child_is_last = i == len(data) - 1
                    composite.add(self.build(str(i), item, is_last=child_is_last))
            return composite
        else:
            return Leaf(name, data, is_last=is_last)