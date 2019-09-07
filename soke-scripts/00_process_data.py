print('Process Data')
#from dotenv import load_dotenv
#load_dotenv()
import os
from pprint import pprint
from util import Util
from wrangle_documents import WrangleDocuments

Util().loadEnv()

# environment variables
#table_name_key = os.environ['MY_TABLE_NAME_KEY'].strip()
#stage = os.environ['MY_STAGE'].strip()

# give admin a chance to review or terminate
# type x q e to terminate the getInput
#MY_TABLE_NAME_KEY = Util().getInput("MY_TABLE_NAME_KEY", table_name_key)
#MY_STAGE = Util().getInput('MY_STAGE', stage)

MY_GIT_PROJECT= Util().getInput('  - MY_GIT_PROJECT', os.environ['MY_GIT_PROJECT'].strip())
MY_STAGE = Util().getInput('  - MY_STAGE', os.environ['MY_STAGE'].strip())
MY_TABLE_NAME_KEY = Util().getInput('  - MY_TABLE_NAME_KEY', '{}_{}'.format(MY_GIT_PROJECT, MY_STAGE))




print(' Input: ', Util().getInputFolder(MY_TABLE_NAME_KEY))
print('Output: ', Util().getOutputFolder(MY_TABLE_NAME_KEY))

process_config = {
                  'key': MY_TABLE_NAME_KEY,
                  'stage': MY_STAGE,
                }

wrangleDocuments = WrangleDocuments(process_config['key']).run()
# wrangleDocuments.settings()['keys']['word_count']={} # remove the word counters
wrangleDocuments.get_settings()['keys']['word_count']={}
pprint(wrangleDocuments.get_settings())
print('Process Data Complete')