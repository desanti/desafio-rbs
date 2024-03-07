import logging

import pandas as pd

from hooks.randomuser.randomuser import RandomUserHook
from packages.pg_repository import UserRawRepository, UserCuratedRepository, UserApplicationRepository
from projects.user_transform import UserTransform


class ExtractUserToRaw:
    def __init__(self):
        self._user_results = 5000

    def execute(self):
        logging.info("Carregando os dados da API")
        data = self._get_data_from_api()

        logging.info("Gravando os dados na zona RAW")
        self._save_in_raw(data)

    def _get_data_from_api(self):
        hook = RandomUserHook()

        return hook.get_user(self._user_results)

    @staticmethod
    def _save_in_raw(data):
        repository = UserRawRepository()

        repository.save_users(data)

    @staticmethod
    def entrypoint(**kwargs):
        ExtractUserToRaw().execute()


class UserEventRawToCurated:

    @staticmethod
    def entrypoint(**kwargs):
        curated_repository = UserCuratedRepository()

        curated_repository.truncate_table()

        logging.info("Carregando os dados da zona RAW")
        for user in UserRawRepository().get_users():
            df = pd.DataFrame(user.get("event").get("results"))

            logging.info(df.info())

            logging.info("Aplicando transformações nos dados")
            df = UserTransform.transform(df)

            logging.info("Gravando os dados na zona Curated")
            curated_repository.save(df)


class UserCuratedToApplication:
    @staticmethod
    def entrypoint(**kwargs):
        curated_repository = UserCuratedRepository()
        app_repository = UserApplicationRepository()

        logging.info("Excluindo dados da Application Zone")
        app_repository.truncate_table()

        logging.info("Carregando os dados da Zona Curated")
        for df in curated_repository.get_all_users():
            logging.info("Gravando os dados na Application Zone")
            app_repository.save(df)
