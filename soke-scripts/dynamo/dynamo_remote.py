import boto3
import json
import time
from dynamo.dynamo import Dynamo

class DynamoRemote(Dynamo):
    '''
    settings is {
      'db_name': 'dynamodb',
      'region_name': 'us-east-1',
      'aws_access_key_id': 'anything',
      'aws_secret_access_key': 'anything'
    }
    '''
    def __init__(self, access):
        Dynamo.__init__(self, settings={'access': access})
        self.table_definition =  None
        self.table_name = None
        self.delay_time = 60
        self.input_files = None





    def set_table_name(self, table_name):
        self.table_name = table_name
        return self

    def get_table_name(self):
        return self.table_name

    def set_template_values(self, template_values):
        self.get_settings()['template_values'] = template_values
        return self

    def load_table_definition(self, table_histories_file_name='table.template.json'):
        print('* Load table template')
        self.table_histories = {}
        with open(table_histories_file_name) as json_file:
            self.table_histories = json.load(json_file)

        for tmplt in self.table_histories:
            if tmplt == 'template':
                print('  - set template: ', tmplt)
                self.table_definition = self.table_histories[tmplt]

        if self.table_definition == None:
            raise Exception('Table Definition not set in {}'.format(self.getClassName()))

        return self

    def get_table_definition(self):

        self.table_definition['TableName']=self.get_settings()['template_values']['table_name']
        self.table_definition['GlobalSecondaryIndexes'][0]['IndexName'] = self.get_settings()['template_values']['index_name']

        return self.table_definition

    def get_table_list(self):
        '''
        returns list of table names
        '''

        responce = self.client.list_tables()
        table_name_list = responce['TableNames']

        return table_name_list

    def drop_table(self):
        print('* Drop Table')

        table_name = self.get_table_name()

        try:
            # table_list = self.get_table_list()
            self.get_settings()['begin_table_list'] = self.get_table_list()
            if self.get_table_name() in self.get_settings()['begin_table_list']:
                print(' - dropping: {}'.format(self.get_table_name()))
                print('  - deleting {}'.format(self.get_table_name()))
                table = self.get_resource().Table(self.get_table_name())
                table.delete()
                print("  - table deleted")
                print('  - wait {} seconds to complete delete of {}'.format(self.delay_time, self.get_table_name()))
                time.sleep(self.delay_time)
                self.get_settings()['table_list'] = self.get_table_list()
            else:
                print('  - table not found {}'.format(self.get_table_name()))

        except NameError:

            print('!!!!!!!!!!! delete failed for {}'.format(table_name))
            print(' you should delete manually')

        return self

    def create_table(self):
        print('* Create Table')
        table_list = self.get_table_list()
        if self.get_table_name() not in table_list:
            print('  - creating table {}'.format(self.get_table_name()))
            self.get_client().create_table(**self.get_table_definition())
            print('  - wait {} seconds before using {}'.format(self.delay_time, self.get_table_name()))
            time.sleep(self.delay_time)
            self.get_settings()['ending_table_list'] = self.get_table_list()
        else:
            print('  - cannot overwrite exiting table {}'.format(self.get_table_name()))

        return self



def main():
    print('fix me')

if __name__ == "__main__":
    main()