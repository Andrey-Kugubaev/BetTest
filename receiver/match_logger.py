from enum import Enum


class STATUS(Enum):
    start_game = 0
    game_play = 1
    game_end = 2
    failed = 3


class MatchLogger():

    def __init__(self, memo, num_periods=2):
        self.memo = None
        self.update_memo(memo)

        self.DEFAULT_SCORE = (0, 0)
        self.NUM_PERIODS = num_periods

    def update_memo(self, memo):
        self.memo = memo

    def update_match_state(self):
        self.status_enum = STATUS.__members__[self.memo.to_dict()['status']]
        self.match_state = {
            'status': self.status_enum.value,
            'match_status': self.fmt_match_status(),
            'match_time': self.memo.to_dict()['match_time']
        }
        return self.match_state

    def fmt_match_status(self):
        if self.status_enum.value > 1:
            match_status = 3
        else:
            match_status = self.memo.to_dict(
            )['game_period']+self.status_enum.value
        return match_status

    def fmt_match_score(self, a, b):
        return {'home_score': a, 'away_score': b}

    def fmt_period_scores(self):
        res = []
        cp = self.memo.to_dict()['game_period']
        for i in range(0, self.NUM_PERIODS):
            res_ = {
                "number": i+1,
                **self.fmt_match_score(
                    *self.memo.get_real_score(i) if i <= cp
                    else self.DEFAULT_SCORE
                )
            }
            res.append(res_)
        return res

    def update_match_score(self):
        self.match_score = {
            'score': self.fmt_match_score(
                self.memo.to_dict()['home_score'],
                self.memo.to_dict()['away_score']
            ),
            'period_scores': self.fmt_period_scores()
        }
        return self.match_score

    def clog(self, data):
        print(data)

    def save_result(self):
        match = [self.update_match_state(), self.update_match_score()]
        self.clog(match)
