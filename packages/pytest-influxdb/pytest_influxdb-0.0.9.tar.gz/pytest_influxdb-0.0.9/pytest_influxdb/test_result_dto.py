import ast


class TestResultDTO:
    __run = 'UNDEFINED'
    __test = None
    __status = 'disabled'
    __project = 'UNDEFINED'
    __version = 'UNDEFINED'
    __screenshot = None
    __duration_sec = None
    __exception = None
    __merged = None
    __test_result_tag_dict = {}
    __test_result_field_dict = {}

    def set_run(self, run):
        if run != '':
            self.__run = str(run)

    def get_test(self):
        return self.__test

    def set_test(self, test):
        self.__test = str(test)

    def set_status(self, status):
        self.__status = str(status)

    def set_project(self, project):
        if project != '':
            self.__project = str(project)

    def set_version(self, version):
        if version != '':
            self.__version = str(version)

    def set_screenshot(self, screenshot):
        self.__screenshot = str(screenshot)

    def set_duration_sec(self, duration_sec):
        self.__duration_sec = int(duration_sec)

    def set_exception(self, exception):
        self.__exception = str(exception)

    def set_merged(self, is_merged):
        self.__merged = str(is_merged)

    def set_test_result_tag_dict(self, test_result_tag_dict):
        TestResultDTO.__test_result_tag_dict = test_result_tag_dict

    def set_test_result_field_dict(self, test_result_field_dict):
        TestResultDTO.__test_result_field_dict = test_result_field_dict

    def get_test_json(self, measurement_name):
        json_body = [
            {
                "measurement": measurement_name,
                "tags": {
                    "test": self.__test,
                    "run": self.__run,
                    "project": self.__project,
                    "version": self.__version
                },
                "fields": {
                    "status": self.__status,
                    "screenshot": self.__screenshot,
                    "duration_sec": self.__duration_sec,
                    "exception": self.__exception,
                    "merged": self.__merged
                }
            }
        ]
        tags_dict_for_all_tests = TestResultDTO.__test_result_tag_dict
        tags_dict_for_current_test = tags_dict_for_all_tests.get(str(self.get_test()))
        if tags_dict_for_current_test:
            for key in tags_dict_for_current_test:
                json_body[0]['tags'].update({key: tags_dict_for_current_test[key]})
        fields_dict_for_all_tests = TestResultDTO.__test_result_field_dict
        fields_dict_for_current_test = fields_dict_for_all_tests.get(str(self.get_test()))
        if fields_dict_for_current_test:
            for key in fields_dict_for_current_test:
                json_body[0]['fields'].update({key: fields_dict_for_current_test[key]})
        return json_body

    def get_test_json_for_suite_level(self):
        json_body = {
            "test": self.__test,
            "status": self.__status,
            "duration_sec": self.__duration_sec,
            "run": self.__run,
            "project": self.__project,
            "version": self.__version
        }

        return json_body

    def parse_json_to_test_result_dto(self, json_test_result_dto):
        if json_test_result_dto.endswith('\n'):
            json_test_result_dto = json_test_result_dto[:-1]
        json_test_result_dto = ast.literal_eval(json_test_result_dto)
        test_result_dto = TestResultDTO()
        test_result_dto.set_test(json_test_result_dto['test'])
        test_result_dto.set_status(json_test_result_dto['status'])
        test_result_dto.set_duration_sec(json_test_result_dto['duration_sec'])
        test_result_dto.set_run(json_test_result_dto['run'])
        test_result_dto.set_project(json_test_result_dto['project'])
        test_result_dto.set_version(json_test_result_dto['version'])

        return test_result_dto

    def set_tag_values(self, item_nodeid, tags_dict):
        main_dict = TestResultDTO.__test_result_tag_dict
        if item_nodeid in main_dict:
            main_dict[item_nodeid].update(tags_dict)
        else:
            main_dict.update({item_nodeid: tags_dict})

    def set_field_values(self, item_nodeid, fields_dict):
        main_dict = TestResultDTO.__test_result_field_dict
        if item_nodeid in main_dict:
            main_dict[item_nodeid].update(fields_dict)
        else:
            main_dict.update({item_nodeid: fields_dict})

    def set_test_result_data(self, project_name, release_version, run_id_value, report_outcome,
                             merged):
        self.set_project(project_name)
        self.set_version(release_version)
        self.set_run(run_id_value)
        self.set_duration_sec(report_outcome.duration)
        self.set_status(report_outcome.outcome)
        self.set_merged(merged)

    def collect_custom_values(self, influxdb_values):
        custom_values = influxdb_values
        if custom_values and custom_values is not '':
            influxdb_values_dict: dict = ast.literal_eval(str(custom_values))
            self.set_field_values(self.get_test(), influxdb_values_dict['fields']['test_result'])
            self.set_tag_values(self.get_test(), influxdb_values_dict['tags']['test_result'])

    def collect_user_properties(self, request):
        user_properties_tuple = request.node.user_properties
        for var in user_properties_tuple:
            if isinstance(var, dict):
                self.set_field_values(self.get_test(), var)
