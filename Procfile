web: flask init-db
web: waitress-serve --port=$PORT --call 'app:create_app'