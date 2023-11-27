from fastapi import FastAPI
import re
import json
from pydantic import BaseModel

app = FastAPI()


class ReqType(BaseModel):
    day: str
    batch: str
    file: str


@app.post("/")
async def get_subject_data(req: ReqType):
    batch = req.batch
    day = req.day
    file = req.file

    day_map = []

    classes = {}
    with open(file) as f:
        data = json.load(f)

        for d in data:
            if d["Column1"] == day:
                day_map.append(d)

    for d in day_map:
        for x, y in d.items():
            _m = re.match(r"^.*?\(", y)
            if not _m:
                continue

            result = _m.group(0)[:-1]
            class_string = result.split(",")

            for i in class_string:
                if batch in i:
                    classes[x] = y
    to_return = {
        "9-9.50 AM" : "",
        "10-10.50 AM" : "",
        "11-11.50 AM" : "",
        "12-12.50 PM" : "",
        "1-1.50 PM" : "",
        "2-2.50 PM" : "",
        "3-3.50 PM" : "",
        "4-4.50 PM" : "",
    }

    for x, y in classes.items():
        match_parentheses = re.search(r"\((.*?)\)", y)
        match_hyphen_slash = re.search(r"-(.*?)/", y)

        subject_code = match_parentheses.group(1) if match_parentheses else None
        room_no = match_hyphen_slash.group(1) if match_hyphen_slash else None

        to_return[x] = f"{subject_code},{room_no}"

    return to_return
