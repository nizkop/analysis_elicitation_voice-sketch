


def translation(s: str) -> str:
    s = s.strip().lower().replace("\n", " ")

    translations = {
        "sehr einfach": "very easy",
        "einfach": "easy",
        "neutral": "neutral",
        "schwer": "difficult",
        "sehr schwer": "very difficult",
        "keine": "none",
        "ein wenig": "a little",
        "viel": "a lot",
        "männlich": "male",
        "weiblich": "female",
        "nicht-binär": "non-binary",
        "links": "left",
        "rechts": "right",
        # mother language inputs:
        "deutsch": "german",
        "hungarian": "hungarian",
        "ukrainian": "ukrainian",
        "griechisch": "greek",
        "is": "icelandic",
        "russisch": "russian",
        "de": "german",
        "english": "english",
        "island": "icelandic",
        "/ice": "icelandic",
        "ice": "icelandic",
        "íslenska": "icelandic",
        "tegulu": "tegulu",#south indian
        "hindi": "hindi",
        "persian": "persian",# west iranian
    }

    # Wenn der Begriff bereits auf Englisch ist, gib ihn zurück
    if s in translations.values():
        return s
    try:
        return translations[s]
    except KeyError:
        return s
