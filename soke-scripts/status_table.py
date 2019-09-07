from process.load import Load
from dynamo.dynamo_remote import DynamoRemote
from util import Util
import json
import logging
import sys

class StatusTable(Load):
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

        self.get_settings()['items'] = table.item_count


def main():
    print('define main')

if __name__ == "__main__":
    main()