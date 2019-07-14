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
- JWT authentication

## Strategy

This **Flask HTTP REST API** skeleton uses the **MVC** as its base architecture, where the *blueprint* package is the controller layer and the *model* package is the model layer.

The interface with the model layer is given by classes that use the **Repository Pattern**, containing the business rules of the application. Associated with the **Strategy Pattern**, it not only provides a user-friendly interface with the model layer but also implements the **SOLID** principles **Single Responsibility Principle** and **Open / Closed Principle**, which avoids tight couplings.


## Project layout
	.
	└── app
	   ├── authentication.py
	   ├── blueprint
	   │   ├── account.py
	   │   ├── auth.py
	   │   ├── handlers.py	
	   │   └── index.py
	   ├── commands.py
	   ├── config.py
	   ├── database.py
	   ├── exceptions.py
	   ├── __init__.py
	   ├── local.env
	   └── model
	       ├── models.py
	       ├── repository.py
	       └── user_repository.py

**app/authentication:** Contains function decorators used to control JWT tokens authentication.

**app/blueprint**: The *controller* layer.

- **handler**: Contains functions to deal with the error exceptions of API.
- **account.py**: A blueprint to organize and group views related to the `/account` endpoints.
- **auth.py**: A blueprint to organize and group views related to the `/auth` endpoints.
- **index.py**: A blueprint to organize and group views related to the index endpoint.


**app/commands**: Package to keep the commands line.

**app/config.py**: Keeps the settings classes that are loading according to the running environment.

**app/database.py:**: The database bootstrapper.

**app/exceptions.py:**: Custom exceptions.

**app/__init__.py**: Contains the factory function 'create_app' that is responsible for initializing the application according to a previous configuration.

**app/local.env**: A sample of the *.env* config file..

**app/model**: The *model* layer.

- **models.py**: Persistent objects of the SQLAlchemy.
- **repository.py**: Contains Repository generic class.
- **user_repository.py**: Contains UserRepository class.

## Configuring and Running The Application

The following steps are required to run the application


### Configure The Database

This **Flask HTTP REST API** skeleton support to work with PostgreSQL and SQLite databases. With the database configured, you need to make the database URI containing the database credentials to access it. This URI will be set later for application through environment variables.

Database URIs examples:

	PostgreSQL: postgresql+psycopg2://username:123@127.0.0.1:15432/database_name
	SQLite: sqlite:////home/user/app.db


### Install The Dependencies

To make sure about the *[dependency isolation](https://12factor.net/dependencies "dependency isolation")* is recommended to use the *[venv](http://https://docs.python.org/3/library/venv.html "venv")* to create a virtual environment.

After downloading or cloned this repository, open the project directory and install the dependencies with the below *pip* command: 

`pip install -r requirements.txt`


### Setting The Environment Variables

To execute the application, do database migrations or performing any other command, it is necessary to configure two environment variables: FLASK_ENV and DATABASE_URL. These variables inform the Flask what is the environment of execution and the URI to access the database.

In Linux or Unix-like, this command will look like this:

`export FLASK_ENV=development`<br>
`export DATABASE_URL=postgresql+psycopg2://username:123@127.0.0.1:15432/database_name`<br>

The FLASK_ENV is a Flask environment variable using to configure the flask execution.  In this **Flask HTTP REST API** skeleton it is used to load the right database URI for the environment specified (development or production). **If FLASK_ENV it not informed the flask will run in production mode.**


### Perform Database Migration

You can do the database migrations with the following commands:

`flask db init`<br>
`flask db migrate`<br>
`flask db upgrade`<br>

Note: This will create the *migrations* folder to the application. The contents of this folder need to be added to version control along with your other source files.


### Running

**Development**

In development, you can use the built-in development server with the `flask run` command. Remember to set the environment and the database URI:

`export FLASK_ENV=development`<br>
`export DATABASE_URL=postgresql+psycopg2://postgres:password@127.0.0.1:15432/database_name`<br>
`Flask run`

For a smoother work-flow on development, you can use a .env file to load the database URI. The *local.env* file, in the *app* folder, is an example of use to .env file.

**Production** 

In the production environment, you just need to set the DATABASE_URL environment variable. Then you can use the command:

`waitress-serve --call 'app:create_app'`

[Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/ "Waitress") is the production WSGI server used for this project.

**Tests**

To run the test, you need to set the DATABASE_URL environment variable too. Like in development, you can use a test/.env to set the DATABASE_URL variable.

Run the test with the following command:

`python -m pytest`

You can also run with coverage:

`coverage run -m pytest`


## Configuring the Secret Key

The secret key is kept in the config.py module at the root of the application. Edit the `SECRET_KEY` class variable of the Production class with some random bytes. You can use the following command to output a random secret key:

	python -c 'import os; print(os.urandom(16))'
	b'_5#y2L"F4Q8z\n\xec]/'


## Deploying to Heroku

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

This Postman collection was made based on:

	Host: 127.0.0.1
	Port: 5000

**Note: To access a protected view, all we have to do is send in the JWT with the request. By default, this is done with an authorization header that looks like::**

	Authorization: Bearer <access_token>

	
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