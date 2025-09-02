

def check_category_for_duplicates(category, info:str):
    if "sketch" in category or "voice" in category:
        possible_inputs = [i + ":voice" for i in ["pointing", "address", "entry", "words", "symbol"]]
        possible_inputs += [i + ":sketch" for i in ["pointing", "address", "entry", "words", "symbol"]]
        possible_inputs += [i + ":sketch+voice" for i in ["pointing", "address", "entry", "words", "symbol"]]
        if "voice+sketch" in category or "?" in category:
            raise Exception("Nebenfehler")
    else:
        possible_inputs = ["pointing", "address", "entry", "words", "symbol"]
    for substring in possible_inputs:
        if category.lower().count(substring) > 1:
            # print([category, info, substring], flush=True)
            raise Exception("should not happen!")