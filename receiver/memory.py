from message import JsonMessage


class Memo():
    def __init__(self) -> None:
        self.raw = None
        self.scores = 2 * [(0, 0)]

    def update_match_score(self):
        data = self.to_dict()
        self.scores[data['game_period']] = (
            data['home_score'],
            data['away_score'],
        )

    def get_real_score(self, i):
        if i == 0:
            return self.scores[i]
        else:
            return [self.scores[i][0] - self.scores[i - 1][0],
                    self.scores[i][1] - self.scores[i - 1][1]]

    def update(self, data):
        self.raw = JsonMessage(data)
        self.update_match_score()

    def is_ready(self):
        return bool(self.raw)

    def to_dict(self):
        return self.raw.to_dict()
