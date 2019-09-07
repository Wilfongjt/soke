from process.process import Process
class Clean(Process):
    def __init__(self, df_source, commonNameMap, region_map):
        self.dataframe = df_source
        self.commonNameMap = commonNameMap
        self.region_map=region_map