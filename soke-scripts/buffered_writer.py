import json

class BufferedWriter:
    '''
    write a aws compatiable json object to a series files

    '''
    def __init__(self, out_folder, out_name, table_name_key=None, ext='.json' ,count_limit=25):
        # out_folder is /a/b 
        # out_name is with extention 'somefile.json' 
        # ext='.json' 
        # count_limit=25 
        self.folder = out_folder # no slash at end
        self.out_file_name = out_name
        #self.root_name = out_name # include extention
        if table_name_key == None:
            self.table_name_key = out_name.replace(ext,'') # remove extention assume filename is table name
        else:
            self.table_name_key = table_name_key
            
        self.buffer = [] 
        self.file_count = 0
        self.limit = count_limit
        # self.item_count = 0
        # self.word_counts = {} # dict of words with a counter {'the' : 1, 'data': 2}
        #print('BufferedWriter init', self.state())
    
    def formatOutFileName(self):
        #print('folder: ', self.folder, ' file_count: ', self.file_count, ' out_file_name: ', self.out_file_name)
        #print('buffer: ', '{}/{}.{}'.format(self.folder, self.file_count, self.out_file_name) )
        return '{}/{}.{}'.format(self.folder, self.file_count, self.out_file_name)

    def state(self):
        return {'file_count': self.file_count,
                'limit': self.limit,
                # 'item_count': self.item_count,
                # 'word_counts': self.word_counts,
                'buffer_count': len(self.buffer)
                }
    def write(self, item):
        # print('BufferedWriter.write ', self.state())
        self.buffer.append(item)
            
        if len(self.buffer) >= self.limit:
            #print('BufferedWriter.write ', self.state())
            # with open('{}/{}.{}'.format(self.folder, self.file_count, self.root_name), 'w') as f:
            with open(self.formatOutFileName(), 'w') as f:    
                # recode the key with the id before writing
                #final = {'documents': self.buffer}
                final = {self.table_name_key: self.buffer}
                f.write(json.dumps(final))
                #f.write(json.dumps(self.buffer))
                self.file_count += 1
                self.buffer=[]

    def flushReset(self):
        if len(self.buffer) > 0:
            # with open('{}/{}.{}'.format(self.folder, self.file_count, self.root_name), 'w') as f:
            with open(self.formatOutFileName(), 'w') as f:
                # recode the key with the id before writing
                # final = {'documents': self.buffer}
                # final = {self.root_name: self.buffer}

                final = {self.table_name_key: self.buffer}
                f.write(json.dumps(final))
                # f.write(json.dumps(self.buffer))
                self.file_count = 0

                self.buffer = []
    def flush(self):
        if len(self.buffer) > 0:
            
            #with open('{}/{}.{}'.format(self.folder, self.file_count, self.root_name), 'w') as f:
            with open(self.formatOutFileName(), 'w') as f:     
                # recode the key with the id before writing
                #final = {'documents': self.buffer}
                #final = {self.root_name: self.buffer}
                
                final = {self.table_name_key: self.buffer}
                f.write(json.dumps(final))
                # f.write(json.dumps(self.buffer))
                self.file_count += 1
                
                self.buffer=[]

def main():
    from util import Util

    util = Util()

    sentence='This FAQs has been drafted by the Department of Licensing and Regulatory Affairs (LARA) and the Michigan Department of Health and Human Services (DHHS) to provide some clarification to help with implementation of the Michigan Opioid Laws.'
    #          'The answers to the frequently asked questions are not to be considered as legal advice.'
    table_name_key="test_table"
    bufferedWriter = BufferedWriter(util.getOutputFolder(table_name_key),
                                         '{}.json'.format(table_name_key))

    doc_id = 1

    r = range(51)
    dict = {
        'documents': {},
        'paragraphs': {},
        'words': {},
        'word-documents': {}
        }
    for i in r:
        #print(i)
        doc_id = 'doc-{}'.format(i)
        if doc_id not in dict['documents']:
            item = {'pk': doc_id,
                    'sk': 'DOCUMENT',
                    'data': sentence,
                    'type': 'DOC'
                    }

            dict['documents'][doc_id] = item
            #item = self.typifyItem(item)
            item = {'PutRequest': {'Item': item}}
            bufferedWriter.write(item)
    print(bufferedWriter.state())
    bufferedWriter.flush()
    print(bufferedWriter.state())


if __name__ == "__main__":
    main()