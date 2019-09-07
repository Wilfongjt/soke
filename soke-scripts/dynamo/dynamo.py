import boto3
from dynamo.cloud_base import CloudBase

class Dynamo(CloudBase):
    '''
    settings is {
      'db_name': 'dynamodb',
      'region_name': 'us-east-1',
      'endpoint_url': 'http://localhost:8000/',
      'aws_access_key_id': 'anything',
      'aws_secret_access_key': 'anything'
    }
    '''
    def __init__(self, settings=None):
        CloudBase.__init__(self, settings)
        self.client = None
        self.resource = None

    def get_resource(self):
        if self.resource == None:
            raise Exception('Initialize resource in {}'.format(self.getClassName()))
        return self.resource

    def get_client(self):
        if self.client == None:
            raise Exception('Initialize client in {}'.format(self.getClassName()))
        return self.client

    def connect(self):
        print('* Connect to dynamodb')
        DB_NAME = 'dynamodb'

        self.resource = boto3.resource(DB_NAME, **self.get_settings()['access'])

        print('  - remote db connecting...')

        self.client = boto3.client(DB_NAME, **self.get_settings()['access'])

        print('  - connected')
        return self




def main():
    print('fix me')

if __name__ == "__main__":
    main()