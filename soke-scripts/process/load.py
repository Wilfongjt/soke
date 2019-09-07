from process.process import Process
class Load(Process):
    def __init__(self, settings=None):
        Process.__init__(self, settings=settings)
        # import_file_name is  full local file name or url to source
        #self.import_file_list=import_file_list
        #self.dataframe=None
        #self.dictionary={}
        #self.list={}
        #print('Load')

    '''
    def get_dictionary(self):
        return self.dictionary

    def get_dataframe(self):
        return self.dataframe

    def get_list(self):
        return self.list
    '''