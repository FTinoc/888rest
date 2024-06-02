from sports.db import get_db

new_sport = "INSERT INTO sports (name, slug) VALUES (?, ?)"
sports = "SELECT name, id FROM sports"
sport_delete = "DELETE FROM sports WHERE id = ?"

new_event = ("INSERT INTO events (name, slug, active, kind, sport_id, status, scheduled_start, actual_start) "
             "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
             )
events = "SELECT * FROM events WHERE sport_id = ?"

check_db_query = "SELECT column FROM table"

find_id = "SELECT id FROM table WHERE column = ?"


def slugify(name, table):
    slug = name.replace(" ", "-")
    initial_slug = slug
    i = 0
    busy_slug = check_db("slug", table, slug)
    while (busy_slug):
        slug = initial_slug + str(i)
        i += 1
        busy_slug = check_db("slug", table, slug)
    return slug


def check_db(column, table, data):
    query = check_db_query.replace("column", column)
    query = query.replace("table", table)
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    check = False
    for row in results:
        if data == row[column]:
            check = True
            continue

    return (check)


def add_sport(name):
    db = get_db()
    slug = slugify(name, "sports")
    
    try:
        response = {"status":"success"}
        db.execute(new_sport, (name, slug))
        db.commit()
    
    except Exception as e:
        response["status"] = str(Exception(e))
    
    return response

def get_id(column, table, data):
    db = get_db()
    query = find_id.replace("column", column)
    query = query.replace("table", table)
    cursor = db.cursor()
    cursor.execute(query, (data, ))
    results = cursor.fetchone()
    return results["id"]


def all_sports():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(sports)
    results = cursor.fetchall()
    sports_list = {}
    for row in results:
        sports_list[row["id"]] = row["name"]
    return sports_list


def delete_sport(name):
    db = get_db()
    sport = get_id("name", "sports", name)
    db.execute(sport_delete, (sport, ))
    db.commit()


def add_event(name, kind, sport, scheduled_start, status, actual_start="NULL", active=False):
    
    if active and actual_start == "NULL":
        response = {"error": "active event needs start"}
    
    else:
        db = get_db()
        
        if type(sport) is not int:
            sport = get_id("name", "sports", sport)
        slug = slugify(name, "events")
        
        try:
            response = {"status": "success"}
            db.execute(new_event, (name, slug, active, kind, sport,
                       status, scheduled_start, actual_start))
            db.commit()
        
        except Exception as e:
            response["status"] = str(Exception(e))
        
    return response


def all_events(sport):
    db = get_db()
    query = events
    cursor = db.cursor()
    result = cursor.execute(query, (sport, ))
    all_events_list = {}
    for row in result:
        all_events_list[row["id"]] = dict(
            name=row["name"], active=row["active"], scheduled_start=row["scheduled_start"],
            kind=row["kind"])
    return all_events_list
