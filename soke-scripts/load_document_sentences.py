from process.load import Load

class LoadDocumentSentences(Load):
    '''
    load sentences from a single file
    * keys for counting document_no, paragraph_no, sentence_no
    * in_folder
    * import_file_list
    '''

    def __init__(self, keys, in_folder, filename):
        Load.__init__(self, settings={'keys': keys, 'in_folder': in_folder, 'file_name': filename})

        # self.filename = filname

        if 'document_no' not in self.get_settings()['keys']:
            self.get_settings()['keys']['document_no'] = 0

        if 'paragraph_no' not in self.get_settings()['keys']:
            self.get_settings()['keys']['paragraph_no'] = 0

        if 'sentence_no' not in self.get_settings()['keys']:
            self.get_settings()['keys']['sentence_no'] = 0

    def get_files(self):
        return self.get_settings()['import_file_list']

    def get_keys(self):
        return self.get_settings()['keys']

    def get_last(self):
        sz = len(self.get_list()) - 1
        return self.get_list()[sz]

    def process(self):
        filename = self.get_settings()['file_name']
        in_folder = self.get_settings()['in_folder']

        # for filename in self.get_files():
        self.get_keys()['document_no'] += 1  # increment document number
        self.get_keys()['paragraph_no'] = 0  # reset paragraphs for document
        self.get_keys()['sentence_no'] = 0  # reset sentence for document
        with open('{}/{}'.format(in_folder, filename), 'r') as document_file:
            # walk the paragraphs
            for paragraph in document_file:
                clean_paragraph = paragraph.replace('\n', '').rstrip().lstrip()

                self.get_keys()['paragraph_no'] += 1
                # bust up the paragraphs
                for sentence in clean_paragraph.split('. '):
                    self.get_keys()['sentence_no'] += 1
                    self.get_list().append({'document_no': self.get_keys()['document_no'],
                                            'paragraph_no': self.get_keys()['paragraph_no'],
                                            'sentence_no': self.get_keys()['sentence_no'],
                                            'text': sentence
                                            }
                                           )
def main():
    from pprint import pprint
    from util import Util
    table_name_key='test_table'
    keys = {}
    in_folder = Util().getInputFolder(table_name_key)
    filename = Util().getOneFile(table_name_key)

    print('in_folder: ', in_folder)
    print('filename:', filename)

    pprint(LoadDocumentSentences(keys, in_folder, filename).run().get_list())

if __name__ == "__main__":
    main()