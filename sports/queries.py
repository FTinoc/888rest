from sports.db import get_db
from . import util
from datetime import datetime

new_sport = "INSERT INTO sports (name, slug) VALUES (?, ?)"
new_event = ("INSERT INTO events (name, slug, active, kind, sport_id, status, scheduled_start, actual_start) "
             "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
             )
new_selection = ("INSERT INTO selections (name, price, active, outcome, event_id, sport_id)"
                 "VALUES (?, ?, ?, ?, ? , ?)"
                 )

sports = "SELECT * FROM sports"
events = "SELECT * FROM events WHERE sport_id = ?"
selections = "SELECT * FROM selections WHERE event_id = ?"

db_query = "SELECT column FROM table"
id_lookup = "SELECT id FROM table WHERE column = ?"
lookup =    ("SELECT table.*, "
             "table_metrics.* "
             "FROM sports spt " 
            "LEFT JOIN events evt ON evt.sport_id = spt.id "
            "LEFT JOIN sports_metrics spt_metrics ON spt_metrics.id = spt.id "
            "WHERE "
            )

table_lookup = "PRAGMA table_info(table_lookup)"
view_lookup = "PRAGMA view_info(table_lookup)"

patch = "UPDATE table SET columns_values WHERE id = ?"

get_ids = "SELECT id FROM table"

operators = {"equ":"=", "not":"<>",
             "grt":">", "gqu":">=",
             "lss":"<","lqu":"<="}

#Simpler query to read all rows from table wo filters
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

def create(data, table):
    db = get_db()
    response = {"status_code":200, "data":{"status":"success"}}
    sport = None
    event = None
    valid = True
    
    if table == "sports":
        slug = slugify(data["name"], "sports")
        query = new_sport
        arguments = (data["name"], slug)
        
    elif table == "events":
        sport = get_id("slug", "sports", data["sport"])
        slug = slugify(data["name"], "events")
        if valid_data("scheduled_start", data["scheduled_start"]) and valid_data("kind", data["kind"]):
            query = new_event
            arguments = (data["name"], slug, data["active"], data["kind"], sport,
                         data["status"], data["scheduled_start"], data["actual_start"])
        else:
            valid = False
        
    elif table == "selections":
        sport = get_id("slug", "sports", data["sport"])
        event = get_id("slug", "events", data["event"])
        if valid_data("outcome", data["outcome"]):
            query = new_selection
            arguments = (data["name"], data["price"], data["active"], data["outcome"], event, sport)
        else:
            valid = False
    if valid:
        try:
            db.execute(query, arguments)
            db.commit()
            if "active" in data.keys():
                if data["active"]:
                    cascade_active(True, table, {"sports_id":sport, "events_id":event})
        except Exception as e:
            response["status_code"] = 500
            response["data"] = "DB error: " + str(Exception(e))
    else:
        response["status_code"] = 400
        response["data"] = {"error": "bad value"}
    return response
    
def read(lookup_data, select_table):
    query = lookup
    values = []
    valid_tables = {"sports":"spt", "events":"evt", "selections":"slt"}
    valid_columns = {"spt":get_columns("sports"),
                     "evt":get_columns("events"),
                     "slt":get_columns("selections")
                     }
    valid_metrics = {"spt":get_columns("sports_metrics"),
                     }
    for entry in lookup_data.keys():
        valid = util.validate_dict(lookup_data[entry], ["table", "column", "operator", "value", "next"])
        if valid:
            table = lookup_data[entry]["table"]
            if table in valid_tables.keys():
                table = valid_tables[table]
                column = lookup_data[entry]["column"]
                if column in valid_columns[table].keys():
                    kind = lookup_data[entry]["next"]
                    operator = lookup_data[entry]["operator"]
                    query += build_where(table, column, kind, operator)
                    values.append(lookup_data[entry]["value"])
                
                elif column in valid_metrics["spt"].keys():
                    kind = lookup_data[entry]["next"]
                    operator = lookup_data[entry]["operator"]
                    query += build_where(table, column, kind, operator, True)
                    values.append(lookup_data[entry]["value"])
                
                else:
                    valid = False
                    break
            else:
                valid = False
                break
        else:
            break
        
    if valid:
        query = query.replace("table", select_table)
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query , values)
        result = cursor.fetchall()
        results = []
        status_code = 200
        for row in result:
            data_row = {}
            for key in row.keys():
                data_row[key] = row[key]
            results.append(data_row)
    else:
        status_code = 400
        results = "bad request"
    
    return {"status_code": status_code,
            "data": results}

def update(table, row, columns, values, cascade = True, slug_list = []):
    response = {"data":[]}
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
            try:
                id_list = {}
                db.execute(query, values_data)
                db.commit()
                if cascade and "active" in columns and slug_list:
                    for key in slug_list.keys():
                        id_list[key+"_id"] = get_id("slug", key, slug_list[key])
                    cascade_active(values[columns.index("active")], table, id_list)
                response["status_code"] = 200
                response["data"] = {"status":"success"}
            except Exception as e:
                response["status_code"] = 500
                response["data"] = "DB error: " + str(Exception(e)) + " " + query
    
    return response

def build_where(table, column, kind, operator, metrics = False):
    base_where = "table.column operator ?"
    where = base_where.replace("column", column)
    if metrics:
        where = where.replace("table", table + "_metrics")
    else:
        where = where.replace("table", table)
    where = where.replace("operator", operators[operator])
    if kind != "END":
        where += "\n" + kind + " "
    return where

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
    query = db_query.replace("column", column)
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
    query = id_lookup.replace("column", column)
    query = query.replace("table", table)
    cursor = db.cursor()
    cursor.execute(query, (data, ))
    results = cursor.fetchone()
    return results["id"]

#compare col_list against input to prevent sql injection when querying db
def get_columns(table, metrics = False):
    db = get_db()
    if not metrics:
        query = table_lookup.replace("table_lookup", table)
    else:
        query = view_lookup.replace("table_lookup", table)
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
    elif field in ["actual_start", "scheduled_start"]:
        try:
            datetime.fromisoformat(data)
        except ValueError:
            return False
    else:
        return False

def cascade_active(active, table, id_list):
    if active:
        if table == "selections":
            update("events", id_list["events_id"], ["active"], [True], False)
            cascade_active(active, "events", id_list)
        if table == "events":
            update("sports", id_list["sports_id"], ["active"], [True], False)
    else:
        if table == "selections":
            other_active = read({"1":
                                    {"table":"events",
                                    "column":"active_selections",
                                    "operator":"gqu",
                                    "value":1,
                                    "next":"END"
                                    }
                                },"events")
            if not other_active["data"]:
                update("events", id_list["events_id"], ["active"], [False], False)
                cascade_active(active, "events", id_list)
        if table == "events":
            other_active = read({"1":
                                    {"table":"sports",
                                    "column":"active_events",
                                    "operator":"gqu",
                                    "value":1,
                                    "next":"END"
                                    }
                                },"sports")
            if not other_active["data"]:
                update("sports", id_list["sports_id"], ["active"], [False], False)