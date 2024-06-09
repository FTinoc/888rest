from sports.db import get_db

def test_sport_endpoint(client, app):
    with app.app_context():
        #POST
        response = client.post("/", json={"name":"soccer"})
        assert response.status_code == 200
        assert get_db().execute("SELECT * FROM sports WHERE name = 'soccer'").fetchone() is not None
        
        response = client.post("/", json={"name":""})
        assert response.status_code == 400
        
        response = client.post("/", json={"dog":"soccer"})
        assert response.status_code == 400
        
        response = client.post("/")
        assert response.status_code == 400
        
        #GET
        response = client.get("/", json={"1":{"table":"sports", "column":"name", "operator":"equ", "value":"soccer", "next":"END"}})
        assert response.status_code == 200
        
        response = client.get("/", json={})
        assert response.status_code == 200
        
        #PATCH
        response = client.patch("/", json={"id":3, "columns":["name"], "values":["notsoccer"]})
        assert response.status_code == 200
        assert get_db().execute("SELECT * FROM sports WHERE name = 'notsoccer'").fetchone() is not None
        
        response = client.patch("/", json={"notid":3, "columns":["name"], "values":["notsoccer"]})
        assert response.status_code == 400
        