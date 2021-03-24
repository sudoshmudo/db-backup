import datetime
import os

from dotenv import load_dotenv
from synology_api import filestation

load_dotenv()

DOCKER_CONTAINER = os.environ['DOCKER_CONTAINER']
FILE_PREFIX = os.environ['FILE_PREFIX']
POSTGRES_USER = os.environ['POSTGRES_USER']
SYNOLOGY_PASSWORD = os.environ['SYNOLOGY_PASSWORD']
SYNOLOGY_PATH = os.environ['SYNOLOGY_PATH']
SYNOLOGY_PORT = os.environ['SYNOLOGY_PORT']
SYNOLOGY_USER = os.environ['SYNOLOGY_USER']
SYNOLOGY_HOST = os.environ['SYNOLOGY_HOST']

def get_date():
    return datetime.date.today().strftime('%Y-%m-%d')

def main():
    filename = '{}_{}.sql'.format(FILE_PREFIX, get_date())

    os.system('exec -t {} pg_dumpall -c -U {} > {}'.format(DOCKER_CONTAINER, POSTGRES_USER, filename))

    synology_server = filestation.FileStation(SYNOLOGY_HOST, SYNOLOGY_PORT, SYNOLOGY_PATH, SYNOLOGY_PASSWORD, secure=True)

    synology_server.upload_file(SYNOLOGY_PATH, filename)

if __name__ == "__main__":
    main()
