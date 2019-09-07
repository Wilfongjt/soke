from process.load import Load
from dynamo.dynamo_remote import DynamoRemote
from util import Util
import json
import logging
import sys

class LoadTable(Load):
    '''
    load sentences from a single file
    * keys for counting document_no, paragraph_no, sentence_no
    * in_folder
    * import_file_list
    '''

    def __init__(self, table_name_key, access=None):
        Load.__init__(self, settings={'table_name_key': table_name_key, 'access': access})
        self.delay_time = 60

    def set_input_files(self, input_files):
        self.input_files = input_files
        return self

    def get_input_files(self):
        return self.input_files



    def process(self):
        print('load_table')
        self.get_settings()['process'] = {}
        #print('load_tables: ', self.get_input_files())
        MY_TABLE_NAME_KEY = self.get_settings()['table_name_key']
        dynamo = DynamoRemote(self.get_settings()['access']) \
            .connect()

        table = dynamo.get_resource().Table(MY_TABLE_NAME_KEY)

        input_files = Util().getOutputFiles(MY_TABLE_NAME_KEY, ext='json')
        input_folder = Util().getOutputFolder(MY_TABLE_NAME_KEY)
        print('folder: ', input_folder)
        self.get_settings()['process']['input_folder'] = input_folder
        self.get_settings()['process']['table'] = self.get_settings()['table_name_key']
        self.get_settings()['files']=0
        self.get_settings()['items']=0
        #self.get_settings()['begining_items'] = table.item_count
        with table.batch_writer() as batch:
            for input_file in input_files:
                self.get_settings()['files'] += 1
                with open('{}/{}'.format(input_folder, input_file)) as json_file:
                    table_data = json.load(json_file)

                    for table_name in table_data:
                        print(input_file, table_name)

                        for put_request in table_data[table_name]:
                            #print('put_request: ', put_request)
                            #print('item: ', put_request['PutRequest']['Item'])
                            try:
                                self.get_settings()['items'] += 1
                                batch.put_item(Item=put_request['PutRequest']['Item'])

                            except:
                                e = sys.exc_info()[0]
                                print('Unknown exception {}'.format(e))
                                # logging.basicConfig(filename='load.log', level=logging.ERROR).error('Unknown {} in {}'.format(e, self.getClassName()))
        print('  - wait {} seconds before using {}'.format(self.delay_time, MY_TABLE_NAME_KEY))

        self.get_settings()['ending_items'] = table.item_count

def main():
    print('define main')

if __name__ == "__main__":
    main()