from db_reader import DbReader


class PostgresUtil(object):
    def __init__(self):
        try:
            self.sql_obj = DbReader()

        except Exception as e:
            raise Exception("DB Configuration Error" + str(e))

    def fetch_data_from_postgres(self, query):
        """
            This method is used for fetching the data from the table.
            :param query: query to fetch the data.
            :return: status: The status True on success and False on failure and the data.
        """
        result = []
        try:
            batch_size = 10000
            with self.sql_obj.sql_connect() as conn:
                conn.execute(query)
                while True:
                    rows = conn.fetchmany(batch_size)
                    if not rows:
                        break
                    result += rows
                column_names = [desc[0] for desc in conn.description]

            return result, column_names
        except Exception as e:
            print(e)
            return result, []