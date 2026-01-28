DEFAULT_TO = ["ltsertwlyudao@gmail.com"]
DEFAULT_CC = ["ltsertwlyudao@gmail.com"]

OBSERVATION_EMAILS = {
    "海域水質": {"to": ["huckyuan@gmail.com"], "cc": ["likefh@gmail.com"]},
    "陸域植物": {
        "to": ["galanhsnu@gmail.com"],
        "cc": ["bochung@gate.sinica.edu.tw", "kunchang.li@gmail.com"],
    },
    "底棲動物": {
        "to": ["apogonids@gmail.com"],
        "cc": ["chiuywlab@gmail.com", "kunchang.li@gmail.com"],
    },
    "聲音指數": {
        "to": ["janiceli0918@gmail.com"],
        "cc": ["mntuanmu@gate.sinica.edu.tw", "kunchang.li@gmail.com"],
    },
    "生物辨識": {
        "to": ["janiceli0918@gmail.com"],
        "cc": ["mntuanmu@gate.sinica.edu.tw", "kunchang.li@gmail.com"],
    },
    "棲地評估": {
        "to": ["apogonids@gmail.com"],
        "cc": ["chiuywlab@gmail.com", "kunchang.li@gmail.com"],
    },
    "溪流水質": {
        "to": ["apogonids@gmail.com"],
        "cc": ["chiuywlab@gmail.com", "kunchang.li@gmail.com"],
    },
    "溪流生物": {
        "to": ["apogonids@gmail.com"],
        "cc": ["chiuywlab@gmail.com", "kunchang.li@gmail.com"],
    },
    "海氣象浮標": {"to": ["kunchang.li@gmail.com"], "cc": ["acropora.chen@gmail.com"]},
    "珊瑚礁魚類多樣性與群聚": {
        "to": ["joshcy@gmail.com"],
        "cc": ["colinwen@gmail.com", "kunchang.li@gmail.com"],
    },
    "珊瑚礁底棲群聚": {
        "to": ["lecy.yhuang@gmail.com"],
        "cc": ["acropora.chen@gmail.com", "kunchang.li@gmail.com"],
    },
    "珊瑚入添": {
        "to": ["lecy.yhuang@gmail.com"],
        "cc": ["acropora.chen@gmail.com", "kunchang.li@gmail.com"],
    },
    "休閒漁業": {
        "to": ["joshcy@gmail.com"],
        "cc": ["colinwen@gmail.com", "kunchang.li@gmail.com"],
    },
    "氣象資料": {"to": ["kunchang.li@gmail.com"], "cc": ["acropora.chen@gmail.com"]},
    "海溫": {"to": ["kunchang.li@gmail.com"], "cc": ["acropora.chen@gmail.com"]},
    "珊瑚礁水下聲景": {
        "to": ["schonkopf@gmail.com"],
        "cc": ["kunchang.li@gmail.com"],
    },
    "鳥音辨識": {
        "to": ["janiceli0918@gmail.com"],
        "cc": ["mntuanmu@gate.sinica.edu.tw", "kunchang.li@gmail.com"],
    },
}


def get_email_targets(observation_item):
    """
    回傳 (to_list, cc_list, bcc_list)
    - observation_item 若找不到，回退到 DEFAULT_*
    - 支援 OBSERVATION_EMAILS 裡面只填 to/cc/bcc 任一項
    """
    cfg = OBSERVATION_EMAILS.get(observation_item or "", {})
    to = cfg.get("to") or DEFAULT_TO
    cc = cfg.get("cc") or DEFAULT_CC

    if isinstance(to, str):
        to = [to]
    if isinstance(cc, str):
        cc = [cc]

    return to, cc
