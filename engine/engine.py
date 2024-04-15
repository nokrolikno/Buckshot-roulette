import random
from engine.item import Item, Action, ActorAction, Shoot, RoundStart, Nothing, ActionOutcome, Shell, InitialShellCount, PhoneCall
from abc import ABC, abstractmethod


class PlayerAbstract(ABC):
    @abstractmethod
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
        """
        :param my_hp: int, your current HP.

        :param opponent_hp: int, opponent`s current HP.

        :param my_items: list[str], list of all your items.
        Example: ['BEER', 'BEER', 'CIGARETTES', 'HANDCUFFS', 'HAND_SAW', 'MAGNIFIER']

        :param opponent_items: list[str], list of all opponents items.
        Example: ['BEER', 'BEER', 'CIGARETTES', 'HANDCUFFS', 'HAND_SAW', 'MAGNIFIER']

        :param action: str, string containing action as input. It builds like this:
            '{1} {2}'
            1 - [YOU, OPPONENT, BASE] - who did the action or 'BASE' if it is general action
            2 - [YOU, OPPONENT, BEER, CIGARETTES, HANDCUFFS, HAND_SAW, MAGNIFIER, ROUND_START] - the action itself where
                YOU, OPPONENT - stands for shooting you or opponent
                BEER, CIGARETTES, HANDCUFFS, HAND_SAW, MAGNIFIER - using an item
                ROUND_START - start of the round, action_result will contain number of live and blank rounds
        Example: 'YOU YOU' - means you shoot yourself
                 'YOU HANDCUFFS' - means you use handcuffs on your opponent
                 'BASE ROUND_START' - start of the round

        :param action_result: str, string containing result of the action. May be:
                [LIVE, BLANK] - if action was shooting someone, using beer, or you used magnifier
                'N LIVE, M BLANK' - if action was ROUND_START
                '' - empty string otherwise
        Example: '2 LIVE, 3 BLANK'
                 'BLANK'

        :param available: list[str] - list of available actions. if it is empty, you must return 'NOTHING'.
        Example: ['YOU', 'OPPONENT', 'BEER', 'CIGARETTES', 'HANDCUFFS', 'HAND_SAW', 'MAGNIFIER']

        :return: str, one of the available actions or 'NOTHING' if available empty.
        Example: 'BEER'
                 'NOTHING'
        """
        pass


class Player:
    def __init__(self, hp: int, handler: PlayerAbstract):
        self.hp = hp
        self.items = []
        self.handler = handler


class Engine:
    ITEMS = [Item.Beer, Item.Cigarettes, Item.Handcuffs, Item.HandSaw, Item.Magnifier, Item.Phone, Item.Inverter, Item.Medicine, Item.Adrenaline]

    def __init__(
        self,
        player1: PlayerAbstract,
        player2: PlayerAbstract,
        hp=4,
        max_items=8,
        draw_items=4,
        min_bullets=3,
        max_bullets=8,
    ):
        self.player1 = Player(hp, player1)
        self.player2 = Player(hp, player2)
        self.max_hp = hp
        self.max_items = max_items
        self.draw_items = draw_items
        self.min_bullets = min_bullets
        self.max_bullets = max_bullets

        if min_bullets < 2:
            raise ValueError('min_bullets must be 2 or higher')

    def initialize_round(self):
        for i in range(self.draw_items):
            if len(self.player1.items) >= self.max_items:
                break
            self.player1.items.append(random.choice(self.ITEMS))
        for i in range(self.draw_items):
            if len(self.player2.items) >= self.max_items:
                break
            self.player2.items.append(random.choice(self.ITEMS))
        total_bullets = random.randint(self.min_bullets, self.max_bullets)
        live_bullets = random.randint(1, total_bullets - 1)
        blank_bullets = total_bullets - live_bullets
        chamber = [Shell.Live for i in range(live_bullets)] + [Shell.Blank for j in range(blank_bullets)]
        random.shuffle(chamber)
        return live_bullets, blank_bullets, chamber

    def get_move(self, player_number: int, action: Action, action_result: ActorAction, available: list[Action]):
        player = self.player1 if player_number == 1 else self.player2
        opponent = self.player2 if player_number == 1 else self.player1
        try:

            def action_sort(action):
                if action == Shoot.You:
                    return 1
                elif action == Shoot.Opponent:
                    return 2
                else:
                    return 3

            move = player.handler.make_move(
                player.hp,
                opponent.hp,
                player.items,
                opponent.items,
                action,
                action_result,
                sorted(list(set(available)), key=action_sort),
            )
            if move not in available and (len(available) > 0 or not isinstance(move, Nothing)):
                raise ValueError('move is not in available')
        except Exception:
            raise
        return move

    def handle_round(self, move, who_moves, chamber):
        player = self.player1 if who_moves == 1 else self.player2
        opponent = self.player2 if who_moves == 1 else self.player1
        opponent_handcuffed = False
        handcuffs_cooldown = 0
        hand_saw_active = False
        adrenaline_active = False
        while True:
            if isinstance(move, Shoot):
                bullet = chamber.pop(0)
                swap = True
                if move == Shoot.You and bullet == Shell.Live:
                    player.hp -= 1
                    if hand_saw_active:
                        player.hp -= 1
                if move == Shoot.Opponent and bullet == Shell.Live:
                    opponent.hp -= 1
                    if hand_saw_active:
                        opponent.hp -= 1
                if move == Shoot.You and bullet == Shell.Blank:
                    swap = False
                if handcuffs_cooldown:
                    handcuffs_cooldown -= 1
                if opponent_handcuffed:
                    opponent_handcuffed = False
                    swap = False
                hand_saw_active = False 
                if swap:
                    available = [Shoot.You, Shoot.Opponent] + opponent.items
                    if not chamber or player.hp <= 0 or opponent.hp <= 0:
                        available = []
                    who_shot = Shoot.You if move == Shoot.Opponent else Shoot.Opponent
                    opponent_move = self.get_move(
                        who_moves % 2 + 1,
                        ActorAction(Shoot.Opponent, who_shot),
                        bullet,
                        available,
                    )
                    self.get_move(
                        who_moves,
                        ActorAction(Shoot.You, move),
                        bullet,
                        [],
                    )
                    move = opponent_move
                    who_moves = who_moves % 2 + 1
                    player, opponent = opponent, player
                else:
                    available = [Shoot.You, Shoot.Opponent] + player.items
                    if not chamber or player.hp <= 0 or opponent.hp <= 0:
                        available = []
                    who_shot = Shoot.You if move == Shoot.Opponent else Shoot.Opponent
                    move = self.get_move(
                        who_moves,
                        ActorAction(Shoot.You, move),
                        bullet,
                        available,
                    )
                    self.get_move(
                        who_moves % 2 + 1,
                        ActorAction(Shoot.Opponent, who_shot),
                        bullet,
                        [],
                    )
                if not chamber or player.hp <= 0 or opponent.hp <= 0:
                    return

            if move == Item.Beer:
                bullet = chamber.pop(0)
                if adrenaline_active:
                    opponent.items.remove(Item.Beer)
                    adrenaline_active = False
                else:    
                    player.items.remove(Item.Beer)
                available = [Shoot.You, Shoot.Opponent] + player.items
                if not chamber:
                    available = []
                move = self.get_move(
                    who_moves,
                    ActorAction(Shoot.You, Item.Beer),
                    bullet,
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    ActorAction(Shoot.Opponent, Item.Beer),
                    bullet,
                    [],
                )
                if not chamber:
                    return
            elif move == Item.Cigarettes:
                player.hp = player.hp + 1 if player.hp < self.max_hp else player.hp
                if adrenaline_active:
                    opponent.items.remove(Item.Cigarettes)
                    adrenaline_active = False
                else:    
                    player.items.remove(Item.Cigarettes)
                available = [Shoot.You, Shoot.Opponent] + player.items
                move = self.get_move(
                    who_moves,
                    ActorAction(Shoot.You, Item.Cigarettes),
                    ActorAction(Shoot.You, Item.Cigarettes),
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    ActorAction(Shoot.Opponent, Item.Cigarettes),
                    ActorAction(Shoot.Opponent, Item.Cigarettes),
                    [],
                )
            elif move == Item.Handcuffs:
                if adrenaline_active:
                    opponent.items.remove(Item.Handcuffs)
                    adrenaline_active = False
                else:    
                    player.items.remove(Item.Handcuffs)
                if handcuffs_cooldown == 0:
                    opponent_handcuffed = True
                    handcuffs_cooldown = 2
                available = [Shoot.You, Shoot.Opponent] + player.items
                move = self.get_move(
                    who_moves,
                    ActorAction(Shoot.You, Item.Handcuffs),
                    ActorAction(Shoot.You, Item.Handcuffs),
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    ActorAction(Shoot.Opponent, Item.Handcuffs),
                    ActorAction(Shoot.Opponent, Item.Handcuffs),
                    [],
                )
            elif move == Item.HandSaw:
                if adrenaline_active:
                    opponent.items.remove(Item.HandSaw)
                    adrenaline_active = False
                else:    
                    player.items.remove(Item.HandSaw)
                hand_saw_active = True
                available = [Shoot.You, Shoot.Opponent] + player.items
                move = self.get_move(
                    who_moves,
                    ActorAction(Shoot.You, Item.HandSaw),
                    ActorAction(Shoot.You, Item.HandSaw),
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    ActorAction(Shoot.Opponent, Item.HandSaw),
                    ActorAction(Shoot.Opponent, Item.HandSaw),
                    [],
                )
            elif move == Item.Magnifier:
                if adrenaline_active:
                    opponent.items.remove(Item.Magnifier)
                    adrenaline_active = False
                else:    
                    player.items.remove(Item.Magnifier)
                available = [Shoot.You, Shoot.Opponent] + player.items
                bullet = chamber[0]
                move = self.get_move(who_moves, ActorAction(Shoot.You, Item.Magnifier), bullet, available)
                self.get_move(
                    who_moves % 2 + 1,
                    ActorAction(Shoot.Opponent, Item.Magnifier),
                    Shell.Unknown,
                    [],
                )
            elif move == Item.Phone:
                if adrenaline_active:
                    opponent.items.remove(Item.Phone)
                    adrenaline_active = False
                else:    
                    player.items.remove(Item.Phone)
                available = [Shoot.You, Shoot.Opponent] + player.items
                bulletno = random.randint(0, len(chamber) - 1)
                result = PhoneCall(bulletno, chamber[bulletno])
                move = self.get_move(
                    who_moves,
                    ActorAction(Shoot.You, Item.Phone),
                    result,
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    ActorAction(Shoot.Opponent, Item.Phone),
                    Shell.Unknown,
                    [],
                )
            elif move == Item.Inverter:
                if adrenaline_active:
                    opponent.items.remove(Item.Inverter)
                    adrenaline_active = False
                else:    
                    player.items.remove(Item.Inverter)
                available = [Shoot.You, Shoot.Opponent] + player.items
                chamber[0] = Shell.Live if chamber[0] == Shell.Blank else Shell.Blank
                move = self.get_move(
                    who_moves,
                    ActorAction(Shoot.You, Item.Inverter),
                    ActorAction(Shoot.You, Item.Inverter),
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    ActorAction(Shoot.Opponent, Item.Inverter),
                    ActorAction(Shoot.Opponent, Item.Inverter),
                    [],
                )
            elif move == Item.Medicine:
                player.hp = player.hp + 2 if random.randint(1,2) == 2 else player.hp - 1
                player.hp = self.max_hp if player.hp > self.max_hp else self.max_hp
                if adrenaline_active:
                    opponent.items.remove(Item.Medicine)
                    adrenaline_active = False
                else:    
                    player.items.remove(Item.Medicine)
                available = [Shoot.You, Shoot.Opponent] + player.items
                move = self.get_move(
                    who_moves,
                    ActorAction(Shoot.You, Item.Medicine),
                    ActorAction(Shoot.You, Item.Medicine),
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    ActorAction(Shoot.Opponent, Item.Medicine),
                    ActorAction(Shoot.Opponent, Item.Medicine),
                    [],
                )
            elif move == Item.Adrenaline:
                player.items.remove(Item.Adrenaline)
                available = opponent.items.copy()
                adrenaline_active = True
                if Item.Adrenaline in available:
                    available = available.remove(Item.Adrenaline)
                if not available:
                    adrenaline_active = False
                move = self.get_move(
                who_moves,
                ActorAction(Shoot.You, Item.Adrenaline),
                ActorAction(Shoot.You, Item.Adrenaline),
                available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    ActorAction(Shoot.Opponent, Item.Adrenaline),
                    ActorAction(Shoot.Opponent, Item.Adrenaline),
                    [],
                )    

    def start(self):
        while self.player1.hp > 0 and self.player2.hp > 0:
            who_moves = 1 # random.randint(1, 2)
            live_bullets, blank_bullets, chamber = self.initialize_round()
            if who_moves == 1:
                move = self.get_move(
                    1,
                    RoundStart(),
                    InitialShellCount(live_bullets, blank_bullets),
                    [Shoot.You, Shoot.Opponent] + self.player1.items,
                )
                self.get_move(
                    2,
                    RoundStart(),
                    InitialShellCount(live_bullets, blank_bullets),
                    [],
                )
            else:
                self.get_move(
                    1,
                    RoundStart(),
                    InitialShellCount(live_bullets, blank_bullets),
                    [],
                )
                move = self.get_move(
                    2,
                    RoundStart(),
                    InitialShellCount(live_bullets, blank_bullets),
                    [Shoot.You, Shoot.Opponent] + self.player2.items,
                )
            self.handle_round(move, who_moves, chamber)
        if self.player1.hp <= 0:
            return 'PLAYER 2 WINS'
        return 'PLAYER 1 WINS'
