from cli_player.cli_player import CLIPlayer
from engine.engine import Engine
from dealer.dealer import DealerBot
from language.language import pick_language


def main():
    language = pick_language()
    player1 = CLIPlayer(input(language.greeting()), language)
    player2 = DealerBot()
    print(Engine(player1, player2).start())


if __name__ == "__main__":
    main()
