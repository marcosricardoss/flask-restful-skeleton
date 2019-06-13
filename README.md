# Flask HTTP REST API Skeleton

Use this skeleton application to quickly setup and start to create a Flask HTTP REST API.


## Features

- SQLAlchemy ORM
- Flask-Migrate
- Pytest
- Line Commands
- Twelve-factor methodology
- SOLID design principles
- PEP-8 for code style
- Heroku deployable


## Strategy

This **Flask HTTP REST API** skeleton uses the **MVC** as its base architecture, where the *blueprint* package is the controller layer and the *model* package is the model layer.

The interface with the model layer is given by classes that use the **Repository Pattern**, containing the business rules of the application. To make interaction with the model layer as simple as possible, the design pattern **Factory Method** is used for creating new repositories for a specific implementation. The Factory Method not only provides a user-friendly interface with the model layer but also implements the **SOLID** principles **Single Responsibility Principle** and **Open / Closed Principle**, which avoids tight couplings.


## Project layout
	.
	├── app
	│   ├── blueprint
	│   │   ├── authentication
	│   │   ├── handler
	│   │   ├── index.py
	│   │   └── users.py
	│   ├── commands
	│   ├── config.py
	│   ├── __init__.py
	│   └── model
	│       ├── database.py
	│       ├── factory.py
	│       ├── po.py
	│       └── repository
	├── instance
	├── migrations
	├── Procfile
	├── README.md
	├── requirements.txt
	├── setup.cfg
	└── tests
		├── conftest.py
		├── test_base.py
		├── test_db.py
		├── test_factory.py
		└── users_blueprint
			├── test_user_delete.py
			├── test_user_patch.py
			├── test_user_register.py
			├── test_user_retrieve.py
			├── test_user_update.py
			└── util.py

**app/blueprint**: The *controller* layer.

- **authentication:** Contains function decorators used to control the access on the API routes.
- **handler**: Contains functions to deal with the error exceptions of API.
- **index.py**: A blueprint to organize and group views related to the index endpoint.
- **user.py**: A blueprint to organize and group views related  to the `/users` endpoints.

**app/commands**: Package to keep the commands line.

**app/config.py**: Keeps the settings classes that are loading according to the running environment.

**app/__init__.py**: Contains the factory function 'create_app' that is responsible for initializing the application according to a previous configuration.

**app/model**: The *model* layer.

- **database.py:**: Initialize the database.
- **factory.py**: Contains the repositories factories implementations. Each concrete factory class is a subclass of RepositoryFactory class.
- **po.py**: *Persistent* objects of the SQLAlchemy, also known as *Model*.
- **repository**: Contains the repository implementations. Each repository implementation has its own package and is a subclass of the Repository class.


## Run The Application

In order to run the application, it is necessary to have a database configured. With that done, is necessary to the passe the database URI to the application via environment variables. This **Flask HTTP REST API** skeleton support to work with PostgreSQL and SQLite databases.

Database URLs examples:

	PostgreSQL: 'postgresql+psycopg2://postgres:123@127.0.0.1:15432/olist_test'
	SQLite: 'sqlite:////home/user/app.db'

To make sure about the *dependency isolation* is recommended to use the *[venv](http://https://docs.python.org/3/library/venv.html "venv")* to create of virtual environments.

After downloading the cloned open the project directory and install the dependencies with the below *pip* command: 

`pip install -r requirements.txt`

And the database migrations with:

`flask db init`<br>
`flask db migrate`<br>
`flask db upgrade`<br>

Note: This will add a migrations folder to your application. The contents of this folder need to be added to version control along with your other source files.

**Running on Development**

To run the application, we need to add two variables to the environment: **FLASK_ENV** and **DATABASE_URL**. The first one informs the Flask the type of environment and the second is the URL to the database source. 

In Linux SO this command will look like this:

`export FLASK_ENV=development`<br>
`export DATABASE_URL=postgresql+psycopg2://postgres:password@127.0.0.1:15432/database_name`<br>

And to run the application do:

`Flask run`

To facilitate the development process we can use .env file to load variable to the environment. The *local.env* file, in the *app* folder, is an example for a .env file.

**Running on Production** 

In the production enviroment, you just need to set the DATABASE_URL environment variable. Then you can use the command:

`waitress-serve --call 'flaskr:create_app'`

[Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/ "Waitress") is a the production WSGI server.

**Running the Tests**

To run the test, you need to set the DATABASE_URL environment variable too. Like in development, you can use a test/.env to set the DATABASE_URL variable.

Run the test with the command:

`python -m pytest`

You can olso run with coverage:

`coverage run -m pytest`

**Deploying to Heroku**

The application is ready to deploy in Heroku, being only necessary to create an application and a database in the Heroku platform.

After deploying the application will be started according to the existing configuration in the Procfile file. Then you can apply the migration to the database with the `heroku run upgrade` command.

**Note**: Note: You need to create a migration repository and generate the migrations locally. On the Heroku you only must do the database upgrade.

*Locally:*

`flask db init`<br>
`flask db migrate`<br>

*On Heroku:*

`heroku run init`


## Examples of Use

You can use the Postman to try the HTTP REST API. Download 
*Postman Collections* of requests in the link below and import to Postman. 

[Download Postman Collections](https://www.getpostman.com/collections/f177968870d56e2828a3 "Download Postman Collections")

This Postman collection collection collection was made based on:

	Host: 127.0.0.1
	Port: 5000
	User: demo (Base Auth)
	password: demo (Base Auth)

To create the new user, use `user` command:

`flask user demo demo`


## Contributing

Whether reporting bugs, discussing improvements and new ideas or writing extensions: Contributions are welcome! Here's how to get started:

1. Fork the repository on Github, create a new branch off the master branch and start making your changes (known as[ GitHub Flow](https://guides.github.com/introduction/flow/index.html " GitHub Flow"))
2. Write a test which shows that the bug was fixed or that the feature works as expected
3. Send a pull request and bug the maintainer until it gets merged and published


## Credits

[Marcos Ricardo](https://github.com/marcosricardoss/)

## License

### The MIT License (MIT)

Copyright (c) 2018 Marcos Ricardo <marcosricardoss@gmail.com>

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.