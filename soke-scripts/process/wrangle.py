from process.process import Process
class Wrangle(Process):
    def __init__(self, maps, expected_output_columns_list):
        self.maps=maps
        self.expected_output_columns_list=expected_output_columns_list
    
    def filename(self, in_f):
        ps = in_f.split('/')
        return ps[len(ps)-1]  
    
    def get_dataframe(self):
        return self.dataframe
    
    def set_dataframe(self, dataframe):
        self.dataframe = dataframe