from process.process import Process
import json

class Data(Process):

    '''
    provides interface to file holding data
    provides some utility data processing functions
    '''
    def __init__(self, data, settings=None ):
        Process.__init__(self, settings=settings )
        self.data = data

    def get_data(self):
        return self.data

    def spacifyPuncuation(self, line):
        # add spaces around puncuation
        line = line.replace(':',' : ')
        line = line.replace('.',' . ')
        line = line.replace('*',' * ')
        line = line.replace('?',' ? ')
        line = line.replace('(',' ( ')
        line = line.replace(')',' ) ')
        line = line.replace('[',' [ ')
        line = line.replace(']',' ] ')
        line = line.replace('{',' { ')
        line = line.replace('}',' } ')
        line = line.replace(',',' , ')
        line = line.replace('\'',' \' ')
        line = line.replace('’',' \' ')
        line = line.replace('"',' " ')
        line = line.replace('”',' " ') # yes this is a duplicate, leave
        line = line.replace('“',' " ') # yes this is a duplicate, leave
        line = line.replace('/',' / ')
        line = line.replace('\\',' \\ ') # doesnt work
        return line

    def typifyItem(self, item):
        '''
        write data for awe batch loader
        dont use with boto3 table.batch_writer
        '''
        typedItem = {}
        keys = item.keys()
        # print('keys: ', keys)
        for k in keys:
            typ = type(item[k])
            isStr = isinstance(item[k], str)
            if isStr:
                typedItem[k] = {"S": item[k]}
            else:
                isInt = isinstance(item[k], int)
                if isInt:
                    typedItem[k] = {"N": str(item[k])}

                    # print('typedItem: ', typedItem )
        return typedItem