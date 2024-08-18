import dataclasses
from sound_input.combo import Combo


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
    combo: None | Combo  # 0 none, 1-6 in combo

    def toJsonObj(self) -> dict:
        if self.combo == None:
            combo_num = 0
        else:
            combo_num = self.combo.value

        return {
            "walk_direction": self.walk_direction,
            "jump": self.jump,
            "combo": combo_num,
        }


def player_action_set_from_json_obj(obj: dict) -> PlayerActionSet:
    if obj["combo"] == 0:
        combo = None
    else:
        combo = Combo(obj["combo"])

    return PlayerActionSet(
        walk_direction=obj["walk_direction"], jump=obj["jump"], combo=combo
    )
