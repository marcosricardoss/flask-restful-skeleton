web: waitress-serve --port=$PORT --call 'app:create_app'
init: flask db init
migrate: flask db migrate
upgrade: flask db upgrade