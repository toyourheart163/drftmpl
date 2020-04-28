from os.path import join, exists
import os

from drftmpl.main import (
    _render,
    render,
    exists_app,
    get_project_name,
    add_model_to_import,
    add_to_tail,
    write_or_add_to_file,
    condition_filename
)

modules = ('viewset', 'serializer', 'router')
items = ['ViewSet', 'Serializer']
models = ['blog', 'bingo']
app = 'hi'
if not exists('hi'):
    os.makedirs('hi')


def test__render():
    data = '{{ name }}'
    assert _render(data, name='lisa') == 'lisa'


def test_render():
    for module in modules:
        tmpl = join('templates', module + 's.py.tmpl')
        assert module in render(tmpl, models=models).lower()
        tail_tmpl = join('templates', module + 's.tail.py.tmpl')
        assert module in render(tail_tmpl, models=models).lower()
    url_tmpl = join('templates', 'urls.py.tmpl')
    assert 'router' in render(url_tmpl, models='', app='hi')


def test_get_project_name():
    assert 'demo' == get_project_name()


def test_exists_app():
    assert exists_app('hi') == 'hi'


def tmpl(module, tail=''):
    if tail:
        return join('templates', '{}s.tail.py.tmpl'.format(module))
    else:
        return join('templates', f'{module}s.py.tmpl')


def test_add_model_to_import():
    data = render(tmpl('viewset'), models=models)
    assert 'AuthorSerializer' in add_model_to_import(data, ['Author'])
    data = render(tmpl('serializer'), models=models)
    assert 'Author' in add_model_to_import(data, ['Author'])


def test_add_to_tail():
    for module in modules[:-1]:
        pyfile = join(app, module + 's.py')
        if exists(pyfile):
            os.remove(pyfile)
        head = render(tmpl(module), models)
        tail = render(tmpl(module, 'tail'), models)
        filename = condition_filename(module, app)
        write_or_add_to_file(filename, head, tail)
    if exists(pyfile):
        assert items[1] in add_to_tail(tmpl('serializer', 'tail'), ['Auth'], join(app, 'serializers.py'))
        assert items[0] in add_to_tail(tmpl('viewset', 'tail'), ['Auth'], join(app, 'viewsets.py'))
