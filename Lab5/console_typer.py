from typing import NamedTuple
import console_logic

import typer

app = typer.Typer()

class CommandArgs(NamedTuple):
    parameter: str
    frequency: str
    begin: str
    end: str
    station: str = None

def parse_arguments(parameter, frequency, begin, end, station = None):
    return CommandArgs(
        parameter=parameter,
        frequency=frequency,
        begin=begin,
        end=end,
        station=station
    )

@app.command(help='Znajdź losową stację mierzącą dany parametr z daną dokładnością w danym czasie')
def random(
    parameter: str = typer.Argument(..., help='Szukana mierzona wielkość'),
    frequency: str = typer.Argument(..., help='Szukana częstotliwość'),
    begin: str = typer.Argument(..., help='Początek szukanego przedziału czasowego(YYYY-MM-DD)'),
    end: str = typer.Argument(..., help='Koniec szukanego przedziału czasowego(YYYY-MM-DD)')
):
    args = parse_arguments(parameter, frequency, begin, end)
    console_logic.handle_random(args)

@app.command(help = 'Policz średnią i odchylenie standardowe danego parametru z daną dokładnością zmierzoną na danej stacji w danym czasie')
def average(
    station: str = typer.Argument(..., help='Kod stacji, której dane chcemy zmierzyć'),
    parameter: str = typer.Argument(..., help='Szukana mierzona wielkość'),
    frequency: str = typer.Argument(..., help='Szukana częstotliwość'),
    begin: str = typer.Argument(..., help='Początek szukanego przedziału czasowego(YYYY-MM-DD)'),
    end: str = typer.Argument(..., help='Koniec szukanego przedziału czasowego(YYYY-MM-DD)')
):
    args = parse_arguments(parameter, frequency, begin, end, station)
    console_logic.handle_average(args)

if __name__ == '__main__':
    app()