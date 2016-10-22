class TestGeneral:
    def test_sanity_check(self):
        return "sanity" > 0

    def test_index(self, client):
        response = client.get("/index.html")
        assert response.status_code == 200
