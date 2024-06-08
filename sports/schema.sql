DROP TABLE IF EXISTS sports;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS selections;

DROP VIEW IF EXISTS [sports_metrics];
DROP VIEW IF EXISTS [events_metrics];



CREATE TABLE sports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    active BOOL DEFAULT 0 NOT NULL
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    active BOOL DEFAULT 0 NOT NULL,
    kind TEXT NOT NULL,
    sport_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    scheduled_start TEXT NOT NULL,
    actual_start TEXT,
    FOREIGN KEY (sport_id) REFERENCES sports (id) ON UPDATE CASCADE
);

CREATE TABLE selections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    price REAL NOT NULL,
    active BOOL DEFAULT 0 NOT NULL,
    outcome TEXT DEFAULT 'Unsettled' NOT NULL,
    event_id INTEGER NOT NULL,
    sport_id INTEGER NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events (id) ON UPDATE CASCADE
    FOREIGN KEY (sport_id) REFERENCES events (sport_id) ON UPDATE CASCADE

);

CREATE VIEW [sports_metrics] AS 

SELECT  spt.id,    
        (SELECT COUNT(id) FROM events WHERE id = spt.id) "quantity_events", 
        (SELECT COUNT(id) FROM events WHERE id = spt.id AND active = 1) "active_events",
        (SELECT COUNT(id) FROM events WHERE id = spt.id AND kind = 'pending') "pending_events",
        (SELECT COUNT(id) FROM events WHERE id = spt.id AND kind = 'started') "started_events",
        (SELECT COUNT(id) FROM events WHERE id = spt.id AND kind = 'cancelled') "cancelled_events",
        (SELECT COUNT(id) FROM events WHERE id = spt.id AND kind = 'ended') "finished_events",    
        (SELECT COUNT(id) FROM selections WHERE id = spt.id) "quantity_selections",
        (SELECT COUNT(id) FROM selections WHERE id = spt.id AND active = 1) "active_selections", 
        (SELECT COUNT(id) FROM selections WHERE id = spt.id AND outcome = 'void') "void_selections",
        (SELECT COUNT(id) FROM selections WHERE id = spt.id AND outcome = 'win') "win_selections",
        (SELECT COUNT(id) FROM selections WHERE id = spt.id AND outcome = 'lose') "lose_selections",
        (SELECT COUNT(id) FROM selections WHERE id = spt.id AND outcome = 'unsettled') "unsettled_selections"  

FROM sports spt;

CREATE VIEW [events_metrics] AS 

SELECT  evt.id,
        (SELECT COUNT(id) FROM selections WHERE id = evt.id) "quantity_selections",
        (SELECT COUNT(id) FROM selections WHERE id = evt.id AND active = 1) "active_selections", 
        (SELECT COUNT(id) FROM selections WHERE id = evt.id AND outcome = 'void') "void_selections",
        (SELECT COUNT(id) FROM selections WHERE id = evt.id AND outcome = 'win') "win_selections",
        (SELECT COUNT(id) FROM selections WHERE id = evt.id AND outcome = 'lose') "lose_selections",
        (SELECT COUNT(id) FROM selections WHERE id = evt.id AND outcome = 'unsettled') "unsettled_selections" 

FROM events evt;