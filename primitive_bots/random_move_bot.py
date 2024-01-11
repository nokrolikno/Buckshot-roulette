from random import choice
from engine.engine import PlayerAbstract
from engine.item import Action, ActionOutcome, ActorAction, Item, Nothing


class RandomMoveBot(PlayerAbstract):
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
        if not available:
            return Nothing()
        return choice(available)

