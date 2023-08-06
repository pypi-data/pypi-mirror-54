from pytest_influxdb.test_result_dto import TestResultDTO


class DataManager:
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

    def save_db_data_in_properties(self, request, db_host, db_port, db_user, db_password, db_name,
                                   influxdb_values, run, project, version):
        request.node.user_properties = ({"influxdb": dict(influxdb_host=db_host, influxdb_port=db_port,
                                                          influxdb_user=db_user, influxdb_password=db_password,
                                                          influxdb_name=db_name, influxdb_values=influxdb_values,
                                                          run=run, project=project, version=version)},)

    def get_test_influxdb_credentials(self, terminalreporter):
        influxdb_creds_dict = dict()
        for test_obj in terminalreporter.stats.get(''):
            if test_obj.when == 'teardown' and ('skip' not in test_obj.keywords):
                user_influxdb_creds_dict = test_obj.user_properties[0].get('influxdb')
                influxdb_creds_dict.update(dict(influxdb_test_host=user_influxdb_creds_dict['influxdb_host'],
                                                influxdb_test_port=user_influxdb_creds_dict['influxdb_port'],
                                                influxdb_test_user=user_influxdb_creds_dict['influxdb_user'],
                                                influxdb_test_password=user_influxdb_creds_dict['influxdb_password'],
                                                influxdb_test_name=user_influxdb_creds_dict['influxdb_name'],
                                                influxdb_test_values=user_influxdb_creds_dict['influxdb_values'],
                                                influxdb_run_value=user_influxdb_creds_dict['run'],
                                                influxdb_project_value=user_influxdb_creds_dict['project'],
                                                influxdb_version_value=user_influxdb_creds_dict['version']
                                                ))
                break
        return influxdb_creds_dict

    def get_valid_influxdb_values(self, terminalreporter):
        influxdb_creds_dict = self.get_test_influxdb_credentials(terminalreporter)

        db_host = influxdb_creds_dict.get("influxdb_test_host")
        db_port = influxdb_creds_dict.get("influxdb_test_port")
        db_user = influxdb_creds_dict.get("influxdb_test_user")
        db_password = influxdb_creds_dict.get("influxdb_test_password")
        db_name = influxdb_creds_dict.get("influxdb_test_name")
        influxdb_values = influxdb_creds_dict.get("influxdb_test_values")
        run = influxdb_creds_dict.get("influxdb_run_value")
        project = influxdb_creds_dict.get("influxdb_project_value")
        version = influxdb_creds_dict.get("influxdb_version_value")

        influxdb_creds_dict.clear()
        influxdb_creds_dict.update(
            dict(db_host=db_host, db_port=db_port, db_user=db_user, db_password=db_password, db_name=db_name,
                 influxdb_values=influxdb_values, run=run, project=project, version=version))

        return influxdb_creds_dict

    def get_results_dict(self, collected_test_results):
        total_passed = len(collected_test_results.get('passed'))
        total_skipped = len(collected_test_results.get('skipped'))
        total_failed = len(collected_test_results.get('failed'))
        total_disabled = len(collected_test_results.get('xfailed')) + total_skipped

        return dict(passed=total_passed, skipped=total_skipped, failed=total_failed,
                    disabled=total_disabled)
