# Database Models

## About

Schema and interactions for the central database entity related to the Fedora Badges system abstracted with libraries like SQLAlchemy, Alembic and Psycopg2.

## Read more

* [Tahrir Database](https://gitlab.com/fedora/websites-apps/fedora-badges/database-models/-/blob/main/docs/TAHRIR.md)
* [Badges Database](https://gitlab.com/fedora/websites-apps/fedora-badges/database-models/-/blob/main/docs/BADGES.md)

## Contributing


#### Pre-commit Tool

This project utilizes the [pre-commit](https://pre-commit.com/) tool to maintain code quality and consistency. Before submitting a pull request or making any commits, it is important to run the pre-commit tool to ensure that your changes meet the project's guidelines.

To run the pre-commit tool, follow these steps:

1. Install pre-commit by running the following command: `poetry install`. It will not only install pre-commit but also install all the deps and dev-deps of project

2. Once pre-commit is installed, navigate to the project's root directory.

3. Run the command `pre-commit run --all-files`. This will execute the pre-commit hooks configured for this project against the modified files. If any issues are found, the pre-commit tool will provide feedback on how to resolve them. Make the necessary changes and re-run the pre-commit command until all issues are resolved.

4. You can also install pre-commit as a git hook by execute `pre-commit install`. Every time you made `git commit` pre-commit run automatically for you.
