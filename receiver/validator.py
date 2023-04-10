def is_valid(prev_state, cur_state) -> bool:
    event_val = prev_state['event_id'] == cur_state['event_id']
    home_val = prev_state['home_score'] <= cur_state['home_score']
    away_val = prev_state['away_score'] <= cur_state['away_score']
    time_val = prev_state['time'] < cur_state['time']
    return event_val and home_val and away_val and time_val
