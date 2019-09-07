from process.process import Process
class Output(Process):
    def __init__(self, settings):
        Process.__init__(self, settings=settings)

        self.buffered_writer=None

    def set_bufferedwriter(self, buffered_writer):
        self.buffered_writer = buffered_writer
        return self

    def get_bufferedwriter(self):
        return self.buffered_writer