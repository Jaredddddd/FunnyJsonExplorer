from abc import ABC, abstractmethod #ABC = Abstract Base Class


# 抽象产品：JSON可视化器
class JSONVisualizer(ABC):
    @abstractmethod
    def display(self):
        pass


# 具体产品1：树形样式可视化器
class TreeStyle(JSONVisualizer):
    def __init__(self, data, icon_factory):
        # super().__init__()
        self.data = data
        self.icon_factory = icon_factory

    def display(self):
        middle_icon = self.icon_factory.get_middle_icon()
        leaf_icon = self.icon_factory.get_leaf_icon()
        array_icon = self.icon_factory.get_array_icon()
        self._display_recursive(self.data, 0, middle_icon, leaf_icon, array_icon)

    # 修改递归显示方法以使用图标
    def _display_recursive(self, obj, depth, middle_icon, leaf_icon,array_icon, is_last=False):
        def print_with_indent(text, end='\n'):
            print("  " * depth + text, end=end)

        if isinstance(obj, dict):
            items = list(obj.items())
            for i, (k, v) in enumerate(items):
                prefix = "  " * depth
                if i == len(items) - 1:
                    icon = middle_icon if (isinstance(v, dict) or isinstance(v,list)) else leaf_icon
                    prefix += "└─" + icon + " "
                    is_last_item = True
                else:
                    icon = middle_icon if (isinstance(v, dict) or isinstance(v,list)) else leaf_icon
                    prefix += "├─" + icon + " "
                    is_last_item = False

                print(prefix + str(k), end='')
                if isinstance(v, dict):
                    print()  
                    self._display_recursive(v, depth + 1, middle_icon, leaf_icon,array_icon ,is_last_item)
                elif isinstance(v, str) and v:
                    print(": " + str(v))
                elif isinstance(v, list):
                    print()
                    self._display_recursive(v, depth + 1, middle_icon, leaf_icon,array_icon ,is_last_item)
                elif v is not None:
                    print(": " + str(v))
                else:
                    print()
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                last_item = i == len(obj) - 1
                self._display_recursive(item, depth + 1, middle_icon, leaf_icon,array_icon, last_item)        
        else:
            # 处理基本类型值，如字符串、整数等
            print_with_indent(array_icon+ " " + str(obj))

# 具体产品2：线性样式可视化器
class LinearStyle(JSONVisualizer):
    def __init__(self, data, icon_factory):
        self.data = data
        self.icon_factory = icon_factory

    def display(self):
        middle_icon = self.icon_factory.get_middle_icon()
        leaf_icon = self.icon_factory.get_leaf_icon()
        array_icon = self.icon_factory.get_array_icon()
        self._display_recursive(self.data, "", middle_icon, leaf_icon,array_icon)

    def _display_recursive(self, obj, prefix, middle_icon, leaf_icon,array_icon):
        if isinstance(obj,dict):
            for k, v in obj.items():
                icon = middle_icon if isinstance(v, dict) else leaf_icon
                print(prefix +icon+ " " + str(k), end='')
                
                if isinstance(v, dict):
                    print()  # 换行以便下一级缩进
                    self._display_recursive(v, prefix + "│   ", middle_icon, leaf_icon,array_icon)
                elif isinstance(v, str) and v:
                    print(": " + v)
                elif isinstance(v, list):
                    print()
                    self._display_recursive(v, prefix + "│   ", middle_icon, leaf_icon,array_icon)
                elif v is not None:
                    print(": " + str(v))
                else:
                    print()  # 对于非字典且无值的情况，简单换行
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                self._display_recursive(item, prefix, middle_icon, leaf_icon,array_icon)
        else:
            print(prefix + array_icon +" " + str(obj))
    

# 具体产品3：树形样式可视化器2
class TreeStyle2(JSONVisualizer):
    def __init__(self, data, icon_factory):
        self.data = data
        self.icon_factory = icon_factory

    def display(self):
        middle_icon = self.icon_factory.get_middle_icon()
        leaf_icon = self.icon_factory.get_leaf_icon()
        array_icon = self.icon_factory.get_array_icon()
        self._display_recursive(self.data, 1 ,middle_icon, leaf_icon,array_icon)

    
    def _display_recursive(self, obj, depth, middle_icon, leaf_icon,array_icon ,is_last_sibling=False):
        def print_with_indent(text, end='\n'):
            print("  " * depth + text, end=end)
        if isinstance(obj, dict):
            items = list(obj.items())
            for i, (k, v) in enumerate(items):
                # 添加或移除"│"取决于是否是同级中的最后一个元素
                prefix = "│   " * (depth - 1) + ("├─")
                icon = middle_icon if isinstance(v, dict) else leaf_icon
                # 计算并填充前缀的空白字符
                padded_prefix = prefix + icon +" " + str(k)
                print(padded_prefix, end='')

                if isinstance(v, dict):
                    print()  # 换行以便下一级缩进
                    # 传递当前项是否为同级最后一个的信息到下一层递归
                    self._display_recursive(v, depth + 1,middle_icon,leaf_icon,array_icon, i == len(items) - 1)
                elif isinstance(v, str) and v:
                    print(':',str(v))
                elif isinstance(v, list):
                    print()
                    self._display_recursive(v, depth + 1,middle_icon,leaf_icon,array_icon, i == len(items) - 1)
                elif v is not None:
                    print(':',str(v))
                else:
                    print()  # 对于非字典且无值的情况，简单换行
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                # 传递当前项是否为同级最后一个的信息到下一层递归
                self._display_recursive(item, depth, middle_icon, leaf_icon,array_icon , i == len(obj) - 1)
        else:
            print_with_indent(array_icon+ " " + str(obj))

    
# 具体产品4：矩形样式可视化器
class RectangleStyle(JSONVisualizer):
    def __init__(self, data, icon_factory):
        self.data = data
        self.icon_factory = icon_factory

    def display(self):
        middle_icon = self.icon_factory.get_middle_icon()
        leaf_icon = self.icon_factory.get_leaf_icon()
        array_icon = self.icon_factory.get_array_icon()
        max_widths = _calculate_max_widths(self.data)
        if max_widths >50:
            max_widths = 50
        # print(max_widths)
        self._display_recursive(self.data, 1 ,middle_icon, leaf_icon,array_icon, max_widths)

                        
    def _display_recursive(self, obj, depth, middle_icon, leaf_icon,array_icon, max_width=40):

        if isinstance(obj, dict):
            items = list(obj.items())
            for i, (key, value) in enumerate(items):
                # Add or remove "│" depending on whether it is the last element in the same level
                if depth == 1 and i == 0:
                    prefix = "│  " * (depth - 1) + "┌─"
                else:
                    prefix = "│  " * (depth - 1) + "├─"
                # prefix = "│  " * (depth - 1) + "├─"
                icon = middle_icon if isinstance(value, dict) else leaf_icon
                # Construct the prefix and the main content
                main_content = f"{prefix}{icon} {key}"
                
                if isinstance(value, dict):
                    # Calculate remaining width and fill with line continuation characters
                    remaining_width = max_width * 2 - len(main_content)
                    if depth == 1 and i == 0:
                        line_continuation = "─" * remaining_width + "┐"
                    else:
                        line_continuation = "─" * remaining_width + "┤"

                    print(main_content + line_continuation)
                    # Pass information about whether the current item is the last sibling to the next recursion level
                    self._display_recursive(value, depth + 1, middle_icon, leaf_icon,array_icon, max_width)
                
                elif isinstance(value, str) and value:
                    # Calculate remaining width and fill with line continuation characters
                    remaining_width = max_width * 2 - len(main_content) - len(value) - 2  # -2 for ": "
                    if depth == 1 and i == 0:
                        # line_continuation = "─" * remaining_width + "┘"
                        line_continuation = "─" * remaining_width + "┐"
                    else:
                        line_continuation = "─" * remaining_width + "┤"
                    print(f"{main_content}: {value}{line_continuation}")
                elif isinstance(value, list):
                    # Calculate remaining width and fill with line continuation characters
                    remaining_width = max_width * 2 - len(main_content)
                    line_continuation = "─" * remaining_width + "┤"
                    print(main_content + line_continuation)
                    # Pass information about whether the current item is the last sibling to the next recursion level
                    self._display_recursive(value, depth + 1, middle_icon, leaf_icon,array_icon ,max_width)
                elif value is not None:
                    # Calculate remaining width and fill with line continuation characters
                    remaining_width = max_width * 2 - len(main_content) - len(str(value)) - 2
                    print(main_content + f": {value}" + "─" * remaining_width + "┤")
                else:
                    # Calculate remaining width and fill with line continuation characters
                    remaining_width = max_width * 2 - len(main_content)
                    line_continuation = "─" * remaining_width + "┤"
                    print(main_content + line_continuation)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                # Pass information about whether the current item is the last sibling to the next recursion level
                self._display_recursive(item, depth, middle_icon, leaf_icon,array_icon, max_width)
        else:
            # Handle basic value types like strings, integers, etc.
            remaining_width = max_width * 2 - len(str(obj)) -2*depth -2
            line_continuation = "─" * remaining_width + "┤" 
            print("  " * depth + array_icon+ " " + str(obj) + line_continuation)
            # print_with_indent('+'+ " " + str(obj))
        
        # Print the cover after the last line
        if depth == 1 and len(items) > 0:
            remaining_width = max_width * 2-1
            cover_line = "─" * remaining_width
            print("└" + cover_line + "┘")

#------------------------------------------------------------------------------------------------------------

# 修改抽象工厂以接受图标工厂

class StyleFactory(ABC):
    @abstractmethod
    def create_visualizer(self, json_data, icon_factory):
        pass

# 具体工厂1：树形样式工厂
class TreeStyleFactory(StyleFactory):
    def create_visualizer(self, json_data, icon_factory):
        return TreeStyle(json_data, icon_factory)
    
# 具体工厂2：线性样式工厂
class LinearStyleFactory(StyleFactory):
    def create_visualizer(self, json_data, icon_factory):
        return LinearStyle(json_data, icon_factory)
    
# 具体工厂3：树形样式工厂2
class TreeStyleFactory2(StyleFactory):
    def create_visualizer(self, json_data,icon_factory):
        return TreeStyle2(json_data, icon_factory)

# 具体工厂4：矩形样式工厂
class RectangleFactory(StyleFactory):
    def create_visualizer(self, json_data, icon_factory):
        return RectangleStyle(json_data, icon_factory)
    



def _calculate_max_widths(obj, depth=0, max_widths=None):
    if max_widths is None:
        max_widths = {0: [0, 0]}  # 初始化，键为深度，值为[key_len, value_len]的列表
    
    items = list(obj.items()) if isinstance(obj, dict) else obj
    for i, (k, v) in enumerate(items):
        key_str = str(k)
        value_str = str(v) if not isinstance(v, dict) and v else ''
        key_len = len(key_str)
        value_len = len(value_str)
        
        # 确保当前深度的宽度信息已存在
        while depth + 1 not in max_widths:
            max_widths[depth + 1] = [0, 0]
        
        # 更新当前深度的最大键名长度和值长度
        max_widths[depth][0] = max(max_widths[depth][0], key_len)
        max_widths[depth][1] = max(max_widths[depth][1], value_len)
        
        if isinstance(v, dict):
            # 对子字典递归计算，同时确保下一层宽度信息已被初始化
            _calculate_max_widths(v, depth + 1, max_widths)

    max_key_length = max([width[0] for width in max_widths.values()])
    max_value_length = max([width[1] for width in max_widths.values()])
    # return max_widths
    return max_key_length+max_value_length



