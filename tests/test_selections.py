from sports.db import get_db

def test_events_endpoint(client, app):
    with app.app_context():
        #BAD LINK
        response = client.get("/golf/Tw-not-world-tour", json={})
        assert response.status_code == 404
        
        #POST
        response = client.post("/golf/TW-world-tour", json={"name":"par", "active":False, "outcome":"unsettled", "price":12.98})
        assert response.status_code == 200
        assert get_db().execute("SELECT * FROM selections WHERE name = 'par'").fetchone() is not None
        
        response = client.post("/golf/TW-world-tour", json={"notname":"par", "active":False, "outcome":"unsettled", "price":12.98})
        assert response.status_code == 400
        
        #GET
        response = client.get("/golf/TW-world-tour", json={"1":{"table":"selections", "column":"name", "operator":"equ", "value":"hole 1 - birdie", "next":"END"}})
        assert response.status_code == 200
        
        response = client.get("/golf/TW-world-tour", json={})
        assert response.status_code == 200
        
        response = client.get("/golf/TW-world-tour")
        assert response.status_code == 400
        
        #PATCH
        response = client.patch("/golf/TW-world-tour", json={"id":1, "columns":["name"], "values":["hole 1: not birdie"]})
        assert response.status_code == 200
        assert get_db().execute("SELECT * FROM selections WHERE name = 'hole 1: not birdie'").fetchone() is not None
        
        response = client.patch("/golf/TW-world-tour", json={"data":1, "columns":["name"], "values":["corinthians x arsenal"]})
        assert response.status_code == 400