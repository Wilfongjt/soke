from process.format import Format

class FormatSentence(Format):
    def __init__(self, sentence):
        Format.__init__(self, sentence, settings=None)
        # sentence is {'document_no': 1, 'paragraph_no': 2, 'sentence_no': 2, 'text': 'Updated on March 6, 2019'}
        self.sentence = sentence



    def process(self):
        document_id = 'd#{:03d}'.format(self.sentence['document_no'])
        sentence_id = 's#{:05d}#{:06d}'.format(self.sentence['paragraph_no'], self.sentence['sentence_no'])

        item = {'pk': document_id,
                'sk': sentence_id,
                'data': self.spacify(self.sentence['text']),
                'type': 'SENTENCE'
                }
        # item = self.typifyItem(item)
        item = {'PutRequest': {'Item': item}}

        self.get_list().append(item)

        if self.get_bufferedwriter() != None:
            self.get_bufferedwriter().write(item)


def main():
    from pprint import pprint
    sentence = {'document_no': 1, 'paragraph_no': 2, 'sentence_no': 2, 'text': 'Updated on March 6, 2019'}

    pprint(FormatSentence(sentence).run().get_list())

if __name__ == "__main__":
    main()