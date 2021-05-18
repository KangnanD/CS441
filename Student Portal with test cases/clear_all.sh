#pip install --upgrade  virtualenv==20.4.3
#virtualenv -p python venv
#source ./venv/bin/activate
pip install -r requirements.txt
rm db.sqlite3
touch db.sqlite3
find . -path "./Member/migrations/*.py" -not -name "__init__.py" -delete
find . -path "./Member/migrations/*.pyc"  -delete
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  --username admin --email admin@localhost.com
python manage.py loaddata FileType.json
python manage.py loaddata Course.json
python manage.py loaddata Group.json
python manage.py loaddata Status.json
