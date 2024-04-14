from enum import Enum


def pick_language():
    language = None
    while language is None:
        print('Выберите язык')
        print('Select Language')
        print('----------')
        print('русский = 1')
        print('English = 2')
        match input():
            case '1':
                language = Language.Russian
            case '2':
                language = Language.English
    return language


class Language(Enum):
    Russian = 1
    English = 2

    def greeting(self):
        match self:
            case Language.Russian:
                return 'Введите имя игрока: '
            case Language.English:
                return 'Enter your name: '

    def acting_player(self):
        match self:
            case Language.Russian:
                return 'Делаю ход от лица '
            case Language.English:
                return 'Making a move on behalf of '

    def hp(self):
        match self:
            case Language.Russian:
                return 'Мои хп: '
            case Language.English:
                return 'HP: '

    def opponent_hp(self):
        match self:
            case Language.Russian:
                return 'Хп оппонента: '
            case Language.English:
                return "Opponent's HP: "

    def my_items(self):
        match self:
            case Language.Russian:
                return 'Мои вещи: '
            case Language.English:
                return 'My items: '

    def opponent_items(self):
        match self:
            case Language.Russian:
                return 'Вещи оппонента: '
            case Language.English:
                return "Opponent's items: "

    def action(self):
        match self:
            case Language.Russian:
                return 'Действие: '
            case Language.English:
                return 'Action: '

    def action_result(self):
        match self:
            case Language.Russian:
                return 'Результат действия: '
            case Language.English:
                return 'Action outcome: '

    def available_moves(self):
        match self:
            case Language.Russian:
                return 'Доступные ходы: '
            case Language.English:
                return 'Available moves: '

    def my_move(self):
        match self:
            case Language.Russian:
                return 'Мой ход: '
            case Language.English:
                return 'My move: '
