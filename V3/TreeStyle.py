from StyleFactory import StyleFactory

class TreeStyle(StyleFactory):
    def displayComposite(self, node, level, is_last, arg_list):
        icon = self.icon_factory.get_middle_icon()
        if not is_last and level > 0 and level not in arg_list:
            arg_list.append(level)
        if is_last and level in arg_list:
            arg_list.remove(level)
        if level > 0:
            prefix = ''
            for i in range(1, level):
                if i in arg_list:
                    prefix += '│  '
                else:
                    prefix += '   '
            prefix += '└─ ' if is_last else '├─ '
            line = prefix + icon + ' ' + node.name
            print(line)

    def displayLeaf(self, node, level, is_last, arg_list):
        icon = self.icon_factory.get_leaf_icon()
        prefix = ''
        for i in range(1, level):
            if i in arg_list:
                prefix += '│  '
            else:
                prefix += '   '
        prefix += '└─ ' if is_last else '├─ '
        if node.value is None:
            line = prefix + icon + ' ' + node.name + ' '
        else:
            line = prefix + icon + ' ' + node.name + ': ' + str(node.value) + ' '
        print(line)

    def display(self, node, level=0, is_last=False, arg_list=[]):
        if node.children:
            self.displayComposite(node, level, is_last, arg_list)
            for i, child in enumerate(node.children):
                child_is_last = i == len(node.children) - 1
                # is_top = i == 0
                # arg_list.insert(0, is_top)
                self.display(child, level + 1, child_is_last, arg_list)
        else:
            self.displayLeaf(node, level, is_last, arg_list)     
