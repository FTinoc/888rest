from sports.db import get_db
from . import util

new_sport = "INSERT INTO sports (name, slug) VALUES (?, ?)"
new_event = ("INSERT INTO events (name, slug, active, kind, sport_id, status, scheduled_start, actual_start) "
             "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
             )

sports = "SELECT * FROM sports"
events = "SELECT * FROM events WHERE sport_id = ?"
selections = "SELECT * FROM selections WHERE event_id = ?"

check_db_query = "SELECT column FROM table"
find_id = "SELECT id FROM table WHERE column = ?"
lookup =    ("SELECT table.*, "
             "table_metrics.* "
             "FROM sports spt " 
            "LEFT JOIN events evt ON evt.sport_id = spt.id "
            "LEFT JOIN sports_metrics spt_metrics ON spt_metrics.id = spt.id "
            "WHERE "
            )

table_lookup = "PRAGMA table_info(table_lookup)"

patch = "UPDATE table SET columns_values WHERE id = ?"

get_ids = "SELECT id FROM table"

operators = {"equ":"=", "not":"<>",
             "gtr":">", "gqu":">=",
             "lss":"<","lqu":"<="}

def all(kind, param = ""):
    db = get_db()
    cursor = db.cursor()
    if kind == "sports":        
        result = cursor.execute(sports)
        
    elif kind == "events":
        result = cursor.execute(events, (param, ))
    
    elif kind == "selections":
        result = cursor.execute(selections, (param, ))
        
    data = []
    for row in result:
        data_row = {}
        for key in row.keys():
            data_row[key] = row[key]
            
        data.append(data_row)
        
    return data
    
def add_sport(name):
    db = get_db()
    slug = slugify(name, "sports")
    
    db.execute(new_sport, (name, slug))
    db.commit()
    response = {"status":"sucess"}
    
    return response

def add_event(name, kind, sport, scheduled_start, status, active):
    db = get_db()
    if type(sport) is not int:
        sport = get_id("slug", "sports", sport)
    
    slug = slugify(name, "events")
    db.execute(new_event, (name, slug, active, kind, sport,
               status, scheduled_start))
    db.commit()
    response = {"status":"success"}
        
    return response
    
def read(lookup_data, select_table):
    query = lookup
    valid_tables = {"sports":"spt", "events":"evt", "selections":"slt"}
    valid_columns = {"spt":get_columns("sports"),
                     "evt":get_columns("events"),
                     "slt":get_columns("selections")
                     }
    values = []
    for entry in lookup_data.keys():
        valid = util.validate_dict(lookup_data[entry], ["table", "column", "operator", "value", "next"])
        if not valid:
            return {"status_code": 400,
                    "results": {"error": "bad query",
                                "culprit": entry}
                    }

        table = lookup_data[entry]["table"]
        if table not in valid_tables.keys():
            return {"status_code": 400,
                    "results": {"error": "bad table",
                                "culprit": table}
                    }
        
        else:
            table = valid_tables[table]
            
        column = lookup_data[entry]["column"]
        if column not in valid_columns[table].keys():
            return {"status_code": 400,
                    "results": {"error": "bad column",
                                "culprit": column}
                    }
        
        else:
            column = valid_columns[table][column]
            
        kind = lookup_data[entry]["next"]
        operator = lookup_data[entry]["operator"]
        query += build_where(table, column, kind, operator)
        values.append(lookup_data[entry]["value"])
    
    query = query.replace("table", select_table)
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query , values)
    result = cursor.fetchall()
    data = []
    for row in result:
        data_row = {}
        for key in row.keys():
            data_row[key] = row[key]
            
        data.append(data_row)
    
    return {"status_code": 200,
            "results": data}

def build_where(table, column, kind, operator):
    base_where = "table.column operator ?"
    where = base_where.replace("column", column)
    where = where.replace("table", table)
    where = where.replace("operator", operators[operator])
    if kind != "END":
        where += "\n" + kind + " "
        
    else:
        pass
        
    return where

def update(table, row, columns, values):
    response = {}
    valid_columns = {"sports":get_columns("sports"),
                     "events":get_columns("events"),
                     "selections":get_columns("selections")
                     }
    if len(columns) != len(values):
        response["status_code"] = 400
        response["data"] = "bad request"
        
    else:
        cols_vals = "column = ?"
        columns_values = ""
        values_data = []
        
        for i in range(len(columns)):
            if columns[i] not in valid_columns[table]:
                response["status_code"] = 404
                response["data"] = {"data":"column not found"}
                break
            
            elif row not in get_all_ids(table):
                response["status_code"] = 404
                response["data"] = {"data":"id not found"}
                
            if columns[i] == columns[-1]:
                columns_values += cols_vals 
                
            else:
                columns_values += cols_vals + ", "
                
            columns_values = columns_values.replace("column", columns[i])
            values_data.append(values[i])
        
        if not response["data"]:
            query = patch
            query = query.replace("columns_values", columns_values)
            query = query.replace("table", table)
            values_data.append(row)
            db = get_db()
            db.execute(query, values_data)
            db.commit()
            response["status_code"] = 200
            response["data"] = {"status":"success"}
    
    return response

def slugify(name, table):
    slug = name.replace(" ", "-")
    slug = slug.replace("/", "_")
    slug = slug.replace("\\", "_")
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

def get_id(column, table, data):
    db = get_db()
    query = find_id.replace("column", column)
    query = query.replace("table", table)
    cursor = db.cursor()
    cursor.execute(query, (data, ))
    results = cursor.fetchone()
    return results["id"]

def get_columns(table):
    db = get_db()
    query = table_lookup.replace("table_lookup", table)
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    col_list = {}
    for row in results:
        col_list[row["name"]] = row["name"]
        
    return col_list

def get_all_ids(table):
    db = get_db()
    query = get_ids.replace("table", table)
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    id_list = []
    for row in results:
        id_list.append(row["id"])
        
    return id_list

def valid_data(field, data):
    valid_dict = {"kind":["preplay", "inplay"],
                  "status":["pending", "started", "ended", "cancelled"],
                  "outcome":["unsettled", "void", "lose", "win"]
                  }
    if data in valid_dict[field]:
        return True
    else:
        return False