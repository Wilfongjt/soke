print('Drop DynamoDb Table')

import os

from util import Util
from dynamo.dynamo_remote import DynamoRemote

from pprint import pprint
import time
Util().loadEnv()
delay_time = 60
# environment variables
print('* Verify inputs')
print('  - type x to terminate')

# give admin a chance to review or terminate
# type x q e to terminate the getInput
MY_GIT_PROJECT= Util().getInput('  - MY_GIT_PROJECT', os.environ['MY_GIT_PROJECT'].strip())
MY_STAGE = Util().getInput('  - MY_STAGE', os.environ['MY_STAGE'].strip())
MY_TABLE_NAME_KEY = Util().getInput('  - MY_TABLE_NAME_KEY', '{}_{}'.format(MY_GIT_PROJECT, MY_STAGE))
# MY_TABLE_NAME_KEY = Util().getInput('  - MY_TABLE_NAME_KEY', os.environ['MY_TABLE_NAME_KEY'].strip())
areYouSure = Util().getInput('  - Are you sure?', 'N')

if areYouSure != 'y' and areYouSure != 'Y':
    print('terminated')
    exit(0)

access = {
    'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID'].strip(),
    'aws_secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY'].strip(),
    'region_name': os.environ['REGION_NAME'].strip()
}
template_values = {
    'table_name': MY_TABLE_NAME_KEY,
    'index_name': 'gsi_{}_sk_data_{}'.format(MY_GIT_PROJECT, MY_STAGE)
}

# dynamo = DynamoRemote(settings=settings).loadTableDefinition().connect()
dynamo = DynamoRemote(access)\
    .connect()\
    .set_table_name(MY_TABLE_NAME_KEY)\
    .set_template_values(template_values)\
    .load_table_definition()\
    .drop_table()\
    .create_table()

pprint(dynamo.get_settings())
print('  - ', 'Tables may take longer than {} to delete or create.'.format(delay_time))

print('Drop DynamoDb Table Complete')