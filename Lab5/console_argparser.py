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

sub_anomalies = subparser.add_parser('anomalies', help='Wyszukaj anomalie pomiarowe danej wielkości z określonej stacji i podanego czasu')
sub_anomalies.add_argument('station', help='Kod stacji, której anomalie chcemy zbadac')

if __name__ == '__main__':
    args = arg_parser.parse_args()
    if args.command == 'random':
        console_logic.handle_random(args)
    elif args.command == 'average':
        console_logic.handle_average(args)
    elif args.command == 'anomalies':
        console_logic.anomalies(args)

# python console_argparser.py average DsGlogWiStwo "As(PM10)" 24g 2023-01-01 2023-12-01
# python console_argparser.py random "As(PM10)" 24g 2023-01-01 2023-12-01
# python console_argparser.py anomalies DsGlogWiStwo "As(PM10)" 24g 2023-01-01 2023-12-01