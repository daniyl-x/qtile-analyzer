DROP TABLE IF EXISTS wm_class;
DROP TABLE IF EXISTS focus;

CREATE TABLE wm_class (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instance_name TEXT NOT NULL,
    class_name TEXT NOT NULL,
    -- Ensure unique combinations
    UNIQUE(instance_name, class_name)
);

CREATE TABLE focus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time DATETIME UNIQUE NOT NULL,
    wm_class_id INTEGER,
    FOREIGN KEY (wm_class_id) REFERENCES wm_class(id)
);

