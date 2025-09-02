from typing import Union

from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.check_category_for_duplicates import check_category_for_duplicates


class Coding(object):
    def __init__(self, codes_raw: dict) -> None:
        self.d = codes_raw
        self.coding_existing = not self.test_array_empty(codes_raw)
        self.codes = self.get_nonempty_entries(codes_raw)

    def test_array_empty(self, d : Union[dict , str, None]= "Start") -> dict:
        """
        :param d: zum Start = (verschachteltes) Dict!
         """
        if d == "Start":
            d = self.d
        if d is None:
            return True
        if isinstance(d, str) and len(d) > 0:
            return False
        if isinstance(d, dict):
            return all(self.test_array_empty(v) for v in d.values())
        return True


    def get_nonempty_entries(self, d : Union[dict , str, None]= "Start") -> dict:
        if self.test_array_empty():
            return {}
        if d == "Start":
            d = self.d
        if not isinstance(d, dict) or d is None:
            return {}
        filtered = {}
        for k, v in d.items():
            if isinstance(v, dict):
                nested = self.get_nonempty_entries(v)
                if nested:  # nur hinzufügen, wenn verschachteltes Dict nicht leer
                    filtered[k] = nested
            elif isinstance(v, str):
                if v.strip():  # nur nicht-leere Strings (auch ohne nur Leerzeichen)
                    filtered[k] = v
            elif v is not None:
                filtered[k] = v
        return filtered

    def flatten_dict(self, d: dict, parent_key: str = '') -> list[str]:
        """
        HILFSFUNKTION
        :param d:
        :param parent_key:
        :return:
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}:{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key))
            else:
                items.append(f"{new_key}:{v}")
        return items

    def get_category(self):
        if not self.coding_existing:
            return None
        if "SKIPPED" in self.codes.keys():
            return "SKIPPED"
        if "GUI" in self.codes.keys():
            return "GUI"

        parts = self.flatten_dict(self.codes)
        if len(parts) == 0:
            # TODO: prüfen, ob Task*_skipped.json vorhanden ist? Ansonsten noch nicht gecodet??
            return "SKIPPED"

        # ignore CONNECTED ANNOTATION:
        parts = [i for i in parts if "CONNECTED-ANNOTATION" not in i]

        # KNOWLEDGE:
        # for mod in ["sketch", "voice"]:
        #     parts = [s.replace(f"OPERATION:KNOWLEDGE:{mod}", "knowledge").replace(f"LOCATION:KNOWLEDGE:{mod}", "knowledge")
        #              for s in parts]

        parts = [i.replace("POSITION", "POINTING") for i in parts]#TODO aktuell?
        parts = [i.replace("SELECTION", "POINTING") for i in parts]

        category = " - ".join(set(parts))
        try:
            check_category_for_duplicates(category, info = "Coding-Objekt")
        except:
            #Werte gleichen Codes, aber versch. Modalities kombinieren, z.B.
            # LOCATION:ADDRESS: voice - LOCATION:POINTING: sketch - voice - LOCATION:POINTING: sketch - OPERATION:SYMBOL: sketch - OPERATION:WORDS: voice
            value = None
            for i in range(len(parts)):
                if "sketch" in parts[i] and "voice" in parts[i]:
                    value = parts[i].replace("sketch+voice", "").replace("voice+sketch", "")
            new_parts = [value+"sketch+voice"] if value is not None else []
            new_parts += [i for i in parts if value is not None and value not in i]
            category = " - ".join(set(new_parts))
        check_category_for_duplicates(category, info="Coding-Objekt")
        return category


#TODO get coding bei mehreren Vorschlägen: codes1, codes2, ...

if __name__ == "__main__":
    d = {
      "A": {
        "x": "1",
        "y": "2"
      },
      "B": "3"
    }
    d = Coding(d)
    # print([d.get_category()])