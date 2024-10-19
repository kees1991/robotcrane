import json


class Dimensions(object):

    def __init__(self, l_1, l_2, l_3, d_4, l_5, l_7):
        self.l_1 = l_1  # base column length
        self.l_2 = l_2  # upper arm length
        self.l_3 = l_3  # lower arm length
        self.d_4 = d_4  # wrist extension length
        self.l_5 = l_5  # gripper length
        self.l_7 = l_7  # maximum jaw extension length

    def to_json(self) -> json:
        return json.dumps(self.__dict__)
