import unittest

from badwordschecker.utils.text_normalization import normalize_text, tokenize_text


class TestTextNormalization(unittest.TestCase):
    def test_normalize_text(self):
        self.assertEqual(normalize_text("Caffè, perché!"), "caffe perche")
        self.assertEqual(normalize_text("L'apostrofo"), "lapostrofo")
        self.assertEqual(normalize_text("123 parole"), "123 parole")

    def test_tokenize_text(self):
        self.assertEqual(tokenize_text("caffe perche"), ["caffe", "perche"])
        self.assertEqual(tokenize_text("una frase di prova"), ["una", "frase", "di", "prova"])


if __name__ == "__main__":
    unittest.main()
