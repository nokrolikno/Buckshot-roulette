from random import choice
from engine.engine import PlayerAbstract
from engine.item import Action, ActionOutcome, ActorAction, InitialShellCount, Item, Nothing, Shell, Shoot


class DealerBot(PlayerAbstract):
    def __init__(self) -> None:
        super().__init__()
        self.live_count = 0
        self.blank_count = 0
        self.handcuffs_cooldown = 0
        self.known_shell = None
        self.gun_handsawed = False

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
        if isinstance(action_outcome, InitialShellCount):
            self.live_count = action_outcome.live_count
            self.blank_count = action_outcome.blank_count
        if isinstance(action, ActorAction):
            if action.action_taken in [Shoot.You, Shoot.Opponent] and self.handcuffs_cooldown > 0:
                self.handcuffs_cooldown -= 1
            # If the action can change our count
            if action.action_taken in [Item.Beer, Shoot.You, Shoot.Opponent]:
                self.known_shell = None
                if action_outcome == Shell.Live:
                    self.live_count -= 1
                elif action_outcome == Shell.Blank:
                    self.blank_count -= 1
            if action.action_taken == Item.Magnifier:
                if action_outcome != Shell.Unknown:
                    self.known_shell = action_outcome
        if not available:
            return Nothing()
        guaranteed_lethal = self.blank_count == 0 or self.known_shell == Shell.Live
        if Item.Cigarettes in available and my_hp < 4:
            return Item.Cigarettes
        if Item.Handcuffs in available and self.handcuffs_cooldown == 0:
            self.handcuffs_cooldown = 2
            return Item.Handcuffs
        if guaranteed_lethal and Item.HandSaw in available and not self.gun_handsawed:
            self.gun_handsawed = True
            return Item.HandSaw
        if Item.Magnifier in available and self.known_shell == None:
            return Item.Magnifier
        if self.live_count == 0 or self.known_shell == Shell.Blank:
            if Item.Beer in available:
                return Item.Beer
            else:
                return Shoot.You
        if guaranteed_lethal or self.gun_handsawed:
            self.gun_handsawed = False
            return Shoot.Opponent
        option = None
        while option == None:
            option = choice(available)
            if option == Item.HandSaw:
                if self.gun_handsawed:
                    option = None
                else:
                    self.gun_handsawed = True
            if option == Item.Handcuffs and self.handcuffs_cooldown > 0:
                option = None
            if option == Item.Cigarettes and my_hp >= 4:
                option = None
            if option == Item.Magnifier and self.known_shell != None:
                option = None
        return option


