import ast

from pytest_influxdb.test_result_dto import TestResultDTO
from pytest_influxdb.suite_result_dto import SuiteResultDTO


class DataManager:
    def save_db_data_in_properties(self, request, db_host, db_port, db_user, db_password, db_name,
                                   influxdb_values):
        request.node.user_properties = ({"influxdb": dict(influxdb_host=db_host, influxdb_port=db_port,
                                                          influxdb_user=db_user, influxdb_password=db_password,
                                                          influxdb_name=db_name, influxdb_values=influxdb_values)},)

    def get_test_result_dto(self, test_name, session_dict):
        test_result_dto_dict = session_dict.get('test_result_dto_session_dict')
        test_result_dto_dict.update({test_name: TestResultDTO()})
        test_result_dto: TestResultDTO = test_result_dto_dict.get(test_name)
        test_result_dto.set_test(test_name)
        return test_result_dto

    def get_report(self, request):
        try:
            report_outcome = request.node.rep_call
        except AttributeError:
            report_outcome = request.node.rep_setup
        return report_outcome

    def get_test_influxdb_components(self, influxdb, session_dict):
        influxdb_components = session_dict.get('influxdb')
        if not influxdb_components:
            session_dict.update({'influxdb': influxdb})
            influxdb_components = session_dict.get('influxdb')
        return influxdb_components

    def collect_custom_values(self, test_result_dto, influxdb_values):
        custom_values = influxdb_values
        if custom_values and custom_values is not '':
            influxdb_values_dict: dict = ast.literal_eval(str(custom_values))
            test_result_dto.set_field_values(test_result_dto.get_test(), influxdb_values_dict['fields']['test_result'])
            test_result_dto.set_tag_values(test_result_dto.get_test(), influxdb_values_dict['tags']['test_result'])

    def collect_user_properties(self, test_result_dto, request):
        user_properties_tuple = request.node.user_properties
        for var in user_properties_tuple:
            if isinstance(var, dict):
                test_result_dto.set_field_values(test_result_dto.get_test(), var)

    def generate_test_result_data(self, test_result_dto, project_name, release_version, run_id_value, report_outcome,
                                  merged):
        test_result_dto.set_project(project_name)
        test_result_dto.set_version(release_version)
        test_result_dto.set_run(run_id_value)
        test_result_dto.set_duration_sec(report_outcome.duration)
        test_result_dto.set_status(report_outcome.outcome)
        test_result_dto.set_merged(merged)

    def get_test_influxdb_credentials(self, terminalreporter):
        influxdb_creds_dict = dict()
        for test_obj in terminalreporter.stats.get(''):
            if test_obj.when == 'teardown' and (('skip' or 'xfailed' not in test_obj.keywords)):
                user_influxdb_creds_dict = test_obj.user_properties[0].get('influxdb')
                influxdb_creds_dict.update(dict(influxdb_test_host=user_influxdb_creds_dict['influxdb_host'],
                                                influxdb_test_port=user_influxdb_creds_dict['influxdb_port'],
                                                influxdb_test_user=user_influxdb_creds_dict['influxdb_user'],
                                                influxdb_test_password=user_influxdb_creds_dict['influxdb_password'],
                                                influxdb_test_name=user_influxdb_creds_dict['influxdb_name'],
                                                influxdb_test_values=user_influxdb_creds_dict['influxdb_values'],
                                                ))
                break
        return influxdb_creds_dict

    def get_valid_influxdb_creds(self, terminalreporter, config):
        influxdb_creds_dict = self.get_test_influxdb_credentials(terminalreporter)

        db_host = config.getoption("--influxdb_host")
        if not db_host:
            db_host = config.getini("influxdb_host")
            if not db_host:
                db_host = influxdb_creds_dict.get("influxdb_test_host")

        db_port = config.getoption('--influxdb_port')
        if not db_port:
            db_port = config.getini("influxdb_port")
            if not db_port:
                db_port = influxdb_creds_dict.get("influxdb_test_port")
                if not db_port:
                    db_port = 8086
        db_user = config.getoption("--influxdb_user")
        if not db_user:
            db_user = config.getini("influxdb_user")
            if not db_user:
                db_user = influxdb_creds_dict.get("influxdb_test_user")

        db_password = config.getoption("--influxdb_password")
        if not db_password:
            db_password = config.getini("influxdb_password")
            if not db_password:
                db_password = influxdb_creds_dict.get("influxdb_test_password")

        db_name = config.getoption("--influxdb_name")
        if not db_name:
            db_name = config.getini("influxdb_name")
            if not db_name:
                db_name = influxdb_creds_dict.get("influxdb_test_name")

        influxdb_values = config.getoption("--influxdb_values")
        if not influxdb_values:
            influxdb_values = influxdb_creds_dict.get("influxdb_test_values")

        influxdb_creds_dict.clear()
        influxdb_creds_dict.update(
            dict(db_host=db_host, db_port=db_port, db_user=db_user, db_password=db_password, db_name=db_name,
                 influxdb_values=influxdb_values))

        return influxdb_creds_dict
