from process.process import Process
import numpy as np 

class Condense(Process):
    def __init__(self, dataframe, expected_output_columns_list, extraColumns, outlier_settings):
        '''
        dataframe is a pandas dataframe with pre-cleaned data
        expected_output_columns_list is list of outupt column names
        extraColumns is a list of temporary column that get removee later
        outlier_settings is dictionary of preconfigured outlier definitions
        '''        
        self.dataframe = dataframe
        self.expected_output_columns_list=expected_output_columns_list
        self.extraColumns = extraColumns
        self.outlier_settings = outlier_settings
        #print('Condense A', self.get_dataframe()['dr_discharge'])  


        
    def validateColumns(self):  
        print(' - validate columns')
        '''
        check 's column name for the expected colnames
        '''
        for nm in self.expected_output_columns_list:
            if not nm in self.get_dataframe().columns.values:
                raise Exception('{} is missing from '.format(get_dataframe().format(nm)) )
                
    def removeExtraColumns(self):
        print(' - Remove extra columns')
        for colname in self.extraColumns:
            if( colname in self.get_dataframe().columns.values):
                print(' -- drop column: ',colname)
                self.set_dataframe(self.get_dataframe().drop([colname], axis=1))
                
    def remove_obvious_outliers(self):
        print(' - remove outliers')
        '''
        remove individual observations
        remove range of observation
        _outliers is 
        {
          'outliers': [
            {'column':'scheduled_day',
             'range':(pd.to_datetime('2016-01-01'), pd.to_datetime('2017-01-01')),
             'reason':'Remove 2015. Appointment in 2015 has many gaps in the timeline numbers'},
            {'column': 'scheduled_day_of_week',
             'range': (0,4) ,
             'reason':'Remove Saturday and Sunday visits. These are so few that they could easily .'},
            {'column':'lon',
             'range':(-50.0,-35.0),
             'reason':'Remove neighbourhoods that have bad longitudes (too far east).'},
            {'column':'scheduled_hour',
             'range':(7,20),
             'reason':'Remove small number of observations at 6:00 and 21:00 hours.'}
          ]
        }

        '''
        
        for outlier in self.outlier_settings['outliers']:
            # pprint(outlier)
            col_name = outlier['column']

            if 'range' in outlier:

                low = outlier['range'][0]
                high = outlier['range'][1]
                sz = len(self.get_dataframe())

                tmp = None
                tmp1 = ''

                if isinstance(low, np.datetime64):
                    self.set_dataframe(
                      self.get_dataframe()[(self.get_dataframe()[col_name].to_datetime() >= low) & (self.get_dataframe()[col_name].to_datetime() <= high)]
                    )
                else:   
                    self.set_dataframe(
                        self.get_dataframe()[(self.get_dataframe()[col_name] >= low) & (self.get_dataframe()[col_name] <= high)]
                    )
                outlier["count"] = sz - len(self.get_dataframe())

            elif 'categories' in outlier:
                _list = outlier['categories']
                sz = len(self.get_dataframe())
                self.set_dataframe(
                    self.get_dataframe()[self.get_dataframe()[col_name].isin(_list)]
                )
                outlier["count"] = sz - len(self.get_dataframe())
            if "reason" in outlier:
                outlier["reason"] = outlier["reason"].format(  str(outlier["count"]) )


    def remove_duplicates(self):
        print(' - drop duplicates')
        # self.set_dataframe(self.get_dataframe().drop_duplicates(primary_key,keep='first'))
    
    def get_dataframe(self):
        return self.dataframe
    
    def set_dataframe(self, dataframe):
        self.dataframe = dataframe    
    '''
    def process(self):
        print('* Condense')
        #self.removeExtraColumns()
        #self.validateColumns()
        #self.remove_obvious_outliers()
        #self.remove_duplicates()
        ##self.set_dataframe()
        ##print('Condense B', self.get_dataframe()['dr_discharge'])  
    ''' 