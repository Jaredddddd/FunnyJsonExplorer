import argparse
import json
from Icon import PokerFaceIconFactory, FlowerIconFactory, NullIconFactory, myIconFactory
from container_strength import TreeStyleFactory, LinearStyleFactory, TreeStyleFactory2, RectangleFactory


class JSONVisualizerBuilder:
    def __init__(self, json_file):
        with open(json_file, 'r') as f:
            self.json_data = json.load(f)
        self.style_factory = None
        self.icon_factory = None
        
    def with_style_and_icon_factory(self, style_factory, icon_factory):
        self.style_factory = style_factory
        self.icon_factory = icon_factory
        return self

    def build(self):
        if not self.style_factory or not self.icon_factory:
            raise ValueError("Both style factory and icon factory must be set.")
        visualizer = self.style_factory.create_visualizer(self.json_data, self.icon_factory)
        visualizer.display()

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Funny JSON Explorer from ljw")
    help_str = """
Funny JSON Explorer from                                    
                _          ___          __   ___  __ ____   ___ ______ ____   ___  __ 
               | |        | \ \        / /  |__ \/_ |___ \ / _ \____  |___ \ / _ \/_ |
               | |        | |\ \  /\  / /      ) || | __) | | | |  / /  __) | (_) || |
               | |    _   | | \ \/  \/ /      / / | ||__ <| | | | / /  |__ < > _ < | |
               | |___| |__| |  \  /\  /      / /_ | |___) | |_| |/ /   ___) | (_) || |
               |______\____/    \/  \/      |____||_|____/ \___//_/   |____/ \___/ |_|                                                                                                                                                                 
    """
    parser = argparse.ArgumentParser(description=help_str,formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-f', '--file', help="Path to the JSON file", default='example.json')
    parser.add_argument('-s', '--style', choices=['tree', 'rectangle','tree2','linear'], default='tree', help="Style of the visualization (tree or rectangle)")
    parser.add_argument('-i', '--icon', choices=['poker','flower','null','myicon','configfile'], default='poker', help="Icon family to use for visualization,myicon can be set by yourself")
    parser.add_argument('--icon-set', nargs='+', help="Custom icons set for middle, leaf, and array icons respectively. Usage: --custom-icon-set '.middle_char' 'leaf_char' 'array_char'")

    args = parser.parse_args()

    if args.icon == 'myicon':
        if not args.icon_set or len(args.icon_set) != 3:
            print("Error: When using 'myicon', you must provide an icon set with --icon-set containing middle, leaf, and array icons.")
        print(f"your icon set is,middle:{args.icon_set[0]},lead:{args.icon_set[1]},array:{args.icon_set[2]} ")
        print()
        # 创建自定义图标工厂实例
        myIconFactory = type('myIconFactory', (object,), {
            'get_middle_icon': lambda self: args.icon_set[0],
            'get_leaf_icon': lambda self: args.icon_set[1],
            'get_array_icon': lambda self: args.icon_set[2],
        })
    elif args.icon == 'configfile':
        print("use config file to set icon")
        print()
        # 从配置文件中读取图标设置
        try:
            with open('icon_config.json', 'r',encoding='utf-8') as f:
                icon_config = json.load(f)
        except FileNotFoundError:
            print("Error: 'icon_config.json' not found.")
        except json.JSONDecodeError:
            print("Error: Unable to parse 'icon_config.json'. Please ensure it's a valid JSON file.")
        myIconFactory = type('myIconFactory', (object,), {
            'get_middle_icon': lambda self: icon_config['middle'],
            'get_leaf_icon': lambda self: icon_config['leaf'],
            'get_array_icon': lambda self: icon_config['array'],
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

    style_factory_map = {
        'tree': TreeStyleFactory(),
        'tree2': TreeStyleFactory2(),
        'rectangle': RectangleFactory(),
        'linear': LinearStyleFactory(),
    }

    builder = JSONVisualizerBuilder(args.file)
    builder.with_style_and_icon_factory(style_factory_map[args.style], icon_family_map[args.icon]).build()



