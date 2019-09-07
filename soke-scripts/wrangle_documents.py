from process.wrangle import Wrangle
from buffered_writer import BufferedWriter
from util import Util
from load_document_sentences import LoadDocumentSentences
from format_sentence import FormatSentence
from format_search_words import FormatSearchWords

class WrangleDocuments(Wrangle):
    def __init__(self, table_name_key):
        #print('Wrangle Documents')
        self.table_name_key = table_name_key
        self.bufferedWriter = None
        self.set_settings({})

    def set_bufferedwriter(self, buffered_writer):
        self.buffered_writer = buffered_writer
        return self

    def get_bufferedwriter(self):
        return self.buffered_writer

    def process(self):

        Util().removeOutputFiles(self.table_name_key)
        keys = {'document_no': 0,
                'paragraph_no': 0,
                'sentence_no': 0,
                'word_no': 0,
                'word_count': {}
                }

        in_folder = Util().getInputFolder(self.table_name_key)
        import_file_list = Util().getInputFiles(self.table_name_key)

        self.set_bufferedwriter(BufferedWriter(Util().getOutputFolder(self.table_name_key),
                                               '{}.json'.format(self.table_name_key)))
        self.set_settings({
            'table': self.table_name_key,
            'input_folder': in_folder,
            'output_folder': Util().getOutputFolder(self.table_name_key),
            'keys': keys

        })
        for filename in import_file_list:
            title = filename.replace('.txt', '')

            documentSentences = LoadDocumentSentences(keys, in_folder, filename).run()
            self.get_settings()['keys']['word_count']={} # rest word counters
            # keys = {'word_no': 0} # original key are now in sentence
            keys['word_no'] = 0  # reset by document
            for sentence in documentSentences.get_list():
                # print('sentence: ', sentence)
                # print('keys: ', keys)
                formated_sentence = FormatSentence(sentence) \
                    .set_bufferedwriter(self.get_bufferedwriter()) \
                    .run()
                # keys = {'word_no': 0} # reset by sentence

                formated_searchwords = FormatSearchWords(sentence, keys, title) \
                    .set_bufferedwriter(self.get_bufferedwriter()) \
                    .run()

        if self.get_bufferedwriter() != None:
            self.get_bufferedwriter().flush()

def main():
    table_name_key = 'test_table'
    wrangleDocument = WrangleDocuments('test_table').run()
    print('table_name_key: ', table_name_key)

if __name__ == "__main__":
    main()
