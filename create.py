"""
Script for creating databases and users in a Postgres container.
"""

import os

from dotenv import load_dotenv
from synology_api import filestation

load_dotenv()

APPS_1_DATABASE = os.environ["APPS_1_DATABASE"]
APPS_1_PASSWORD = os.environ["APPS_1_PASSWORD"]
APPS_1_USER = os.environ["APPS_1_USER"]
APPS_2_DATABASE = os.environ["APPS_2_DATABASE"]
APPS_2_PASSWORD = os.environ["APPS_2_PASSWORD"]
APPS_2_USER = os.environ["APPS_2_USER"]
DOCKER_CONTAINER = os.environ["DOCKER_CONTAINER"]


def create_database(name: str):
    """Create database."""
    os.system(
        "docker exec -u postgres -it {} createdb {};".format(DOCKER_CONTAINER, name)
    )


def create_user(name: str, password: str):
    """Create user."""
    os.system(
        "docker exec -u postgres -it {} psql -c \"CREATE USER {} WITH PASSWORD '{}';\"".format(
            DOCKER_CONTAINER, name, password
        )
    )


def grant_access(database: str, user: str):
    """Grant database access to user."""
    os.system(
        'docker exec -u postgres -it {} psql -c "grant all privileges on database {} to {};"'.format(
            DOCKER_CONTAINER, database, user
        )
    )


def main():
    """Main entrypoint of the script."""

    create_database(APPS_1_DATABASE)
    create_user(APPS_1_USER, APPS_1_PASSWORD)
    grant_access(APPS_1_DATABASE, APPS_1_USER)

    create_database(APPS_2_DATABASE)
    create_user(APPS_2_USER, APPS_2_PASSWORD)
    grant_access(APPS_2_DATABASE, APPS_2_USER)


if __name__ == "__main__":
    main()
