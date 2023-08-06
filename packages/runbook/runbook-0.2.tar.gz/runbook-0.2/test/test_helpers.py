import sys
import tempfile
from io import StringIO
from threading import Thread
from time import sleep


class CustomIO(StringIO):
    
    def __init__(self, outstream):
        super().__init__()
        self._outstream = outstream
    
    def write(self, *args):
        self._outstream.write(*args)
        super().write(*args)


def get_temp_dir():
    return tempfile.TemporaryDirectory()
    
    
def capture_output(fn, inputs=[]):
    custom_stdin = None
    custom_stdout = None
        
    def responder_fn():
        sleep(3)
        for input in inputs:
            custom_stdin.write(input+"\n")
            custom_stdin.seek(0)
            # self.stdin.truncate(0)
            # self.stdin.write('yes\n')
            # custom_stdin.seek(0)
            
            # sys.stdin.truncate(0)
            # sys.stdin.write(input+'\n')
            # sys.stdin.seek(0)
            sleep(3)

    responder = Thread(target=responder_fn)

    old_stdin = sys.stdin
    sys.stdin = custom_stdin = StringIO()
    
    old_stdout = sys.stdout
    sys.stdout = custom_out = CustomIO(old_stdout)

    try:
        responder.start()
        return fn(), custom_out.value()
    finally:
        sys.stdout = old_stdout