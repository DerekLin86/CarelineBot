import datetime
import shelve
import string
import random

class FormManager:
    def __init__(self, username):
        self.username = username
        self.filename = './travel-form.s'
        self.form_info = {}
        self._time_format = '%Y%m%d%H%M'
        self._form_key_table = {
            'form_id': '{}-{}'.format(self.username, 'id'),
            'create_time': '{}-{}'.format(self, 'createTime'),
        }
        self.__initialize_form_information()

    def __initialize_form_information(self):
        s = shelve.open(self.filename)
        try:
            s[self._form_key_table['form_id']]
        except KeyError:
            s[self._form_key_table['form_id']] = self._get_random_id()
            s[self._form_key_table['create_time']] = self._get_current_time_string()

        try:
            s[self._form_key_table['create_time']]
        except KeyError:
            s[self._form_key_table['create_time']] = self._get_current_time_string()

        self.form_info = {
            'form_id': s[self._form_key_table['form_id']],
            'create_time': s[self._form_key_table['create_time']]
        }

        s.close()

    def get_form_id(self):
        return self.form_info['form_id']

    def get_create_time(self):
        return self.form_info['create_time']

    def _get_random_id(self, stringLength=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    def _get_current_time_string(self):
        return datetime.datetime.now().strftime(self._time_format) 
