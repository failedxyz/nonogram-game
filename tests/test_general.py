class TestGeneral:
    def test_sanity_check(self):
        return "sanity" > 0

    def test_index(self, client):
        response = client.get("/index.html")
        assert response.status_code == 200

    def test_process_data(self, socket):
        socket.emit("data", "001")
        received = socket.get_received()
        assert received
        data = received[0]
        assert data["name"] == "data"
        assert data["args"][0].find("001") == 0
