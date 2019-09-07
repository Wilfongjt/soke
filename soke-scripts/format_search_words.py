from process.format import Format

class FormatSearchWords(Format):
    def __init__(self, sentence, keys, title):
        Format.__init__(self, sentence, settings={'keys': keys, 'title': title})
        # sentence is {'document_no': 1, 'paragraph_no': 2, 'sentence_no': 2, 'text': 'Updated on March 6, 2019'}
        self.sentence = sentence

    def process(self):
        sentence = self.get_data()

        document_id = 'd#{:03d}'.format(sentence['document_no']) # id the document
        # sentence_id = 's-{:05d}-{:06d}'.format(sentence['paragraph_no'], sentence['sentence_no'])
        #doc_word_count = {} # holds the count of each word in the document use for creating id
        # unique within a sentence
        uniqueList = set(self.spacifyPuncuation(sentence['text'].lower()).split())
        # words are no longer in sentence order
        for word in uniqueList:
            self.get_settings()['keys']['word_no'] += 1
            if word in self.get_settings()['keys']['word_count']:
                self.get_settings()['keys']['word_count'][word]+=1
            else:
                self.get_settings()['keys']['word_count'][word]=1

            # print('word: ', word)
            # word count gets reset to zero for every doc

            #word_unique_id = '{}#{}'.format(word, self.get_settings()['keys']['word_no'])

            word_unique_doc_id = '{}#{}'.format(word, self.get_settings()['keys']['word_count'][word])

            item = {'pk': document_id,
                    'sk': word_unique_doc_id,
                    'data': self.spacify(sentence['text']), # spaces are bad
                    'title': self.get_settings()['title'],
                    'type': 'SEARCH-WORD'
                    }
            #item = self.typifyItem(item)
            item = {'PutRequest': {'Item': item}}

            self.get_list().append(item)  # use for testing

            if self.get_bufferedwriter() != None:
                self.get_bufferedwriter().write(item)


def main():
    from pprint import pprint
    sentence = {'document_no': 1, 'paragraph_no': 2, 'sentence_no': 2, 'text': 'Updated on March 6, 2019'}
    keys = {'word_no': 0}
    title = 'Some title.txt'.replace('.txt', '')
    pprint(FormatSearchWords(sentence, keys, title).run().get_list())

if __name__ == "__main__":
    main()