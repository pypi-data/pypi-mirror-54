import unittest
import os
from datetime import datetime
from ciplog import CipLogNewFormat, LOG_PATH
from ciplog.v2 import NewCipLog


class TestCipLogV2NewLog(unittest.TestCase):

    def setUp(self):

        self._logger = NewCipLog()
        self._file_name_expected = datetime.now().strftime('%d-%m-%Y.log')

        file_path = 'logs/{0}'.format(self._file_name_expected)
        self._logger.warning(code='10', class_name='class_name', method='method', 
                data='data', job_id='10', 
                process_status='process', initial_time='1', finishing_time='2', user='user', path='/path')

        try:
            f = open(file_path)
            if f.readable():
                f.close()
                os.remove(file_path)
        except FileNotFoundError:
            self._logger.debug('file not found!')

    def test_create_a_log_file_with_the_current_date_pattern(self):
        self._logger.warning(code='10', class_name='class_name', method='method', data='data', job_id='10', 
                                process_status='process', initial_time='1', finishing_time='2', user='user', path='/path')
        self._logger.info(class_name='class_name', method='method', data='data', job_id='10', 
                                process_status='process', initial_time='1', finishing_time='2', user='user', path='/path')
        self._logger.error(code='10', class_name='class_name', method='method', data='data', job_id='10', 
                                process_status='process', initial_time='1', finishing_time='2', user='user', path='/path')

        file = self._logger.get_log_files()[0]
        base_name = os.path.basename(file)
        self.assertEqual(self._file_name_expected, base_name)

    
    def test_when_not_set_path(self):
        self.assertEqual(self._logger.path(), LOG_PATH)

    def test_when_set_path(self):
        PATH = os.getcwd()
        self._logger = NewCipLog(log_path=PATH)
        self.assertEqual(self._logger.path(), PATH)

    def test_set_name(self):
        self._logger = NewCipLog(service_name='name_test')
        self.assertEqual(self._logger.service_name_log(), "name_test")

    def test_when_not_set_name(self):
        self._logger = NewCipLog()
        self.assertEqual(self._logger.service_name_log(), "cip_log")

    def test_set_service_version(self):
        os.environ['GIT_TAG'] = "1.0.0"
        self._logger = NewCipLog()
        self.assertEqual(self._logger.service_version_log(), "1.0.0")
        del os.environ['GIT_TAG']

    def test_when_not_set_service_version(self):
        os.environ.unsetenv('GIT_TAG')
        self._logger = NewCipLog()
        self.assertEqual(self._logger.service_version_log(), "0.0.0")

    def tearDown(self):
        self._logger.delete_log_files()


if __name__ == '__main__':
    unittest.main()
