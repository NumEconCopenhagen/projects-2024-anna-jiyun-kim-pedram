import pandas as pd
from dstapi import DstApi
def keep_regs(df, regs):
    """ Example function. Keep only the subset regs of regions in data.

    Args:
        df (pd.DataFrame): pandas dataframe 

    Returns:
        df (pd.DataFrame): pandas dataframe

    """ 
    
    for r in regs:
        I = df.reg.str.contains(r)
        df = df.loc[I == False] # keep everything else
    
    return df

#define the table for HFUD11 below 

def HFUD11_data():
    ind = DstApi('HFUDD11')

   
    # The _define_base_params -method gives us a nice template (selects all available data)
    params = ind._define_base_params(language='en')
    params

    variables = params['variables'] # Returns a view, that we can edit
    #We are only looking at people from Copenhagen, Thisted and Aalborg
    variables[0]["values"] = ["101","787", "851"]
    #We don't write anything to variables[1], and therefore, we are looking at people across all "Herkomst"
    variables[1]["values"] = ["TOT"]
    #We are looking at, how many people have a bachelor degree
    variables[2]['values'] =['H60']
    #We don't look at people with a specific age. But only at Age,total. 
    variables[3]["values"] = ["TOT"]
    #We are only looking at people with the gender male and female
    variables[4]['values'] = ["TOT"]
    #We don't write anything for variables[5], and therefore, we are looking at people across all dates from 2008 to 2022.
    params

    #Use the variables set above
    ind_api = ind.get_data(params=params)

    #Sort values for BOPOMR, HFDD, KØN and TID
    ind_api.sort_values(by=['BOPOMR', 'HFUDD', "KØN", "TID"], inplace=True)
    ind_api.head(5)

    # d. drop the columns "HERKOMST"
    for v in ['HERKOMST']: 
        del ind_api[v]


    #e. rename the columns
    ind_api = ind_api.rename(columns = {'INDHOLD':'population w. BA', 'BOPOMR': 'municipality', "ALDER":"age", "KØN": "gender", "TID" :"year"})

    # f. drop non-municipality
    for val in ['Region', 'All']: 
        I = ind_api['municipality'].str.contains(val)
        ind_api.drop(ind_api[I].index, inplace=True)


    # f. convert to date
    del ind_api["age"]
    del ind_api["HFUDD"]
    del ind_api["gender"]
    return ind_api



