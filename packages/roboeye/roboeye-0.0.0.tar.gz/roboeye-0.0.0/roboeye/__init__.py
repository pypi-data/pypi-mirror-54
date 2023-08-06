from pathlib import Path
import json
import csv

import yaml
import mistletoe


class Database(dict):

    def __init__(self, path):
        self.update(self._parse(Path(path), {}))

    def _parse(self, path, ctx):
        if path.is_dir():
            return Directory(self._parse, ctx, path)
        elif path.suffix == '.json':
            return Json(self._parse, ctx, path)
        elif path.suffix in ['.yml', '.yaml']:
            return Yaml(self._parse, ctx, path)
        elif path.suffix in ['.md']:
            return Markdown(self._parse, ctx, path)
        elif path.suffix in ['.csv']:
            return Csv(self._parse, ctx, path)
        else:
            raise Exception("omfg! i dont get {}".format(path))


def strip_ext(path):
    return path.name if path.suffix == '' else path.name[:-len(path.suffix)]


class Directory(dict):
    def __init__(self, parse, ctx, path):
        def key_func(path, item):
            return strip_ext(path)

        configfile = path / '.roboeye'
        if configfile.is_file():
            with configfile.open('rb') as fp:
                config = yaml.safe_load(fp)
                if 'index_by' in config:
                    def key_func(path, item):
                        return eval(config['index_by'], {}, {
                            "path": path,
                            "item": item
                        })

        items = [(sub, parse(sub, ctx))
                    for sub in path.iterdir()
                    if sub != configfile]

        super().__init__({key_func(filename, item): item
                            for filename, item in items})


class Markdown:
    def __init__(self, parse, ctx, path):
        with path.open('r', encoding='utf-8') as fp:
            self.doc = mistletoe.Document(fp)

    def as_html(self):
        with mistletoe.HTMLRenderer() as renderer:
            return renderer.render(self.doc)


class Yaml(dict):
    def __init__(self, parse, ctx, path):
        with path.open('rb') as fp:
            super().__init__(yaml.safe_load(fp))


class Json(dict):
    def __init__(self, parse, ctx, path):
        with path.open('rb') as fp:
            super().__init__(json.load(fp))


class Csv(list):
    def __init__(self, parse, ctx, path):
        with path.open('r') as fp:
            super().__init__(dict(row) for row in csv.DictReader(fp))
