from queue import Queue
from glouton.infrastructure.satnogNetworkClient import SatnogNetworkClient
from glouton.shared.logger import logger


class ObservationRepo:
    def __init__(self, cmd, repos):
        self.OBSERVATION_URL = 'observations/'
        self.__client = SatnogNetworkClient()
        self.__repos = repos
        self.__cmd = cmd
        self.__threads = []

    def extract(self):
        params = self.__create_request_params()
        page = 1
        while True:
            r = self.__client.get_from_base(
                self.OBSERVATION_URL, params)
            if r.status_code != 200:
                break

            logger.Info('scanning page...' + params['page'])
            self.__read_page(r.json(), self.__cmd.start_date, self.__cmd.end_date)
            page += 1
            params['page'] = str(page)

        print('\ndownloading started (Ctrl + C to stop)...\t~(  ^o^)~')
        self.__create_workers_and_wait()

    def __create_workers_and_wait(self):
        for repo in self.__repos:
            self.__threads.extend(repo.create_worker())
        while self.__is_one_thread_alive():
            for t in self.__threads:
                # let's control to main thread every seconds (in order to be able to capture Ctrl + C if needed)
                t.join(1)

    def __is_one_thread_alive(self):
        for thread in self.__threads:
            if thread.is_alive():
                return True

        return False

    def __read_page(self, observations, start_date, end_date):
        for observation in observations:
            for repo in self.__repos:
                repo.register_command(
                    observation, start_date, end_date)

    def __create_request_params(self):
        return {'satellite__norad_cat_id': self.__cmd.norad_id,
        'ground_station': self.__cmd.ground_station_id,
        'start': self.__cmd.start_date.isoformat(),
        'end': self.__cmd.end_date.isoformat(),
        'vetted_status': self.__cmd.observation_status,
        'vetted_user': self.__cmd.user,
        'transmitter_uuid': self.__cmd.transmitter_uuid,
        'transmitter_mode': self.__cmd.transmitter_mode,
        'transmitter_type': self.__cmd.transmitter_type,
        'page': '1',
        'format': 'json'}
