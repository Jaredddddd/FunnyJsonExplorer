from Strategy import TreeStrategy, RectangleStrategy, Context
from Icon import PokerFaceIconFactory, FlowerIconFactory, NullIconFactory, MyIconFactory


if __name__ == "__main__":
    import argparse
    import json

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
        'tree': TreeStrategy,
        'rectangle': RectangleStrategy,
    }

    context = Context(args.file)
    context.setStrategy(style_map[args.style], icon_factory).executeStrategy()
