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