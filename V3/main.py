from IconFactory import PokerFaceIconFactory, FlowerIconFactory, NullIconFactory, MyIconFactory
import argparse
import json
from component import Composite, Leaf
from TreeStyle import TreeStyle
from RectangleStyle import RectangleStyle
    
# 建造者模式
class FunnyJsonExplorerBuilder:
    def __init__(self, json_file):
        with open(json_file, 'r') as f:
            self.json_data = json.load(f)
        self.style = None
        self.icon_factory = None

    def with_style_and_icon_factory(self, style, icon_factory):
        self.style = style(icon_factory)
        return self

    def show(self):
        root = self.build('root', self.json_data)
        self.style.display(root)

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


if __name__ == "__main__":
    

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

    args = parser.parse_args()

    if args.icon == 'myicon':
        if not args.icon_set or len(args.icon_set) != 2:
            raise ValueError("When using 'myicon', you must provide an icon set with --icon-set containing middle and leaf icons.")
        icon_factory = MyIconFactory(args.icon_set[0], args.icon_set[1])
    elif args.icon == 'configfile':
        with open('icon_config.json', 'r', encoding='utf-8') as f:
            icon_config = json.load(f)
        icon_factory = MyIconFactory(icon_config['middle'], icon_config['leaf'])
    else:
        icon_factory_map = {
            'poker': PokerFaceIconFactory(),
            'flower': FlowerIconFactory(),
            'null': NullIconFactory(),
        }
        icon_factory = icon_factory_map[args.icon]

    style_map = {
        'tree': TreeStyle,
        'rectangle': RectangleStyle,
    }

    builder = FunnyJsonExplorerBuilder(args.file)
    builder.with_style_and_icon_factory(style_map[args.style], icon_factory).show()
