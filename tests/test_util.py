import util


class TestUtil:
    def test_generate_string(self):
        length = 5
        alphabet = "quickbrownfox"
        generated = util.generate_string(length=length, alpha=alphabet)
        assert len(generated) == length
        assert all([c in alphabet for c in generated])
