import json
from datetime import datetime

from flask import Blueprint


api = Blueprint("api", __name__)


def read_log(filename: str = "/tmp/qtile-focus-log-1000.json") -> list[dict]:
    log = []
    with open(filename, "r") as file:
        for line in file:
            line = json.loads(line)
            line["time"] = datetime.fromisoformat(line["time"])
            log.append(line)
    return log


@api.get("/total-time")
def total_time():
    log = read_log()
    total_time = log[-1]["time"] - log[0]["time"]
    total_time = total_time.total_seconds()

    return json.dumps({"total_time": total_time})


@api.get("/time-per-program")
def time_per_program():
    log = read_log()
    time_per_program = {}
    log_len = len(log)
    for i in range(log_len):
        program_name = log[i]["wm_class"][1]
        if program_name not in time_per_program:
            time_per_program[program_name] = 0

        if i < (log_len - 1):
            delta = log[i + 1]["time"] - log[i]["time"]
            delta = delta.total_seconds()
            time_per_program[program_name] += delta

    return json.dumps(time_per_program)
