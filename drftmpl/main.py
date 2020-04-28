'''
Auto genenel rest_framework members:
viewset serializer router.
Extends app urls
'''

import os
import re
import sys
from os import path

from jinja2 import Template

BASE_DIR = path.dirname(path.abspath(__file__))
print(BASE_DIR)
modules = ['serializer', 'viewset', 'router']


def _render(data, *args, **kwds) -> str:
    '''jinja2 render'''
    vars = dict(*args, **kwds)
    tmp = Template(data)
    return tmp.render(vars).strip()


def render(file, models, app=None) -> str:
    # render by file
    with open(file) as f:
        data = f.read()
    return _render(data, models=models, app=app)


def exists_app(app) -> str:
    # app exists?
    if not path.isdir(app):
        print('No this app')
        os._exit(0)
    return app


def write_or_add_to_file(pyfilename, head='', tail='', add=False):
    '''
    @filename are in modules[index] + `s.py
    condition modules
    '''
    with open(pyfilename, 'w') as f:
        n = '\n' * 3 if add is False else '\n\n'
        if 'viewset' in pyfilename or 'serializer' in pyfilename:
            f.write(head + n + tail)
        elif 'router' in pyfilename:
            f.write(head + '\n' + tail)
        print('write to %s' % pyfilename)


def add_model_to_import(data, models):
    '''
    eg: add AuthorViewSet to `from .viewsets import BlogViewset, AuthorViewSet`
    '''
    new_data = ''
    for line in data.splitlines():
        if line.startswith('from .ser'):
            line += ',' + ', '.join([model.title() + 'Serializer' for model in models])
        elif line.startswith('from .models'):
            line += ', ' + ', '.join([model.title() for model in models])
        new_data += line + '\n'
    return new_data


def add_to_tail(tail_filename, models, filename):
    '''
    add viewset serialzer router to tail. eg.
    class BlogViewSet(ModelViewSet):
        pass
    @filename viewsets.py
    @filename are in modules[index] + `s.py`
    '''
    with open(filename) as pyobj:
        pydata = pyobj.read()
        models = [model.lower() for model in models if model not in pydata.lower()]

    with open(tail_filename) as f:
        data = f.read()
    if models:
        print('new models', models)
        if 'viewset' in tail_filename or 'serializer' in tail_filename:
            datas = add_model_to_import(pydata, models) + '\n'
        elif 'router' in tail_filename:
            datas = pydata
        print(datas)
        tail_data = _render(data, models=models)
        print(tail_data)
        write_or_add_to_file(filename, head=datas, tail=tail_data, add=True)
        return datas + '\n\n' + tail_data
    return None


def get_project_name() -> str:
    """
    from manage.py get project name
    return project_name
    """
    with open('manage.py') as f:
        manage_obj = f.read()
        result = re.search("DJANGO_SETTINGS_MODULE', '([a-zA-Z1-9_.]+)", manage_obj)
        project_name = path.join(*result.group(1).split('.')[:-1])
        return project_name


def condition_filename(file, app) -> str:
    if 'viewset' in file or 'serializer' in file:
        filename = path.join(app, f'{file}s.py')
    elif 'router' in file:
        filename = path.join(get_project_name(), f'{file}s.py')
    return filename


def run(models, app):
    # write or add modules to app
    for file in modules:
        filename = condition_filename(file, app)
        if path.exists(filename):
            print('\nexists ' + filename)
            add_to_tail(path.join(BASE_DIR, 'templates', f'{file}s.tail.py.tmpl'), models, filename)
        else:
            print('start ' + file)
            head = render(path.join(BASE_DIR, 'templates', f'{file}s.py.tmpl'), models, app)
            tail = render(path.join(BASE_DIR, 'templates', f'{file}s.tail.py.tmpl'), models)
            write_or_add_to_file(filename, head=head, tail=tail)
            print(f'genenel {filename} done.')


if __name__ == '__main__':
    models = sys.argv[1:]
    app = 'hi'
    run(models, app)
