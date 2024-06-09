INSERT INTO sports (name, slug) 
VALUES ("football", "football"),
       ("golf", "golf");

INSERT INTO events (name, slug, active, kind, sport_id, status, scheduled_start, actual_start)
VALUES ("corinthians x palmeiras", "corinthians-x-palmeiras", 0, "inplay", 1, "pending", "2025-05-29 14:16:00", NULL),
       ("TW world tour", "TW-world-tour", 1, "preplay", 2, "pending", "2025-05-29 17:55:00", "2025-05-29 17:55:19");

INSERT INTO selections (name, price, active, outcome, event_id, sport_id)
VALUES ("2x0 corinthians", 5.60, 0, "win", 1 , 1),
       ("2x1 corinthians", 10.58, 1, "lose", 1 , 1),
       ("hole 1 - birdie", 50, 0, "lose", 2 , 2);