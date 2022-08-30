import os
from typing import List

from fastapi import FastAPI
from starlette.requests import Request
from jinja2 import Environment, FileSystemLoader
from slugify import slugify

app = FastAPI()
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.md')
output_folder = f'{os.path.expanduser("~")}/Drive/sync/obsidian/Memex'


@app.post("/load")
async def load(request: Request):
    json = await request.json()
    for key, value in json.items():
        title = value['title']
        value['annotations'].sort(key=lambda x: x['position'])
        with open(f"{output_folder}/{title}.md", "w") as f:
            f.write(template.render(
                **value,
                excaped_title=title.replace("'", "''"),
                url=key,
                slug=slugify(title)
            ))
    return {}
