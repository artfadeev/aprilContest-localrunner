from subprocess import PIPE, Popen

class Connector():
    def __init__(self, command):
        self.process = Popen(command, stdin=PIPE, stdout=PIPE)

    def write(self, message):
        try:
            message = '{}\n'.format(message).encode()
            self.process.stdin.write(message)
            self.process.stdin.flush()
            return {'ok': True}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def read(self):
        try:
            message = self.process.stdout.readline().decode('utf-8')
            return {'ok': True, 'message': message}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def close(self):
        self.process.terminate()
        self.process.kill()
