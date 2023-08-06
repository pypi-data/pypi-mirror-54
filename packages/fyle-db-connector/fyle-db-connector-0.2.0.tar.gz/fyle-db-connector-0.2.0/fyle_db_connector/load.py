"""
FyleLoadConnector(): Connection between Fyle and Database
"""

import logging
from typing import BinaryIO

import pandas as pd
from fylesdk import FyleSDK

logger = logging.getLogger('FyleConnector')


class FyleLoadConnector:
    """
    - Extract Data from Database and load to Fyle
    """
    def __init__(self, fyle_config, database):
        self.__database = database

        self.__connection = FyleSDK(
            base_url=fyle_config.get('fyle_base_url'),
            client_id=fyle_config.get('fyle_client_id'),
            client_secret=fyle_config.get('fyle_client_secret'),
            refresh_token=fyle_config.get('fyle_refresh_token')
        )
        logger.info('Fyle connection established.')

    def __load_excel(self, file_path: str) -> str:
        """
        Upload Excel File to Fyle
        :param file_path: Absolute path for the excel file
        :return: returns file id
        """
        logger.info('Uploading excel to Fyle.')

        file_data = open(file_path, 'rb')

        file_path_tokenize = file_path.split('/')
        file_name = file_path_tokenize[len(file_path_tokenize) - 1]

        file_id = self.load_file(
            file_name,
            file_data,
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        logger.info('Excel file uploaded successfully.')
        return file_id

    def load_tpa_exports(self, file_path: str = None, file_id: str = None) -> None:
        """
        Load TPA Export Batches in Fyle
        :param file_path: Path of the export file
        :param file_id: Id of file already uploaded to Fyle
        :return: None
        """
        logger.info('Pushing export batch to Fyle.')

        batch = pd.read_sql_query(sql='select * from fyle_load_tpa_export_batch', con=self.__database.connection)

        lineitems = pd.read_sql_query(
            sql='select * from fyle_load_tpa_export_batch_lineitems',
            con=self.__database.connection
        )

        if not file_id:
            if file_path:
                file_id = self.__load_excel(file_path)
            batch['file_id'] = file_id

        batch['success'] = True

        batch_payload = batch.to_dict(orient='records')
        lineitems_payload = lineitems.to_dict(orient='records')

        if lineitems_payload:
            batch_id = self.__connection.Exports.post_batch(batch_payload[0])['id']

            logger.info('Batch successfully upload. Uploading Line items.')

            self.__connection.Exports.post_batch_lineitems(batch_id, lineitems_payload)

            logger.info('%s Lineitems successfully uploaded.', len(lineitems_payload))
        else:
            logger.info('0 Lineitems. Skipping exports')

    def load_file(self, file_name: str, file_data: BinaryIO, content_type: str) -> str:
        """
        Upload File to Fyle
        :param file_name: Name of the file
        :param file_data: Data of the fyle in bytes
        :param content_type: content type
        :return:
        """
        file_obj = self.__connection.Files.post(file_name)
        upload_url = self.__connection.Files.create_upload_url(file_obj['id'])['url']
        self.__connection.Files.upload_file_to_aws(content_type, file_data, upload_url)
        return file_obj['id']
