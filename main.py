from cli_player.cli_player import CLIPlayer
from engine.engine import Engine
from primitive_bots.random_move_bot import RandomMoveBot


def main():
    player1 = CLIPlayer(input('Введите имя игрока: '))
    player2 = RandomMoveBot()
    print(Engine(player1, player2).start())


if __name__ == '__main__':
    main()
