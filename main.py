import os
import json

from fastapi import FastAPI
from starlette.requests import Request
from jinja2 import Environment, FileSystemLoader
from slugify import slugify
import pathlib

app = FastAPI()
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.md')
output_folder = f'{os.path.expanduser("~")}/Drive/sync/obsidian/Memex/'


@app.post("/load")
async def load(request: Request):
    with open('data/series.json') as file:
        series_data = json.load(file)
        for key, value in series_data.items():
            series_data[key]['articles'] = [url.lstrip('https://www.').rstrip('/') for url in value['articles']]
    for name in series_data:
        pathlib.Path(output_folder + name).mkdir(exist_ok=True)
    reversed_series = {}
    for key, value in series_data.items():
        for url in value['articles']:
            reversed_series[url] = key

    article = await request.json()
    for key, value in article.items():
        title = value['title']

        series = reversed_series.get(key, '')
        if series:
            position = series_data[series]['articles'].index(key)
            position += series_data[series].get('start', 0)
            series = series + '/'
            title = f"{position:02d} {title}"

        value['annotations'].sort(key=lambda x: x['position'])
        with open(f"{output_folder}{series}{title}.md", "w") as f:
            f.write(template.render(
                **value,
                excaped_title=title.replace("'", "''"),
                url=key,
                slug=slugify(title)
            ))
    return {}
