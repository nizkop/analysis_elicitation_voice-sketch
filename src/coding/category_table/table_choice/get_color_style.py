from src.color_codes import global_colors
from src.plt_settings import footnotesize


def get_color_style(label:str):
    """

    :param label:
    :return: marker, color, title
    """
    label = label.replace("?", "").replace(" (point in cell)", "")

    if "-" in label:
        label = label.split(" - ")
        label = sorted(label)
        label = " - ".join(label)
        # text = label.replace("location:","").replace("operation:","").replace(" ","")
        # text = text.upper()
    # else:
    #     text = label.rsplit(':', 1)[-1].upper()

    marker = {
        "location:entry": ("*", get_footnote_size("LOCATION")+":"+get_footnote_size("ENTRY")),
        "location:address": ("x", get_footnote_size("LOCATION")+":"+get_footnote_size("ADDRESS")),
        "location:pointing": ("o", get_footnote_size("LOCATION")+":"+get_footnote_size("POINTING")),
        "location:address - location:entry": ("v",
                                              get_footnote_size("LOCATION")+":"+get_footnote_size("ADDRESS")+" - "
                                              +get_footnote_size("LOCATION")+":"+get_footnote_size("ENTRY")),
        "location:entry - location:pointing": ("d",
                                               get_footnote_size("LOCATION")+":"+get_footnote_size("ENTRY")+" - "
                                               +get_footnote_size("LOCATION")+":"+get_footnote_size("POINTING")),
        "location:address - location:pointing": ("3",
                                                 get_footnote_size("LOCATION")+":"+get_footnote_size("ADDRESS")+" - "
                                                 +get_footnote_size("LOCATION")+":"+get_footnote_size("POINTING")),
        "location:address - location:entry - location:pointing": ("H",
                                                                  get_footnote_size("LOCATION")+":"+get_footnote_size("ADDRESS")+" - "
                                                                  +get_footnote_size("LOCATION")+":"+get_footnote_size("ENTRY")+" - "
                                                                  +get_footnote_size("LOCATION")+":"+get_footnote_size("POINTING")),
        #
        "operation:words": ("*", get_footnote_size("OPERATION")+":"+get_footnote_size("WORDS")),
        "operation:symbol": ("x", get_footnote_size("OPERATION")+":"+get_footnote_size("SYMBOL")),
        "operation:symbol - operation:words": ("v",
                                               get_footnote_size("OPERATION")+":"+get_footnote_size("SYMBOL")+" - "
                                               +get_footnote_size("OPERATION")+":"+get_footnote_size("WORDS")),
    }
    color = global_colors[label]
    try:
        return marker[label][0], color, marker[label][1]
    except KeyError:
        raise Exception(f"Unknown color style: {label}")
    raise Exception(f"Unknown color style: {label}")


def get_footnote_size(text):
    return  r"{\fontsize{"+str(footnotesize)+r"}{\baselineskip}"+ text + r"}"


