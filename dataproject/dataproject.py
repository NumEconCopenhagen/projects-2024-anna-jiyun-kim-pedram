import pandas as pd
from dstapi import DstApi
import matplotlib.pyplot as plt



#define the table for HFUD11 below 
def HFUD11_data():
    #Load the data from Statistik Banken
    ind = DstApi('HFUDD11') 

    #Set the language to english
    tabsum = ind.tablesummary(language='en')


    # The _define_base_params -method gives us a nice template (selects all available data)
    params = ind._define_base_params(language='en')
    params

    variables = params['variables'] # Returns a view, that we can edit
    #We are only looking at people from Copenhagen, Thisted and Aalborg
    variables[0]["values"] = ["101","787", "851"]
    #We are looking at people across all "Herkomst"
    variables[1]["values"] = ["TOT"]
    #We are looking at, how many people have a higher education
    variables[2]['values'] =['H70']
    #We don't look at people with a specific age. But only at Age,total. 
    variables[3]["values"] = ["TOT"]
    #We are only looking at people with the gender male and female
    variables[4]['values'] = ["TOT"]
    #We don't write anything for variables[5], and therefore, we are looking at people across all dates from 2008 to 2023.
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
    ind_api = ind_api.rename(columns = {'INDHOLD':'highereducation', 'BOPOMR': 'municipality', "ALDER":"age", "KØN": "gender", "TID" :"year"})

    # f. drop non-municipality
    for val in ['Region', 'All']: 
        I = ind_api['municipality'].str.contains(val)
        ind_api.drop(ind_api[I].index, inplace=True)


    # f. convert to date
    del ind_api["age"]
    del ind_api["HFUDD"]
    del ind_api["gender"]
    return ind_api





#Define the table for FOD407

def FOD407_data():
    fert = DstApi("FOD407")

    #Set the language to english
    tabsum = fert.tablesummary(language='en')

    # The _define_base_params -method gives us a nice template (selects all available data)
    params = fert._define_base_params(language='en')
    params  

    variables = params["variables"]
    #We are only looking at people from Copenhagen, Thisted and Aalborg
    variables[0]["values"] = ["101","787", "851"]
    #We are looking at total fertility rate
    variables[1]["values"] = ["TOT1"]
    #We are looking across all time, therefore we don't write anything to time. 
    params


    #Use the variables set above
    fert_api = fert.get_data(params=params)

    #Sort values for BOPOMR, HFDD, KØN and TID
    fert_api.sort_values(by=['OMRÅDE', 'ALDER', "TID"], inplace=True)
    fert_api.head(5)

    #Drop the coloumns "ALDER"
    for v in ['ALDER']: 
            del fert_api[v]


    #e. rename the columns
    fert_api = fert_api.rename(columns = {'OMRÅDE':'municipality', 'TID': 'year', "INDHOLD":"fertilityquotient"})


    # f. drop non-municipality¬
    for val in ['Region', 'All']: 
            I = fert_api['municipality'].str.contains(val)
            fert_api.drop(fert_api[I].index, inplace=True)

    fert_api['fertilityquotient'] = pd.to_numeric(fert_api['fertilityquotient'], errors='coerce')


    return fert_api



#Define a table for total populaiton in each area

def population_data():
    
    #Load the data from Statistik Banken
    pop = DstApi('HFUDD11') 

    #Set the language to english
    tabsum = pop.tablesummary(language='en')


    # The _define_base_params -method gives us a nice template (selects all available data)
    params = pop._define_base_params(language='en')
    params

    variables = params['variables'] # Returns a view, that we can edit
    #We are only looking at people from Copenhagen, Thisted and Aalborg
    variables[0]["values"] = ["101","787", "851"]
    #We are looking at people across all "Herkomst"
    variables[1]["values"] = ["TOT"]
    #We are looking at everyone, no matter the the education.
    variables[2]['values'] =['TOT']
    #We don't look at people with a specific age. But only at Age,total. 
    variables[3]["values"] = ["TOT"]
    #We are only looking at people with the gender male and female
    variables[4]['values'] = ["TOT"]
    #We don't write anything for variables[5], and therefore, we are looking at people across all dates from 2008 to 2023.
    params

    #Use the variables set above
    pop_api = pop.get_data(params=params)

    #Sort values for BOPOMR, HFDD, KØN and TID
    pop_api.sort_values(by=['BOPOMR', 'HFUDD', "KØN", "TID"], inplace=True)
    pop_api.head(5)

    # d. drop the columns "HERKOMST"
    for v in ['HERKOMST']: 
        del pop_api[v]


    #e. rename the columns
    pop_api = pop_api.rename(columns = {'INDHOLD':'totalpop', 'BOPOMR': 'municipality', "ALDER":"age", "KØN": "gender", "TID" :"year"})

    # f. drop non-municipality
    for val in ['Region', 'All']: 
        I = pop_api['municipality'].str.contains(val)
        pop_api.drop(pop_api[I].index, inplace=True)


    # f. convert to date
    del pop_api["age"]
    del pop_api["HFUDD"]
    del pop_api["gender"]

    return pop_api



#Function for plotting populations with bachelors degree
def plot_ba_pop(ind_api):
    # Data frame with Copenhagen
    HE_copenhagen = ind_api.loc[ind_api['municipality'] == 'Copenhagen', :]
    # Data frame with Thisted
    HE_thisted = ind_api.loc[ind_api['municipality'] == 'Thisted', :]
    # Data frame with Aalborg
    HE_aalborg = ind_api.loc[ind_api['municipality'] == 'Aalborg', :]

    # Create a figure and axis object
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot each DataFrame. Specify the ax parameter to ensure all plots are on the same axes.
    HE_copenhagen['population w. HE'].plot(ax=ax, label='Copenhagen')
    HE_thisted['population w. HE'].plot(ax=ax, label='Thisted')
    HE_aalborg['population w. HE'].plot(ax=ax, label='Aalborg')

    # Add some plot details
    ax.set_xlabel('Year')
    ax.set_ylabel("Population with a Bachelor's Degree")
    ax.set_title("Population with a Bachelor's Degree Over Time")
    ax.legend()

    # Display the plot
    plt.show()



#Function for plotting fertility and BA in copenhagen
def plot_fer_HE_copenhagen(ind_api, fert_api):
    # Create a figure and axis object
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot each DataFrame. Specify the ax parameter to ensure all plots are on the same axes.
    HE_copenhagen = ind_api.loc[ind_api['municipality'] == 'Copenhagen', :]
    fertility_copenhagen = fert_api.loc[fert_api['municipality'] == 'Copenhagen', :]

    # Plot the data about population with a HE on the first y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Population with a HE', color=color)
    HE_copenhagen.plot(x='year', y='highereducation', ax=ax1, label='Population with a HE', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis that shares the same x-axis
    ax2 = ax1.twinx()

    # Plot the data about fertility on the second y-axis
    color = 'tab:red'
    ax2.set_ylabel('Fertility quotient', color=color)
    fertility_copenhagen.plot(x='year', y='fertilityquotient', ax=ax2, label='Fertility quotient', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Add title and legend
    fig.tight_layout()  # To ensure the right y-label is not clipped
    ax1.set_title("Fertility and education in Copenhagen")

    #Display
    plt.show()

#Function for plotting fertility and BA in Aalborg
def plot_fer_HE_aalborg(ind_api, fert_api):
     # Create a figure and axis object
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot each DataFrame. Specify the ax parameter to ensure all plots are on the same axes.
    HE_aalborg = ind_api.loc[ind_api['municipality'] == 'Aalborg', :]
    fertility_aalborg = fert_api.loc[fert_api['municipality'] == 'Aalborg', :]

    #First for Aalborg

    # Plot the data about population with a BA on the first y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Population with a HE', color=color)
    HE_aalborg.plot(x='year', y='highereducation', ax=ax1, label='Population with a HE', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis that shares the same x-axis
    ax2 = ax1.twinx()

    # Plot the data about fertility on the second y-axis
    color = 'tab:red'
    ax2.set_ylabel('Fertility quotient', color=color)
    fertility_aalborg.plot(x='year', y='fertilityquotient', ax=ax2, label='Fertility quotient', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Add title and legend
    fig.tight_layout()  # To ensure the right y-label is not clipped
    ax1.set_title("Fertility and education in Aalborg")

    plt.show()



#Function for plotting fertility and BA in Thisted

def plot_fer_HE_thisted(ind_api, fert_api):
    # Create a figure and axis object
    fig, ax1 = plt.subplots(figsize=(10, 6))

    HE_thisted = ind_api.loc[ind_api['municipality'] == 'Thisted', :]
    fertility_thisted = fert_api.loc[fert_api['municipality'] == 'Thisted', :]


    # Plot the data about population with a BA on the first y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Population with a HE', color=color)
    HE_thisted.plot(x='year', y='highereducation', ax=ax1, label='Population with a HE', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis that shares the same x-axis
    ax2 = ax1.twinx()

    # Plot the data about fertility on the second y-axis
    color = 'tab:red'
    ax2.set_ylabel('Fertility quotient', color=color)
    fertility_thisted.plot(x='year', y='fertilityquotient', ax=ax2, label='Fertility quotient', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Add title and legend
    fig.tight_layout()  # To ensure the right y-label is not clipped
    ax1.set_title("Fertility and education in Thisted")

    plt.show()


#Function for plotting fertility as an interactive figure

def plot_fer_BA(municipality, ind_api, fert_api):
    # Create a figure and axis object
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Filter the DataFrame for the selected municipality
    BA_data = ind_api.loc[ind_api['municipality'] == municipality, :]
    fertility_data = fert_api.loc[fert_api['municipality'] == municipality, :]

    # Plot the data about population with a BA on the first y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Population with a BA', color=color)
    BA_data.plot(x='year', y='BA', ax=ax1, label='Population with a BA', color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis that shares the same x-axis
    ax2 = ax1.twinx()

    # Plot the data about fertility on the second y-axis
    color = 'tab:red'
    ax2.set_ylabel('Fertility quotient', color=color)
    fertility_data.plot(x='year', y='fertilityquotient', ax=ax2, label='Fertility quotient', color=color, marker='x')
    ax2.tick_params(axis='y', labelcolor=color)

    # Add title and possibly a legend
    fig.tight_layout()  # To ensure the right y-label is not clipped
    ax1.set_title(f"Fertility and Education in {municipality}")
    plt.show()















#Importing data for education levels from the CSV with data from eurostat
def educ_c():
    #Rename the country codes so they match that of the World Bank Data
    country_mapping = {
        "BE": "BEL", "BG": "BGR", "HR": "HRV", "CY": "CYP", "DK": "DNK", "CZ": "CZE", "EE": "EST", "FR": "FRA", "FI": "FIN",
        "DE": "DEU", "EL": "GRC", "HU": "HUN", "IE": "IRL", "IT": "ITA", "IS": "ISL", "LV": "LVA", "LT": "LTU", "LU": "LUX",
        "MK": "MKD", "NL": "NLD", "MT": "MLT", "ME": "MNE", "NO": "NOR", "PL": "POL", "PT": "PRT", "AT": "AUT", "RO": "ROU",
        "SK": "SVK", "RS": "SRB", "SI": "SVN", "SE": "SWE", "ES": "ESP", "CH": "CHE", "GB": "GBR"
    }
    #Read the data from the CSV file and replace the 'geo' labels with the newly named ones

    educ = pd.read_csv('sdg_04_20_page_linear.csv')
    educ['geo'] = educ['geo'].replace(country_mapping)

    # columns to remove (columns 1-7 and column 11) since they are not needed
    c_remove = list(educ.columns[0:7]) + [educ.columns[10]]

    # Drop the specified columns from the DataFrame
    educ_c = educ.drop(columns=c_remove)

    #renaming columns to something more suitable
    educ_c.rename(columns = {'geo':'Country'}, inplace=True)
    educ_c.rename(columns = {'TIME_PERIOD':'Years'}, inplace=True)
    educ_c.rename(columns = {'OBS_VALUE':'% tertiary educ.'}, inplace=True)
    return educ_c




#Importing fertility data from the CSV with data from the World Bank Indicators
def fert():

    fert = pd.read_csv('Fert_Data.csv')

    # These columns have to go: 'Country Name' 'Time Code', and bottom rows should be deleted
    drop_these = (['Country Name'] + ['Time Code']) 

    fert.drop(range(374, fert.shape[0]), inplace=True) # drop rows starting from index 374 and on

    fert.drop(drop_these, axis=1, inplace=True)

    #Changing Time to an integer
    fert['Time'] = fert['Time'].astype(int)

    #Changing Names of columns
    fert.rename(columns = {'Country Code':'Country'}, inplace=True)
    fert.rename(columns = {'Time':'Years'}, inplace=True)
    fert.rename(columns = {'Fertility rate, total (births per woman) [SP.DYN.TFRT.IN]':'Fertility'}, inplace=True)
    return fert



#Graph across countries
def plot_fertility_education_country(educ_sorted, fert_sorted, country_codes):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set colors for plotting
    educ_colors = ['tab:blue', 'tab:red', 'tab:green']
    fert_colors = ['tab:blue', 'tab:red', 'tab:green']

    ax2 = ax.twinx()  # Create a secondary y-axis that shares the same x-axis with ax

    for i, country_code in enumerate(country_codes):
        educ_country = educ_sorted.loc[educ_sorted['Country'] == country_code]
        fertility_country = fert_sorted.loc[fert_sorted['Country'] == country_code]

        # Plot the data for education for each country
        color_educ = educ_colors[i]
        educ_label = 'Pop. w. tertiary educ. - ' + country_code
        educ_country.plot(x='Years', y='% tertiary educ.', ax=ax, label=educ_label, color=color_educ, linestyle='--')
        
        # Plot the data for fertility for each country
        color_fert = fert_colors[i]
        fert_label = 'Fertility - ' + country_code
        fertility_country.plot(x='Years', y='Fertility', ax=ax2, label=fert_label, color=color_fert)
        # Remove the legends inside the plot
        ax.get_legend().remove()
        ax2.get_legend().remove()

    # Set y-axis limits, ticks and label for population axis
    ax.set_ylim(20, 50)
    ax.set_yticks(range(20, 50, 5))
    ax.set_ylabel('% population age 25-34 with tertiary educ.', color='black')

    # Set y-axis limits, ticks and label for fertility axis
    ax2.set_ylim(1, 2)  # Adjust y-axis limits for fertility data
    ax2.set_yticks([1, 1.5, 2])  # Set custom y-axis ticks for fertility data
    ax2.set_ylabel('Fertility', color='black')

    # Add title
    fig.tight_layout()
    plt.title("Fertility and education in selected countries")

    fig.legend(loc='lower center', bbox_to_anchor=(0.5, -0.1), shadow=True, ncol=3)

   
    plt.show()



