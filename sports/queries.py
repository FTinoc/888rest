from sports.db import get_db

new_sport = "INSERT INTO sports (name, slug) VALUES (?, ?)"
check_db_query = "SELECT column FROM table"


def slugify(name):
    slug = name.replace(" ", "-")
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
    
    return(check)

def add_sport(name):
    db = get_db()
    slug = slugify(name)
    db.execute(new_sport, (name, slug))
    db.commit()
    
 