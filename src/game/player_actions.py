import dataclasses


# NOTE: To turn action set to json, run `json.dumps(dataclasses.asdict(action_set))`
@dataclasses.dataclass
class PlayerActionSet:
    """
    Actions are sent from the client to client handler.
    The action set represents the combination of all possible actions.
    """

    # long actions
    walk_direction: int  # -1, 0, or 1

    # instantaneous actions (absorbed when processed)
    jump: bool  # just because player wants to jump doesn't mean its possible
    attack: int  # 0 none, 1 fast attack, 2 strong attack
