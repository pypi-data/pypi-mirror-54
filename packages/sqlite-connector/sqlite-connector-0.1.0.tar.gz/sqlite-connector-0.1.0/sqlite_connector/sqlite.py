"""
ExcelConnector(): SQLite connection
"""

import logging
import sqlite3

logger = logging.getLogger('SQLiteConnector')


class SQLiteConnector:
    """
    SQLite connection and functions
    """
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

        logger.info('Database connection established.')

    def execute_transform(self, file_path: str) -> None:
        """
        Execute transformation script in SQLite using provided connection
        :param file_path: Absolute path of the script
        :return: None
        """
        logger.info('Executing Transformation Script')

        query = open(file_path, 'r').read()
        c = self.connection.cursor()
        c.executescript(query)
        c.close()
        self.connection.commit()
        logger.info('Transformation script executed successfully')
