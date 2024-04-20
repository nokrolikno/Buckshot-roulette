from random import choice
from engine.engine import PlayerAbstract
from engine.item import Action, ActionOutcome, ActorAction, InitialShellCount, Item, Nothing, Shell, Shoot, PhoneCall


class DealerBot(PlayerAbstract):
    def __init__(self) -> None:
        super().__init__()
        self.live_count = 0
        self.blank_count = 0
        self.handcuffs_cooldown = 0
        self.gun_handsawed = False
        self.used_inverter = False
        self.memory_shells = []

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
            self.memory_shells = [Shell.Unknown] * (self.live_count + self.blank_count)
        if isinstance(action, ActorAction):
            if action.action_taken in [Shoot.You, Shoot.Opponent] and self.handcuffs_cooldown > 0:
                self.handcuffs_cooldown -= 1
            # If the action can change our count
            if action.action_taken in [Item.Beer, Shoot.You, Shoot.Opponent]:
                self.memory_shells.pop(0)
                if self.used_inverter:
                    if action_outcome == Shell.Live:
                        self.blank_count -= 1
                    if action_outcome == Shell.Blank:
                        self.live_count -= 1
                else:
                    if action_outcome == Shell.Live:
                        self.live_count -= 1
                    elif action_outcome == Shell.Blank:
                        self.blank_count -= 1
                self.used_inverter = False
            if action.action_taken == Item.Inverter:
                self.used_inverter = not self.used_inverter

            if action.action_taken == Item.Magnifier:
                if action_outcome != Shell.Unknown:
                    self.memory_shells[0] = action_outcome
            if action.action_taken == Item.Phone:
                if action_outcome.shell != Shell.Unknown:
                    self.memory_shells[action_outcome.number] = action_outcome.shell

        if not available:
            return Nothing()
        guaranteed_lethal = self.blank_count == 0 or self.memory_shells[0] == Shell.Live
        if Item.Cigarettes in available and my_hp < 4:
            return Item.Cigarettes
        if Item.Medicine in available and 1 < my_hp < 4:
            return Item.Medicine
        if (
            Item.Adrenaline in available
            and (Item.Cigarettes in opponent_items or Item.Medicine in opponent_items)
            and my_hp < 4
        ):
            return Item.Adrenaline
        if Item.Handcuffs in available and self.handcuffs_cooldown == 0:
            self.handcuffs_cooldown = 2
            return Item.Handcuffs
        if guaranteed_lethal and Item.HandSaw in available and not self.gun_handsawed:
            self.gun_handsawed = True
            return Item.HandSaw
        if (
            guaranteed_lethal
            and Item.Adrenaline in available
            and not self.gun_handsawed
            and Item.HandSaw in opponent_items
        ):
            return Item.Adrenaline
        if Item.Adrenaline in available and Item.Magnifier in opponent_items and self.memory_shells[0] == Shell.Unknown:
            return Item.Adrenaline
        if Item.Magnifier in available and self.memory_shells[0] == Shell.Unknown:
            return Item.Magnifier
        if Item.Adrenaline in available and Item.Phone in opponent_items and self.memory_shells[0] == Shell.Unknown:
            return Item.Adrenaline
        if Item.Phone in available and self.memory_shells[0] == Shell.Unknown:
            return Item.Phone
        if self.live_count == 0 or self.memory_shells[0] == Shell.Blank:
            if Item.Adrenaline in available and Item.Inverter in opponent_items:
                return Item.Adrenaline
            if Item.Inverter in available:
                self.memory_shells[0] == Shell.Live
                self.live_count += 1
                self.blank_count -= 1
                return Item.Inverter
            if Item.Adrenaline in available and Item.Beer in opponent_items:
                return Item.Adrenaline
            if Item.Beer in available:
                return Item.Beer
            return Shoot.You
        if guaranteed_lethal or self.gun_handsawed:
            self.gun_handsawed = False
            return Shoot.Opponent
        option = None
        while option is None:
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
            if option == Item.Medicine and my_hp >= 4:
                option = None
            if option == Item.Magnifier and self.memory_shells[0] != Shell.Unknown:
                option = None
            if option == Item.Adrenaline and (
                not opponent_items or all([x == Item.Adrenaline for x in opponent_items])
            ):
                option = None
        return option
