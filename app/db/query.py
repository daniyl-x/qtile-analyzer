INSERT_WM_CLASS = (
        "INSERT INTO wm_class (instance_name, class_name) VALUES (?, ?)"
)
SELECT_WM_CLASS_ID = (
        "SELECT id FROM wm_class WHERE instance_name=? AND class_name=?"
)
INSERT_FOCUS_WM_CLASS = "INSERT INTO focus (time, wm_class_id) VALUES (?, ?)"
INSERT_FOCUS_NONE = "INSERT INTO focus (time) VALUES (?)"
SELECT_TIME_PER_PROGRAM = (
        "SELECT focus.time, wm_class.class_name FROM focus LEFT JOIN wm_class "
        "ON focus.wm_class_id = wm_class.id"
)


def successful_insert(db, query: str, data: tuple) -> bool:
    try:
        db.execute(query, data)
        db.commit()
        return True
    except db.IntegrityError:
        return False


def store_wm_class(db, wm_class: list) -> int:
    if not successful_insert(db, INSERT_WM_CLASS, tuple(wm_class)):
        pass
    wm_class_id = db.execute(SELECT_WM_CLASS_ID,
                             tuple(wm_class)).fetchone()["id"]
    return wm_class_id
