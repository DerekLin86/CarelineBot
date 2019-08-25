import shelve

class TravelProgress:
    def __init__(self, username):
        self.username = username
        self.filename = './travel-progress.s'
        self.stages = [
            'destionation',
            'purpose',
            'depart',
            'arrive',
            'packages',
            'clause',
            'confirm',
            'payment',
            'done'
        ]

    def get_current_stage(self):
        s = shelve.open(self.filename)

        try:
            result = s[self.username]
        except KeyError:
            result = self.stages[0]

        s.close()

        return result

    def go_to_next_stage(self, current_stage):
        current_index = self.stages.index(current_stage)
        try:
            self.set_current_stage(self.stages[current_index + 1])
            return True
        except IndexError:
            self.set_current_stage(current_stage)
            return False

    def go_to_previous_stage(self, current_stage):
        current_index = self.stages.index(current_stage)
        try:
            if (current_index > 0):
                self.set_current_stage(self.stages[current_index - 1])
            return True
        except IndexError:
            self.set_current_stage(current_stage)
            return False

    def set_current_stage(self, stage):
        if stage in self.stages:
            s = shelve.open(self.filename)
            s[self.username] = stage
            s.close()
            return True
        else:
            return False
