DROP TABLE IF EXISTS sports;
DROP TABLE IF EXISTS events;

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
    FOREIGN KEY (sport_id) REFERENCES sports (id)
);