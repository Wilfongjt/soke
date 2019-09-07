from process.data import Data

class Format(Data):
    def __init__(self, sentence, settings=None):
        Data.__init__(self, sentence, settings)
        # sentence is {'document_no': 1, 'paragraph_no': 2, 'sentence_no': 2, 'text': 'Updated on March 6, 2019'}
        self.buffered_writer = None

    def set_bufferedwriter(self, buffered_writer):
        self.buffered_writer = buffered_writer
        return self

    def get_bufferedwriter(self):
        return self.buffered_writer

    def spacify(self, text):
        if len(text.strip()) == 0:
            # print('<space>')
            return '<space>'
        return text