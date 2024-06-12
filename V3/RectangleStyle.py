from StyleFactory import StyleFactory
# 具体的风格类
class RectangleStyle(StyleFactory):
    max_width = 60

    def displayComposite(self, node, level, is_last, arg_list):
        icon = self.icon_factory.get_middle_icon()
        if level > 0:
            is_top = arg_list[0]
            if level == 1 and is_top:
                prefix = '┌'
                suffix = '┐'
            else:
                prefix = '├─ '
                suffix = '┤'
            line = "│  " * (level - 1) + prefix + icon + ' ' + node.name + ' '
            line_width = len(line)
            remain_width = self.max_width - 1 - line_width
            print(line + '─' * remain_width + suffix)
        # if level == 0 and is_last:
        #     print('└' + '─' * (self.max_width - 2) + '┘')

    def displayLeaf(self, node, level, is_last, arg_list):
        icon = self.icon_factory.get_leaf_icon()
        if level > 0:
            is_top = arg_list[0]
            if level == 1 and is_top:
                prefix = '┌'
                suffix = '┐'
            else:
                prefix = '├─ '
                suffix = '┤'
            line = "│  " * (level - 1) + prefix + icon + ' ' + node.name
            if node.value is not None:
                line += ': ' + str(node.value) + ' '
            line_width = len(line)
            remain_width = self.max_width - line_width - 1
            print(line + '─' * remain_width + suffix)
    
    def display(self, node, level=0, is_last=False, arg_list=[]):
        if node.children:
            self.displayComposite(node, level, is_last, arg_list)
            for i, child in enumerate(node.children):
                child_is_last = i == len(node.children) - 1
                is_top = i == 0
                arg_list.insert(0, is_top)
                self.display(child, level + 1, child_is_last, arg_list)
        else:
            self.displayLeaf(node, level, is_last, arg_list) 
        if level == 0:     
            print('└' + '─' * (self.max_width - 2) + '┘')
