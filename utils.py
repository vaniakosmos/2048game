from getch import getch


class Logger(object):
    def __init__(self):
        self.logs = []
        self.clean_logs_after_print = True

    def print_logs(self):
        print('Logs:')
        for log in self.logs:
            print('\t' + log)
        if self.clean_logs_after_print:
            self.logs = []

    def add_log(self, thing):
        self.logs.append(thing)


def get_command():
    command = ''
    while command == '':
        try:
            command = getch()
        except OverflowError:
            print('change keyboard layout')
    return command.lower()


def yes_no_prompt():
    print('(y/n)')
    command = ''
    while command not in ('y', 'n'):
        command = get_command().lower()
    return command == 'y'
