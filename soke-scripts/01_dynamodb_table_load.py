print('Drop Dynamod Table')

import os

from util import Util
#from dynamo.dynamo_remote import DynamoRemote
from load_table import LoadTable

from pprint import pprint
import time
Util().loadEnv()
delay_time = 60
# environment variables
print('* Verify inputs')
print('  - type x to terminate')

# give admin a chance to review or terminate
# type x q e to terminate the getInput
#MY_TABLE_NAME_KEY = Util().getInput('  - MY_TABLE_NAME_KEY', os.environ['MY_TABLE_NAME_KEY'].strip())
#MY_STAGE = Util().getInput('  - MY_STAGE', os.environ['MY_STAGE'].strip())


MY_GIT_PROJECT= Util().getInput('  - MY_GIT_PROJECT', os.environ['MY_GIT_PROJECT'].strip())
MY_STAGE = Util().getInput('  - MY_STAGE', os.environ['MY_STAGE'].strip())
MY_TABLE_NAME_KEY = Util().getInput('  - MY_TABLE_NAME_KEY', '{}_{}'.format(MY_GIT_PROJECT, MY_STAGE))


access = {
    'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID'].strip(),
    'aws_secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY'].strip(),
    'region_name': os.environ['REGION_NAME'].strip()
}

loadTable = LoadTable(MY_TABLE_NAME_KEY, access=access).run()
pprint(loadTable.get_settings())

print('Drop Dynamod Table Complete')
