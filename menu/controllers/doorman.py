from pathlib import Path
import os


class DoorMan:
    def __init__(self, username):
        self.username = username
        self.current_status = ''
        self._event_list = ['travel', 'register']
        self._lock_file_mapping_table = {
            'travel': './{}-travel.lock'.format(self.username),
            'register': './{}-register.lock'.format(self.username),
        }

        self._initialize_status()

    def set_lock_file(self, event):
        if not event in self._event_list:
            return False

        if not os.path.isfile(self._lock_file_mapping_table[event]):
            Path(self._lock_file_mapping_table[event]).touch()

        return True

    def remove_lock_file(self, event):
        if not event in self._event_list:
            return False

        if os.path.isfile(self._lock_file_mapping_table[event]):
            os.remove(self._lock_file_mapping_table[event])

        return True

    def _initialize_status(self):
        for event in self._event_list:
            if os.path.isfile(self._lock_file_mapping_table[event]):
                self.current_status = event
                return
        self.current_status = 'idle'

