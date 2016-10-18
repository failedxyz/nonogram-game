class TestGeneral:
    def test_sanity_check(self):
        return "sanity" > 0

    def test_index(self, client):
        assert client.get("/").data == "Hello, world."
