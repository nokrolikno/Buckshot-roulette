import random
from abc import ABC, abstractmethod


class PlayerAbstract(ABC):
    @abstractmethod
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
        """
        :param my_hp: int, your current HP.

        :param opponent_hp: int, opponent`s current HP.

        :param my_items: list[str], list of all your items.
        Example: ['BEER', 'BEER', 'CIGARETTES', 'HANDCUFFS', 'KNIFE', 'MAGNIFIER']

        :param opponent_items: list[str], list of all opponents items.
        Example: ['BEER', 'BEER', 'CIGARETTES', 'HANDCUFFS', 'KNIFE', 'MAGNIFIER']

        :param action: str, string containing action as input. It builds like this:
            '{1} {2}'
            1 - [YOU, OPPONENT, BASE] - who did the action or 'BASE' if it is general action
            2 - [YOU, OPPONENT, BEER, CIGARETTES, HANDCUFFS, KNIFE, MAGNIFIER, ROUND_START] - the action itself where
                YOU, OPPONENT - stands for shooting you or opponent
                BEER, CIGARETTES, HANDCUFFS, KNIFE, MAGNIFIER - using an item
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
        Example: ['YOU', 'OPPONENT', 'BEER', 'CIGARETTES', 'HANDCUFFS', 'KNIFE', 'MAGNIFIER']

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
    ITEMS = ['BEER', 'CIGARETTES', 'HANDCUFFS', 'KNIFE', 'MAGNIFIER']

    def __init__(
            self,
            player1: PlayerAbstract,
            player2: PlayerAbstract,
            hp=4,
            max_items=8,
            draw_items=4,
            min_bullets=3,
            max_bullets=8
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
        live_bullets = random.randint(1, total_bullets-1)
        blank_bullets = total_bullets - live_bullets
        chamber = ['LIVE' for i in range(live_bullets)] + ['BLANK' for j in range(blank_bullets)]
        random.shuffle(chamber)
        return live_bullets, blank_bullets, chamber

    def get_move(self, player_number: int, action: str, action_result: str, available: list[str]):
        player = self.player1 if player_number == 1 else self.player2
        opponent = self.player2 if player_number == 1 else self.player1
        try:
            move = player.handler.make_move(
                player.hp,
                opponent.hp,
                player.items,
                opponent.items,
                action,
                action_result,
                list(set(available)),
            )
            if move not in available and (len(available) > 0 or move != 'NOTHING'):
                raise ValueError('move is not in available')  # TODO: Поменять логику обработки
        except Exception as e:
            raise
        return move

    def handle_round(self, move, who_moves, chamber):
        player = self.player1 if who_moves == 1 else self.player2
        opponent = self.player2 if who_moves == 1 else self.player1
        opponent_handcuffed = False
        knife_active = False
        while True:
            if move in {'YOU', 'OPPONENT'}:
                bullet = chamber.pop(0)
                swap = True
                if move == 'YOU' and bullet == 'LIVE':
                    player.hp -= 1
                    if knife_active:
                        knife_active = False
                        player.hp -= 1
                if move == 'OPPONENT' and bullet == 'LIVE':
                    opponent.hp -= 1
                    if knife_active:
                        knife_active = False
                        opponent.hp -= 1
                if move == 'YOU' and bullet == 'BLANK':
                    swap = False
                if opponent_handcuffed:
                    opponent_handcuffed = False
                    swap = False
                if player.hp <= 0 or opponent.hp <= 0:
                    return
                if swap:
                    available = ['YOU', 'OPPONENT'] + opponent.items
                    if not chamber:
                        available = []
                    who_shot = 'YOU' if move == 'OPPONENT' else 'OPPONENT'
                    opponent_move = self.get_move(
                        who_moves % 2 + 1,
                        'OPPONENT ' + who_shot,
                        bullet,
                        available,
                    )
                    self.get_move(
                        who_moves,
                        'YOU ' + move,
                        bullet,
                        [],
                    )
                    move = opponent_move
                    who_moves = who_moves % 2 + 1
                    player, opponent = opponent, player
                else:
                    available = ['YOU', 'OPPONENT'] + player.items
                    if not chamber:
                        available = []
                    who_shot = 'YOU' if move == 'OPPONENT' else 'OPPONENT'
                    move = self.get_move(
                        who_moves,
                        'YOU ' + move,
                        bullet,
                        available,
                    )
                    self.get_move(
                        who_moves % 2 + 1,
                        'OPPONENT ' + who_shot,
                        bullet,
                        [],
                    )
                if not chamber:
                    return

            if move == 'BEER':
                bullet = chamber.pop(0)
                player.items.remove('BEER')
                available = ['YOU', 'OPPONENT'] + player.items
                if not chamber:
                    available = []
                move = self.get_move(
                    who_moves,
                    'YOU BEER',
                    bullet,
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    'OPPONENT BEER',
                    bullet,
                    [],
                )
                if not chamber:
                    return
            elif move == 'CIGARETTES':
                player.hp = player.hp + 1 if player.hp < self.max_hp else player.hp
                player.items.remove('CIGARETTES')
                available = ['YOU', 'OPPONENT'] + player.items
                move = self.get_move(
                    who_moves,
                    'YOU CIGARETTES',
                    '',
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    'OPPONENT CIGARETTES',
                    '',
                    [],
                )
            elif move == 'HANDCUFFS':
                player.items.remove('HANDCUFFS')
                opponent_handcuffed = True
                available = ['YOU', 'OPPONENT'] + player.items
                move = self.get_move(
                    who_moves,
                    'YOU HANDCUFFS',
                    '',
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    'OPPONENT HANDCUFFS',
                    '',
                    [],
                )
            elif move == 'KNIFE':
                player.items.remove('KNIFE')
                knife_active = True
                available = ['YOU', 'OPPONENT'] + player.items
                move = self.get_move(
                    who_moves,
                    'YOU KNIFE',
                    '',
                    available,
                )
                self.get_move(
                    who_moves % 2 + 1,
                    'OPPONENT KNIFE',
                    '',
                    [],
                )
            elif move == 'MAGNIFIER':
                player.items.remove('MAGNIFIER')
                available = ['YOU', 'OPPONENT'] + player.items
                bullet = chamber[0]
                move = self.get_move(
                    who_moves,
                    'YOU MAGNIFIER',
                    bullet,
                    available
                )
                self.get_move(
                    who_moves % 2 + 1,
                    'OPPONENT MAGNIFIER',
                    '',
                    [],
                )

    def start(self):
        while self.player1.hp > 0 and self.player2.hp > 0:
            who_moves = random.randint(1, 2)
            live_bullets, blank_bullets, chamber = self.initialize_round()
            if who_moves == 1:
                move = self.get_move(
                    1,
                    'BASE ROUND_START',
                    f'{live_bullets} LIVE {blank_bullets} BLANK',
                    ['YOU', 'OPPONENT'] + self.player1.items,
                )
                self.get_move(
                    2,
                    'BASE ROUND_START',
                    f'{live_bullets} LIVE {blank_bullets} BLANK',
                    [],
                )
            else:
                self.get_move(
                    1,
                    'BASE ROUND_START',
                    f'{live_bullets} LIVE {blank_bullets} BLANK',
                    [],
                )
                move = self.get_move(
                    2,
                    'BASE ROUND_START',
                    f'{live_bullets} LIVE {blank_bullets} BLANK',
                    ['YOU', 'OPPONENT'] + self.player2.items,
                )
            self.handle_round(move, who_moves, chamber)
        if self.player1.hp <= 0:
            return 'PLAYER 2 WINS'
        return 'PLAYER 1 WINS'
