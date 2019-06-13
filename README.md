## Flask HTTP REST API Skeleton

Use this skeleton application to quickly setup and start to create a Flask HTTP REST API.

### Features

- SQLAlchemy ORM
- Flask-Migrate
- Pytest
- Line Commands
- Twelve-factor methodology
- SOLID design principles
- PEP-8 for code style

### Strategy

This **Flask HTTP REST API** skeleton uses the **MVC** as its base architecture, where the *blueprint* package is the controller layer and the *model* package is the model layer.

The interface with the model layer is given by classes that use the **Repository Pattern**, containing the business rules of the application. To make interaction with the model layer as simple as possible, the design pattern **Factory Method** is used for creating new repositories for a specific implementation. The Factory Method not only provides a user-friendly interface with the model layer but also implements the **SOLID** principles **Single Responsibility Principle** and **Open / Closed Principle**, which avoids tight couplings.

 ### Project layout

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