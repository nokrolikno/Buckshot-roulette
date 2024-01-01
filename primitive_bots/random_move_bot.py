from random import choice
from engine.engine import PlayerAbstract, Engine


class RandomMoveBot(PlayerAbstract):
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
        if not available:
            return 'NOTHING'
        return choice(available)

