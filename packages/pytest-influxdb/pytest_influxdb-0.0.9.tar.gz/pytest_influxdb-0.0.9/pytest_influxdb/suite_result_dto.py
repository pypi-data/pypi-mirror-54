import ast
import time

from pytest_influxdb.data_manager import DataManager


class SuiteResultDTO:
    __run = 'UNDEFINED'
    __project = 'UNDEFINED'
    __version = 'UNDEFINED'
    __passed = None
    __failed = None
    __skipped = None
    __duration_sec = 0
    __disabled = 0
    __retries = 0
    __suite_result_dict = {'tags': {}, 'fields': {}}

    def set_run(self, run):
        if run != '':
            self.__run = str(run)

    def set_project(self, project):
        if project != '':
            self.__project = str(project)

    def set_version(self, version):
        if version != '':
            self.__version = str(version)

    def set_passed(self, passed):
        self.__passed = int(passed)

    def set_failed(self, failed):
        self.__failed = int(failed)

    def set_skipped(self, skipped):
        self.__skipped = int(skipped)

    def set_duration_sec(self, duration_sec):
        self.__duration_sec = int(duration_sec)

    def set_disabled(self, disabled):
        self.__disabled = int(disabled)

    def set_retries(self, retries):
        self.__retries = int(retries)

    def set_suite_result_dict(self, suite_result_dict):
        SuiteResultDTO.__suite_result_dict = suite_result_dict

    def get_suite_json(self, measurement_name):
        json_body = [
            {
                "measurement": measurement_name,
                "tags": {
                    "run": self.__run,
                    "project": self.__project,
                    "version": self.__version
                },
                "fields": {
                    "pass": self.__passed,
                    "fail": self.__failed,
                    "skip": self.__skipped,
                    "disabled": self.__disabled,
                    "duration_sec": self.__duration_sec,
                    "retries": self.__retries
                }
            }
        ]

        tags_dict = SuiteResultDTO.__suite_result_dict['tags']
        for key in tags_dict:
            suite_tags = json_body[0]['tags']
            suite_tags.update({key: tags_dict[key]})
        fields_dict = SuiteResultDTO.__suite_result_dict['fields']
        for key in fields_dict:
            suite_fields = json_body[0]['fields']
            suite_fields.update({key: fields_dict[key]})

        return json_body

    def set_tag_values(self, tags_dict):
        suite_tags = SuiteResultDTO.__suite_result_dict
        suite_tags['tags'].update(tags_dict)

    def set_field_values(self, fields_dict):
        suite_fields = SuiteResultDTO.__suite_result_dict
        suite_fields['fields'].update(fields_dict)

    def set_suite_custom_values(self, influxdb_values):
        if influxdb_values and influxdb_values is not '':
            influxdb_values_dict: dict = ast.literal_eval(str(influxdb_values))
            self.set_field_values(influxdb_values_dict['fields']['suite_result'])
            self.set_tag_values(influxdb_values_dict['tags']['suite_result'])

    def get_suite_result_dto(self, terminalreporter, global_values):
        execution_time = round(time.time() - terminalreporter._sessionstarttime)
        suite_results_dict = DataManager().get_results_dict(terminalreporter.stats)

        suite_result_dto = SuiteResultDTO()
        suite_result_dto.set_passed(suite_results_dict.get('passed'))
        suite_result_dto.set_failed(suite_results_dict.get('failed'))
        suite_result_dto.set_skipped(suite_results_dict.get('skipped'))
        suite_result_dto.set_disabled(suite_results_dict.get('disabled'))
        suite_result_dto.set_duration_sec(execution_time)
        suite_result_dto.set_run(global_values.get("run"))
        suite_result_dto.set_project(global_values.get("project"))
        suite_result_dto.set_version(global_values.get("version"))

        return suite_result_dto
