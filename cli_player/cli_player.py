from engine.engine import PlayerAbstract


class CLIPlayer(PlayerAbstract):
    def __init__(self, number, language):
        self.number = number
        self.language = language

    def make_move(
            self,
            my_hp: int,
            opponent_hp: int,
            my_items: list[str],
            opponent_items: list[str],
            action: str,
            action_result: str,
            available: list[str],
    ):
        print(self.language.acting_player(), end='')
        print(self.number)
        print(self.language.hp(), end='')
        print(my_hp)
        print(self.language.opponent_hp(), end='')
        print(opponent_hp)
        print(self.language.my_items(), end='')
        print(my_items)
        print(self.language.opponent_items(), end='')
        print(opponent_items)
        print(self.language.action(), end='')
        print(action)
        print(self.language.action_result(), end='')
        print(action_result)
        if len(available) > 0:
            print(self.language.available_moves(), end='')
            print(available)
            move = input(self.language.my_move())
        else:
            move = 'NOTHING'
        print('-----------------------------')
        return move
