class Process():
    def __init__(self, settings=None):
        self.dataframe=None
        self.settings=settings
        self.list=[]
        self.dictionary={}



    def getClassName(self):
        return self.__class__.__name__

    def set_dataframe(self, dataframe):
        self.dataframe = dataframe
        return self

    def get_dataframe(self):
        if self.dataframe == None:
            raise Exception('Initialize dataframe in {}'.format(self.getClassName()))
        return self.dataframe

    def set_list(self, list):
        self.list = list
        return self

    def get_list(self):
        if self.list == None:
            raise Exception('Initialize list in {}'.format(self.getClassName()))
        return self.list

    def set_settings(self, settings):
        self.settings = settings
        return self

    def get_settings(self):
        if self.settings == None:
            raise Exception('Initialize settings in {}'.format(self.getClassName()))
        return self.settings

    def process(self):
        raise Exception('Overload process() in {}'.format(self.getClassName())) 
        
    def run(self):
        self.process()
        return self 
    