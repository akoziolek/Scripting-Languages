import argparse
import console_logic

arg_parser = argparse.ArgumentParser()
subparser = arg_parser.add_subparsers(dest = 'command')
subparser.add_parser('random', help='Znajdź losową stację mierzącą dany parametr z daną dokładnością w danym czasie')
sub = subparser.add_parser('average', help = 'Policz średnią i odchylenie standardowe danego parametru z daną dokładnością zmierzoną na danej stacji w danym czasie')
sub.add_argument('station', help='Kod stacji, której dane chcemy zmierzyć')
arg_parser.add_argument('parameter', help = 'Szukana mierzona wielkość')
arg_parser.add_argument('frequency', help = 'Szukana częstotliwość')
arg_parser.add_argument('begin', help = 'Początek szukanego przedziału czasowego(YYYY-MM-DD)')
arg_parser.add_argument('end', help = 'Koniec szukanego przedziału czasowego(YYYY-MM-DD)')

if __name__ == '__main__':
    args = arg_parser.parse_args()
    if args.command == 'random':
        console_logic.handle_random(args)
    elif args.command == 'average':
        console_logic.handle_average(args)