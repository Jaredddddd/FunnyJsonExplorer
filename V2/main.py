import argparse
import json
from Icon import PokerFaceIconFactory, FlowerIconFactory, NullIconFactory, myIconFactory
# from StyleFactory import Tree_Leaf, Tree_Node, Rectangle_Leaf, Rectangle_Node
from Node.TreeStyle import Tree_Leaf, Tree_Node
from Node.RectangleStyle import Rectangle_Leaf, Rectangle_Node

# 建造者模式
class FunnyJsonExplorerBulider:
    def __init__(self, json_file):
        # 读取并加载 JSON 文件
        with open(json_file, 'r') as f:
            self.json_data = json.load(f)
        self.LeafStyle_factory = None
        self.NodeStyle_factory = None
        self.icon_factory = None   

    def with_style_and_icon_factory(self, LeafStyle_factory, NodeStyle_factory, icon_factory):
        # 设置叶子节点样式工厂、节点样式工厂和图标工厂
        self.LeafStyle_factory = LeafStyle_factory
        self.NodeStyle_factory = NodeStyle_factory
        self.icon_factory = icon_factory
        return self

    def show(self):
        # 构建根节点并显示
        root = self.build('root', self.json_data)
        # 调用多态的 display 方法
        root.display()

    def build(self, name, data):
        # 根据名称和数据构建节点或叶子节点
        StyleFactory = self.NodeStyle_factory(name, self.icon_factory)
        
        if isinstance(data, dict):
            # 如果数据是字典，遍历键值对
            for key, value in data.items():
                if isinstance(value, dict) or isinstance(value, list):
                    # 如果值是字典或列表，递归构建子节点
                    child_container = self.build(key, value)
                    StyleFactory.add(child_container)
                else:
                    # 否则，创建叶子节点
                    leaf = self.LeafStyle_factory(key, value, self.icon_factory)
                    StyleFactory.add(leaf)
        elif isinstance(data, list):
            # 如果数据是列表，遍历元素
            for index, item in enumerate(data):
                if isinstance(item, dict) or isinstance(item, list):
                    # 如果元素是字典或列表，递归构建子节点
                    child_container = self.build(str(index), item)
                    StyleFactory.add(child_container)
                else:
                    # 否则，创建叶子节点
                    leaf = self.LeafStyle_factory(str(index), item, self.icon_factory)
                    StyleFactory.add(leaf)            
        return StyleFactory


if __name__ == "__main__":
    # 设置命令行参数解析器
    help_str = """
Funny JSON Explorer from                                    
                _          ___          __   ___  __ ____   ___ ______ ____   ___  __ 
               | |        | \ \        / /  |__ \/_ |___ \ / _ \____  |___ \ / _ \/_ |
               | |        | |\ \  /\  / /      ) || | __) | | | |  / /  __) | (_) || |
               | |    _   | | \ \/  \/ /      / / | ||__ <| | | | / /  |__ < > _ < | |
               | |___| |__| |  \  /\  /      / /_ | |___) | |_| |/ /   ___) | (_) || |
               |______\____/    \/  \/      |____||_|____/ \___//_/   |____/ \___/ |_|                                                                                                                                                                 
    """
    parser = argparse.ArgumentParser(description=help_str, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--file', help="Path to the JSON file", default='strength.json')
    parser.add_argument('-s', '--style', choices=['tree', 'rectangle'], default='rectangle', help="Style of the visualization (tree or rectangle)")
    parser.add_argument('-i', '--icon', choices=['poker', 'flower', 'null', 'myicon', 'configfile'], default='poker', help="Icon family to use for visualization, myicon can be set by yourself")
    parser.add_argument('--icon-set', nargs='+', help="Custom icons set for middle, leaf, and array icons respectively. Usage: --custom-icon-set '.middle_char' 'leaf_char'")

    # 解析命令行参数
    args = parser.parse_args()

    # 处理自定义图标工厂的情况
    if args.icon == 'myicon':
        if not args.icon_set or len(args.icon_set) != 2:
            print("Error: When using 'myicon', you must provide an icon set with --icon-set containing middle, leaf, and array icons.")
        print(f"your icon set is, middle: {args.icon_set[0]}, lead: {args.icon_set[1]}")
        print()
        # 创建自定义图标工厂实例
        myIconFactory = type('myIconFactory', (object,), {
            'get_middle_icon': lambda self: args.icon_set[0],
            'get_leaf_icon': lambda self: args.icon_set[1],
        })
    elif args.icon == 'configfile':
        print("use config file to set icon")
        print()
        # 从配置文件中读取图标设置
        try:
            with open('icon_config.json', 'r', encoding='utf-8') as f:
                icon_config = json.load(f)
        except FileNotFoundError:
            print("Error: 'icon_config.json' not found.")
        except json.JSONDecodeError:
            print("Error: Unable to parse 'icon_config.json'. Please ensure it's a valid JSON file.")
        myIconFactory = type('myIconFactory', (object,), {
            'get_middle_icon': lambda self: icon_config['middle'],
            'get_leaf_icon': lambda self: icon_config['leaf'],
        })

    # 根据图标族选择类
    icon_family_map = {
        'poker': PokerFaceIconFactory(),
        'flower': FlowerIconFactory(),
        'null': NullIconFactory(),
    }
    if args.icon == 'myicon':
        icon_family_map['myicon'] = myIconFactory()
    elif args.icon == 'configfile':
        icon_family_map['configfile'] = myIconFactory()

    # 定义叶子节点样式和节点样式的映射
    LeafStyle_map = {
        'tree': Tree_Leaf,
        'rectangle': Rectangle_Leaf,
    }
    NodeStyle_map = {
        'tree': Tree_Node,
        'rectangle': Rectangle_Node,
    }

    print()
    # 创建 FunnyJsonExplorerBuilder 实例并设置样式和图标工厂，然后显示
    builder = FunnyJsonExplorerBulider(args.file)
    builder.with_style_and_icon_factory(LeafStyle_map[args.style], NodeStyle_map[args.style], icon_family_map[args.icon]).show()
