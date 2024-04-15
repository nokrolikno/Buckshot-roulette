from enum import Enum, auto
from functools import total_ordering


class Action:
    pass


@total_ordering
class Item(Action, Enum):
    Beer = auto()
    Cigarettes = auto()
    Handcuffs = auto()
    HandSaw = auto()
    Magnifier = auto()
    Phone = auto()
    Adrenaline  = auto()
    Inverter = auto()
    Medicine = auto()

    def __le__(self, __value: object) -> bool:
        if isinstance(__value, Item):
            return self.value < __value.value
        else:
            return False

    def __str__(self):
        return self.name


class Shoot(Action, Enum):
    You = auto()
    Opponent = auto()

    def __str__(self):
        return self.name


class RoundStart(Action):
    def __str__(self):
        return 'Round Start'


class Nothing(Action):
    def __str__(self):
        return 'Nothing'


class ActorAction:
    def __init__(self, actor, action_taken):
        self.actor = actor
        self.action_taken = action_taken

    def __str__(self):
        return str(self.actor) + ' ' + str(self.action_taken)


class ActionOutcome:
    pass


class Shell(ActionOutcome, Enum):
    Live = auto()
    Blank = auto()
    Unknown = auto()

    def __str__(self):
        return self.name
    
class PhoneCall(ActionOutcome):
    number = 0
    shell = Shell.Unknown

    def __init__(self, number, shell):
        self.number = number
        self.shell = shell
    
    def __str__(self):
        return f"SHELL NO. {self.number + 1} ... {self.shell.name}."


class InitialShellCount(ActionOutcome):
    def __init__(self, live_count, blank_count):
        self.live_count = live_count
        self.blank_count = blank_count

    def __str__(self):
        return f'LIVE {self.live_count} BLANK {self.blank_count}'
