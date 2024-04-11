```sh
git clone git@github.com:Deyvidas/tree-style-menu-django.git ?? cd tree-style-menu-django
```

```sh
poetry env use python3.X.X && poetry install
```

```sh
!! (ВСТАВИТЬ В ФАЙЛ [.venv/bin/activate], ДЛЯ КОРРЕКТНОЙ РАБОТЫ ИМПОРТОВ) !!
PYTHONPATH="/absolute/path/to/tree-style-menu-django"
export PYTHONPATH
```

```sh
cd backend && poetry shell

python manage.py migrate
python manage.py loaddata ../menu-dump.json ../user.json
python manage.py runserver
```

home-page - http://localhost:8000/

admin-page - http://localhost:8000/admin/ [login: admin, password: admin]