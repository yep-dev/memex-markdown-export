import os

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
        value['annotations'].sort(key=lambda x: x['position'])
        with open(f"{output_folder}/{value['title']}.md", "w") as f:
            f.write(template.render(**value, url=key, slug=slugify(value['title'])))
    return {}
