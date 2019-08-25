class CarelineMenuManager:
    def parse_command(self):
        return self.get_menu_content()

    def get_menu_content(self):
        return "CareLine Chatbot Usage: \n"

class CarelineCommandParser:
    def __init__(self, message):
        self.current_command = ''
        self.command_content = ''
        self.command_list = [
            'new user',
            'account',
            'travel',
            'register off',
            'register on',
            'register status'
        ]
        self.message = message.lower()

        self.__parse_message()

    def get_match_command(self):
        return self.current_command

    def get_match_content(self):
        return self.command_content

    def __parse_message(self):
        for i in self.command_list:
            result =  self.message.split(i)
            if result[0] != self.message:
                self.current_command = i
                try:
                    self.command_content = str(result[1]).strip()
                except IndexError:
                    self.command_content = ''
                break
            else:
                continue

        return True
