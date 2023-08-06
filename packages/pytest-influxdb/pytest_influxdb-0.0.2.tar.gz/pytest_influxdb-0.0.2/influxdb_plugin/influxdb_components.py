from influxdb import InfluxDBClient


class Influxdb_Components:
    __client = None

    def __init__(self, host, port, db_user, db_password, db_name):
        self.__client = InfluxDBClient(host, port, db_user, db_password, db_name)

    def get_client(self):
        return self.__client

    def get_results_by_run(self, measurement_name, run_id):
        return self.__client.query(
                f"SELECT * FROM {measurement_name} WHERE run='{run_id}'")

    def delete_results_by_run(self, measurement_name, run_id):
        return self.__client.query(
            f"DELETE FROM {measurement_name} WHERE run='{run_id}'")