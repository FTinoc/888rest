DROP TABLE IF EXISTS sports;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS selections;

DROP VIEW IF EXISTS [sports_metrics];
DROP VIEW IF EXISTS [events_metrics];



CREATE TABLE sports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    active BOOL DEFAULT 0 NOT NULL
);

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
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
    name TEXT NOT NULL,
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
        COUNT(evt.id) "quantity_events", 
        COUNT(slt.id) "quantity_selections",
        SUM(CASE evt.active
                WHEN 1 THEN 1
                ELSE 0
            END) "active_events",
        
        SUM(CASE slt.active
                WHEN 1 THEN 1
                ELSE 0
            END) "active_selections",
        
        SUM(CASE evt.status
                WHEN "pending" THEN 1
                ELSE 0
            END) "pending_events",
        
        SUM(CASE evt.status
                WHEN "started" THEN 1
                ELSE 0
            END) "ongoing_events",
            
        SUM(CASE evt.status
                WHEN "cancelled" THEN 1
                ELSE 0
            END) "cancelled_events",
        
        SUM(CASE slt.outcome
                WHEN "win" THEN 1
                ELSE 0
            END) "win_selections",
            
        SUM(CASE slt.outcome
                WHEN "lose" THEN 1
                ELSE 0
            END) "lose_selections",
        
        SUM(CASE slt.outcome
                WHEN "void" THEN 1
                ELSE 0
            END) "void_selections",
            
        SUM(CASE slt.outcome
                WHEN "unsettled" THEN 1
                ELSE 0
            END) "unsettled_selections"
        
FROM sports spt
LEFT JOIN events evt ON evt.sport_id = spt.id
LEFT JOIN selections slt ON slt.sport_id = spt.id
GROUP BY spt.id
