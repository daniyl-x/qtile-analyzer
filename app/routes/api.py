import json
from datetime import datetime

from flask import Blueprint, request

import app.db.query as qry
from app.db import get_db, close_db


api = Blueprint("api", __name__)


def allowed_filetype(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "json"


def valid_wm_class(wm_class: list[str]) -> bool:
    return isinstance(wm_class, list) and len(wm_class) == 2 and \
            all(isinstance(name, str) for name in wm_class)


def valid_time_format(time: str) -> bool:
    try:
        datetime.fromisoformat(time)
        return True
    except (TypeError, ValueError):
        return False


@api.post("/upload")
def upload():
    file = request.files.get("file")
    if not file:
        return json.dumps({"error": "No valid file provided"}), 400
    if not allowed_filetype(file.filename):
        return json.dumps({"error": "File type is not allowed"}), 415

    lines_saved = 0
    lines_skipped = 0
    try:
        db = get_db()
        for line in file:
            try:
                line = json.loads(line)
            except json.JSONDecodeError:
                lines_skipped += 1
                continue

            time = line.get("time")
            if not time or not valid_time_format(time):
                lines_skipped += 1
                continue

            wm_class = line.get("wm_class")
            if wm_class and valid_wm_class(wm_class):
                wm_class_id = qry.store_wm_class(db, wm_class)
                if not qry.successful_insert(db, qry.INSERT_FOCUS_WM_CLASS,
                                             (time, wm_class_id,)):
                    lines_skipped += 1
                    continue
                lines_saved += 1
            else:
                if not qry.successful_insert(db, qry.INSERT_FOCUS_NONE,
                                             tuple(time)):
                    lines_skipped += 1
                    continue
                lines_saved += 1
    finally:
        close_db()

    file.close()
    return json.dumps({
        "message": "File uploaded successfully",
        "lines_saved": lines_saved,
        "lines_skipped": lines_skipped,
    })


@api.get("/total-time")
def total_time():
    db = get_db()
    log = db.execute("SELECT time FROM focus").fetchall()
    close_db()

    total_time = log[-1]["time"] - log[0]["time"]
    total_time = total_time.total_seconds()

    return json.dumps({"total_time": total_time})


@api.get("/time-per-program")
def time_per_program():
    db = get_db()
    log = db.execute(qry.SELECT_TIME_PER_PROGRAM).fetchall()
    close_db()

    log = list(map(dict, log))
    time_per_program = {}
    log_len = len(log)
    for i in range(log_len):
        program_name = log[i].get("class_name")
        if program_name not in time_per_program:
            time_per_program[program_name] = 0

        if i < (log_len - 1):
            delta = log[i + 1]["time"] - log[i]["time"]
            delta = delta.total_seconds()
            time_per_program[program_name] += delta

    return json.dumps(time_per_program)
