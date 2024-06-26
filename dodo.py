import glob
import shutil
import doit

DOIT_CONFIG = {'default_tasks': ['html']}


def task_pot():
    return {
            'actions': ['pybabel extract src -o src/loc/loc.pot'],
            'file_dep': glob.glob('src/*.py'),
            'targets': ['src/loc/loc.pot'],
            }


def task_po():
    return {
            'actions': ['pybabel update --previous -D loc -d src/loc -i src/loc/loc.pot'],
            'file_dep': ['src/loc/loc.pot'],
            'targets': ['src/loc/ru_RU.UTF-8/LC_MESSAGES/loc.po'],
            }


def task_mo():
    return {
            'actions': ['pybabel compile -D loc -l ru_RU.UTF-8 -d src/loc -i src/loc/ru_RU.UTF-8/LC_MESSAGES/loc.po'],
            'file_dep': ['src/loc/ru_RU.UTF-8/LC_MESSAGES/loc.po'],
            'targets': ['src/loc/ru_RU.UTF-8/LC_MESSAGES/loc.mo'],
            }


def task_i18n():
    return {
            'actions': None,
            'task_dep': ['pot', 'po', 'mo'],
            }


def task_html():
    return {
            'actions': ['sphinx-build -M html docs _build'],
            'file_dep': glob.glob('docs/*.rst') + glob.glob('src/*.py'),
            'targets': ['docs'],
            }


def task_test():
    return {
            'actions': ['python -m unittest test_app.py'],
            }


def task_wheel():
    return {
            'actions': ['python -m build -nw'],
            'task_dep': ['i18n', 'html']
            }
