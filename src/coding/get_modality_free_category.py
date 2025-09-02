from src.coding.CODING_CATEGORIES import CODING_CATEGORIES

#
# def get_modality_free_category(category:str, limit_to:CODING_CATEGORIES):
#     category = category.lower().strip()
#
#     if limit_to == CODING_CATEGORIES.SKETCHVOICE:
#         sketch = "sketch" in category
#         voice = "voice" in category
#     # remove sketch/voice/combinations theirof:
#     category = category.replace(":sketch", "").replace(":voice", "")
#     c = category.split("-")
#     if limit_to == CODING_CATEGORIES.OPERATION:
#         if "gui" in c or "skipped" in c:
#             return None
#         c = [i.strip() for i in c if limit_to.value.lower() in i.lower()]
#     elif limit_to == CODING_CATEGORIES.LOCATION:
#         if "gui" in c or "skipped" in c:
#             return None
#         c = [i.strip() for i in c if limit_to.value.lower() in i.lower()]
#     elif limit_to == CODING_CATEGORIES.ALL:
#         pass
#     elif limit_to == CODING_CATEGORIES.SKETCHVOICE:
#         c = [i.strip() for i in c]
#         if voice:
#             c.append("voice")
#         if sketch:
#             c.append("sketch")
#     else:
#         raise Exception("unknown handling")
#     c = [i.strip() for i in c]
#
#     result = " - ".join(list(set(c)))
#     if len(result) == 0 or len(result.replace(" ","")) == 0:
#         raise Exception(f"get_modality_free_category: empty category {category}")
#     return result


def get_modality_free_category(category: str, limit_to: CODING_CATEGORIES):
    category = category.lower().strip()

    if (not limit_to == CODING_CATEGORIES.FULLMOD and not limit_to == CODING_CATEGORIES.LOCATIONMOD
            and not limit_to == CODING_CATEGORIES.OPERATIONMOD and not limit_to == CODING_CATEGORIES.EMPTYMOD):
        # remove sketch/voice/combinations their-of:
        category = category.replace(":sketch+voice","").replace(":sketch", "").replace(":voice", "")
    c = category.split("-")
    if limit_to == CODING_CATEGORIES.FULLMOD:
        soll_order = "sketch+voice"
        for cat_index in range(len(c)):
            cat = c[cat_index]
            cat = cat.replace("?","").replace(" ","")
            cat = cat.replace("voice+sketch", soll_order)
            c[cat_index] = cat
    if "gui" in c or "skipped" in c:
        return None

    if limit_to == CODING_CATEGORIES.OPERATIONMODLESS or limit_to == CODING_CATEGORIES.OPERATIONMOD:
        c = [i.strip() for i in c if "operation" in i.lower()]
    elif limit_to == CODING_CATEGORIES.LOCATIONMODLESS or limit_to == CODING_CATEGORIES.LOCATIONMOD:
        c = [i.strip() for i in c if "location" in i.lower()]
    elif limit_to == CODING_CATEGORIES.FULLMODLESS:
        c = [i.strip() for i in c]
    elif limit_to == CODING_CATEGORIES.FULLMOD:
        c = [i.strip() for i in c]
    elif limit_to == CODING_CATEGORIES.EMPTYMOD:
        replacements = ["operation", "location", ":", "symbol", "words", "position", "selection", "pointing", "address", "entry"]
        for r in replacements:
            c = [i.replace(r,"") for i in c]
        c = [i.strip() for i in c]
        c = sorted(c, key=lambda i: i.lower())
        if "sketch" in c and not "voice" in c:
            result = "sketch"
        elif "voice" in c and not "sketch" in c:
            result = "voice"
        else:
            result = "sketch - voice"
        return result
    else:
        raise Exception("unknown handling")
    c = [i.replace(" ", "") for i in c]
    c = list(set(c))
    c = sorted(c, key=lambda i: i.lower())
    result = " - ".join(c)
    if len(result) == 0 or len(result.replace(" ", "")) == 0:
        raise Exception(f"get_modality_free_category: empty category {category}")
    return result


if __name__ == "__main__":
    category = "operation:words - location:selection - location:selection"
    # category = "gui"

    print(get_modality_free_category(category, limit_to=CODING_CATEGORIES.LOCATION_MODLESS))