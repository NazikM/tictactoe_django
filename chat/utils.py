class TicTacToe:
    @staticmethod
    def next_step(chart, step, player):
        chart = list(chart)
        if isinstance(step, str):
            step = int(step)
        if TicTacToe.is_possible(chart, step):
            chart[step] = player
            res = TicTacToe.check_winner(chart, player)
            return "".join(chart), res
        return chart, False


    @staticmethod
    def is_possible(chart, step):
        return True if chart[step] == "." else False

    @staticmethod
    def check_winner(chart, player):
        player_comb = [player, player, player]
        if chart[:3] == player_comb or chart[3:6] == player_comb or chart[6:9] == player_comb:
            return True

        if chart[::3] == player_comb or chart[1::3] == player_comb or chart[2::3] == player_comb:
            return True

        if [chart[0], chart[4], chart[8]] == player_comb or [chart[2], chart[4], chart[6]] == player_comb:
            return True

        return False

    @staticmethod
    def chart_repr(chart):
        for i in range(0, 9, 3):
            print(chart[i:i+3])


def generate_name():
    from random import choice, randint
    adjective = choice(('clever', 'small', 'beautiful', 'happy', 'cool', 'sweet'))
    noun = choice(('shark', 'panda', 'elephant', 'monkey', 'fish', 'axolotl'))
    number = str(randint(1, 9))
    return adjective + noun + number



# TicTacToe.next_step('x..x.....', 6, "x")
# TicTacToe.next_step('x...x....', 8, "x")
# TicTacToe.next_step('..x.x....', 6, "x")
