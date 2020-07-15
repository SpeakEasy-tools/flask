# flask-server

## Dependencies

* Python 3.6+

## Development

This project uses the [poetry](https://python-poetry.org/) package manager to handle Python dependencies. Over pip,
this provides us with an easier specification of dependencies (`pyproject.toml`) and a lockfile (`poetry.lock`). To
get started, use the command `poetry install` to install the application dependencies into a new virtualenv that
poetry generates for this project.

In addition to the dependencies above, you will need to get a Google Cloud credentials file, that has the appropriate
access to the necessary services (e.g. Firebase, Speech to Text, Text to Speech). This credentials file should be saved
as `gcloud.json` and stored at the root of the repository.

To run the application, use `poetry run flask run`. This will run the flask server from within the virtualenv for the
application.

To simplify deployment, we utilize a `requirements.txt` file that poetry generates for us, by doing
`poetry export -f requirements.txt > requirements.txt`. This should be run immediately following adding a dependency by
doing `poetry add <dependency>`.

## Deployment

1. Install dependencies (`python3 -m pip install -r requirements.txt`)
1. Get credentials file (see https://firebase.google.com/docs/admin/setup#initialize-sdk), save as `gcloud.json` in this directory.
1. Run `flask run` in this directory
