from engine.engine import PlayerAbstract
from engine.item import Action, ActionOutcome, ActorAction, Item, Nothing, RoundStart
import time

class CLIPlayer(PlayerAbstract):
    def __init__(self, number, language):
        self.number = number
        self.language = language

    def make_move(
            self,
            my_hp: int,
            opponent_hp: int,
            my_items: list[Item],
            opponent_items: list[Item],
            action: ActorAction,
            action_outcome: ActionOutcome,
            available: list[Action],
    ):
        if not isinstance(action, RoundStart):
            print(self.language.acting_player(), end='')
            print(self.number if len(available) > 0 else 'Opponent')
        print(self.language.hp(), end='')
        print(my_hp)
        print(self.language.opponent_hp(), end='')
        print(opponent_hp)
        print(self.language.my_items(), end='')
        print(describe_items(my_items))
        print(self.language.opponent_items(), end='')
        print(describe_items(opponent_items))
        print(self.language.action(), end='')
        print(str(action))
        print(self.language.action_result(), end='')
        print(str(action_outcome))
        if len(available) > 0:
            move = None
            text_moves = list(map(lambda x: str(x).lower(), available))
            while move == None:
                print(self.language.available_moves(), end='')
                print(', '.join(map(str, available)))
                try:
                    move = available[text_moves.index(input(self.language.my_move()).lower())]
                except ValueError:
                    pass

        else:
            time.sleep(2)
            move = Nothing()
        print('-----------------------------')
        return move


def describe_items(items: list[Item]) -> str:
    items = items.copy()
    items.sort()
    ret = []
    last_item = None
    count_of_last_item = 1
    while items or last_item != None:
        try:
            item = items.pop()
        except IndexError:
            item = None
        if last_item == item:
            count_of_last_item += 1
        elif last_item != None:
            if count_of_last_item > 1:
                ret.append(f'{str(last_item)} x{count_of_last_item}')
            else:
                ret.append(str(last_item))
            count_of_last_item = 1
            last_item = None
        last_item = item
    return ', '.join(ret)
