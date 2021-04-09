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

def main():
    os.chdir('/tmp')

    synology_server = filestation.FileStation(SYNOLOGY_HOST, SYNOLOGY_PORT, SYNOLOGY_USER, SYNOLOGY_PASSWORD, secure=True)

    results = synology_server.search_start(folder_path=SYNOLOGY_PATH, pattern='fin_', extension='sql')

    id = results.split('your id is: ')[1].replace('"', '')

    file_info = synology_server.get_search_list(task_id=id, limit=1, sort_by='crtime', sort_direction='desc')['data']['files'][0]

    synology_server.get_file(file_info['path'], 'download')

    os.system('cat {} | docker exec -i {} psql -U {}'.format(file_info['name'], DOCKER_CONTAINER, POSTGRES_USER))

if __name__ == "__main__":
    main()
