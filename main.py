import os
import json
from os import listdir
from os.path import isfile, join

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
    # -------- series handling --------
    with open('data/series.json') as file:
        series_data = json.load(file)
        for key, value in series_data.items():
            series_data[key]['articles'] = [url.replace('https://www.', "").rstrip('/') for url in value['articles']]
    for name in series_data:
        pathlib.Path(output_folder + name).mkdir(exist_ok=True)
    reversed_series = {}
    for key, value in series_data.items():
        for url in value['articles']:
            reversed_series[url] = key

    # -------- writing articles files --------
    titles = []
    articles = await request.json()
    for key, article in articles.items():
        title = article['title']
        titles.append(title)

        series = reversed_series.get(key, '')
        if series:
            position = series_data[series]['articles'].index(key)
            position += series_data[series].get('start', 0)
            series = series + '/'
            title = f"{position:02d} {title}"

        article['annotations'].sort(key=lambda x: x['position'])
        with open(f"{output_folder}{series}{title}.md", "w") as f:
            f.write(template.render(
                **article,
                excaped_title=title.replace("'", "''"),
                url=key,
                slug=slugify(title)
            ))

    # -------- removing files for not passed articles --------
    files = [file[:-3] for file in listdir(output_folder) if
             isfile(join(output_folder, file)) and not file.startswith('_')]
    for file in set(files) - set(titles):
        os.remove(f"{output_folder}{file}.md")

    return {}
