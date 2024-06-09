from sports.db import get_db

def test_events_endpoint(client, app):
    with app.app_context():
        #BAD LINK
        response = client.get("/tennis", json={})
        assert response.status_code == 404
        
        #POST
        response = client.post("/football", json={"name":"corinthians x sao paulo", "kind":"preplay", 
                               "scheduled_start":"2025-05-29 14:16:00", "status":"pending", "active":False})
        assert response.status_code == 200
        assert get_db().execute("SELECT * FROM events WHERE name = 'corinthians x sao paulo'").fetchone() is not None
        
        response = client.post("/football", json={"name":"corinthians x sao technical", "kind":"preplay", 
                               "scheduled_notstart":"2025-05-29 14:16:00", "status":"pending", "active":False})
        assert response.status_code == 400
        
        #GET
        response = client.get("/football", json={"1":{"table":"events", "column":"name", "operator":"equ", "value":"corinthians x sao paulo", "next":"END"}})
        assert response.status_code == 200
        
        response = client.get("/football", json={})
        assert response.status_code == 200
        
        response = client.get("/football")
        assert response.status_code == 400
        
        #PATCH
        response = client.patch("/football", json={"id":1, "columns":["name"], "values":["corinthians x arsenal"]})
        assert response.status_code == 200
        assert get_db().execute("SELECT * FROM events WHERE name = 'corinthians x arsenal'").fetchone() is not None
        
        response = client.patch("/football", json={"notid":1, "columns":["name"], "values":["corinthians x arsenal"]})
        assert response.status_code == 400