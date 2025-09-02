import unittest

from src.coding.CODING_CATEGORIES import CODING_CATEGORIES
from src.coding.Coding import Coding
from src.coding.get_modality_free_category import get_modality_free_category


class TestCoding(unittest.TestCase):
    d1 = {}
    d2 = {"bl": None}
    d3 = {"a": {"b": ""}}
    d4 = {"b1": "a"}
    d4a = {"b1": "a", "c": None}
    d5 = {"a": {"b": "c"}}
    d6 = {"A": {"x": "1", "y": "2"}, "B": "3"}

    def test_empty_dict(self):
        d = {}
        d = Coding(self.d1)
        assert d.test_array_empty() is True

        d = Coding(self.d2)
        assert d.test_array_empty() is True

        d = Coding(self.d3)
        assert d.test_array_empty() is True

        d = Coding(self.d4)
        assert d.test_array_empty() is False

        d = Coding(self.d5)
        assert d.test_array_empty() is False

        d = Coding(self.d6)
        assert d.test_array_empty() is False

    def test_get_nonempty_entries(self):
        d = Coding(self.d1)
        assert d.get_nonempty_entries() == {}

        d = Coding(self.d2)
        assert d.get_nonempty_entries() == {}

        d = Coding(self.d4)
        assert d.get_nonempty_entries() == self.d4

        d = Coding(self.d4a)
        assert d.get_nonempty_entries() == self.d4 #removed key c with value None

        d = Coding(self.d5)
        assert d.get_nonempty_entries() == self.d5

        d = Coding(self.d6)
        assert d.get_nonempty_entries() == self.d6


    def test_get_category(self):
        d = Coding(self.d1)
        assert d.get_category() is None
        d = Coding(self.d3)
        assert d.get_category() is None

        d = Coding(self.d4)
        assert d.get_category().strip() == "b1:a".strip()

        d = Coding(self.d4a)
        assert d.get_category().strip() == "b1:a".strip()

        d = Coding(self.d6)
        assert d.get_category().strip() == 'A:x:1 - B:3 - A:y:2'.strip()


    def test_get_modality_free_category(self):
        # Fall 1:
        for cat in CODING_CATEGORIES:
            coding = "gui"
            sub_category = get_modality_free_category(coding, limit_to=cat)
            assert sub_category is None

        # Fall 2:
        coding = "location:entry:voice - location:pointing:sketch - operation:words:sketch"

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.FULLMODLESS)
        assert sub_category.strip() == "location:entry - location:pointing - operation:words".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.FULLMOD)
        assert sub_category.strip() == coding.strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.OPERATIONMODLESS)
        assert sub_category.strip() == "operation:words".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.LOCATIONMODLESS)
        assert sub_category.strip() == "location:entry - location:pointing".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.LOCATIONMOD)
        assert sub_category.strip() == "location:entry:voice - location:pointing:sketch".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.OPERATIONMOD)
        assert sub_category.strip() == "operation:words:sketch".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.EMPTYMOD)
        assert sub_category.strip() == "sketch - voice".strip()

        # Fall 3:
        coding = "location:address:sketch - operation:symbol:sketch - operation:words:voice"

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.FULLMODLESS)
        assert sub_category.strip() ==  "location:address - operation:symbol - operation:words".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.FULLMOD)
        assert sub_category.strip() == coding.strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.OPERATIONMODLESS)
        assert sub_category.strip() == "operation:symbol - operation:words".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.LOCATIONMODLESS)
        assert sub_category.strip() == "location:address".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.LOCATIONMOD)
        assert sub_category.strip() =="location:address:sketch".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.OPERATIONMOD)
        assert sub_category.strip() == "operation:symbol:sketch - operation:words:voice".strip()

        sub_category = get_modality_free_category(coding, limit_to=CODING_CATEGORIES.EMPTYMOD)
        assert sub_category.strip() == "sketch - voice".strip()


if __name__ == "__main__":
    unittest.main()