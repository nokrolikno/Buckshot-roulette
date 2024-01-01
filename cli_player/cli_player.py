from engine.engine import PlayerAbstract


class CLIPlayer(PlayerAbstract):
    def __init__(self, number):
        self.number = number

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
        print(f'Делаю ход от лица {self.number}')
        print(f'Мои хп: {my_hp}')
        print(f'Хп оппонента: {opponent_hp}')
        print(f'Мои вещи: {my_items}')
        print(f'Вещи оппонента: {opponent_items}')
        print(f'Действие: {action}')
        print(f'Результат действия: {action_result}')
        print(f'Доступные ходы: {available}')
        return input('Мой ход: ')
