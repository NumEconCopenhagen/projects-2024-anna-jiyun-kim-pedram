import pandas as pd
from dstapi import DstApi
import matplotlib.pyplot as plt
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

#define the table for INDKP106

def dkp_data():
    dkp = DstApi('INDKP106')

    tabsum = dkp.tablesummary(language='en')

    # The _define_base_params -method gives us a nice template (selects all available data)
    params = dkp._define_base_params(language='en')

    variables = params['variables'] # Returns a view, that we can edit
    #We are only looking at people from Copenhagen, Thisted and Aalborg and choosing average wage in dkk
    variables[0]["values"] = ["101","787", "851"]
    variables[1]['values'] = ["118"]
    #We are looking at all ages and genders
    variables[2]['values'] =["MOK"]
    variables[3]["values"] = ["00"]
    #We are looking at all income intervals and years 2008-2022
    variables[4]['values'] = ["000"]
    variables[5]['values']= ['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']

    params

    dkp_api = dkp.get_data(params=params)
    dkp_api.head(5)

    dkp_api.sort_values(by=["OMRÅDE", 'ENHED', "KOEN", 'ALDER1',"INDKINTB", "TID", "INDHOLD"], inplace=True)
    dkp_api.head(5)

    #change names
    dkp_api = dkp_api.rename(columns = {"OMRÅDE":"municipality", "ENHED":"Avg. in DKK", "KOEN":"Gender", "ALDER1":"age", "INDKINTB":"Income Interval", "TID":"year", "INDHOLD":"AVG. Income"})

    # e. drop non-municipalities
    for val in ['Region', 'All']: 
        I = dkp_api['municipality'].str.contains(val)
        dkp_api.drop(dkp_api[I].index, inplace=True)

    # f. convert to date
    dkp_api['date'] = pd.PeriodIndex(dkp_api.year,freq='Q').to_timestamp() # Convert to datetime
    del dkp_api['date']
    del dkp_api['Avg. in DKK']
    del dkp_api['Income Interval']
    del dkp_api['age']
    del dkp_api['Gender']
    
    return dkp_api
#Function for plotting populations with bachelors degree
def plot_ba_pop(ind_api):
    # Data frame with Copenhagen
    BA_copenhagen = ind_api.loc[ind_api['municipality'] == 'Copenhagen', :]
    # Data frame with Thisted
    BA_thisted = ind_api.loc[ind_api['municipality'] == 'Thisted', :]
    # Data frame with Aalborg
    BA_aalborg = ind_api.loc[ind_api['municipality'] == 'Aalborg', :]

    # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each DataFrame. Specify the ax parameter to ensure all plots are on the same axes.
    BA_copenhagen['population w. BA'].plot(ax=ax, label='Copenhagen')
    BA_thisted['population w. BA'].plot(ax=ax, label='Thisted')
    BA_aalborg['population w. BA'].plot(ax=ax, label='Aalborg')

    # Add some plot details
    ax.set_xlabel('Year')
    ax.set_ylabel("Population with a Bachelor's Degree")
    ax.set_title("Population with a Bachelor's Degree Over Time")
    ax.legend()

    # Display the plot
    plt.show()







