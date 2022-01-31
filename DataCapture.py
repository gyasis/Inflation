# %%
try:
    %load_ext autotime
except:
    pass
# %%
import glob
import pandas as pd 
import tqdm
# %%
# get World Bank API data
# http://api.worldbank.org/v2/country/all/indicator/EN.ATM.CO2E.PC?format=json&date=1961:2011&per_page=2000

def WB_get(indicator, *args, **kwargs):
    import requests
    
    """
    <!-- Get World Bank API data
    :param base: base url
    :param country: country code
    :param indicator: indicator code
    :param format: json or xml
    :param args: additional arguments
    :param kwargs: additional keyword arguments
    :return: dataframe -->
    """
    
    #build http query request
    base = "http://api.worldbank.org/v2/"
    country = "all"
    indicator = indicator
    format = "json"
    url = base + 'country/' + country + '/indicator/' + indicator + '?format=' + format
    if args:
        url += '&' + '&'.join(args)
    if kwargs:
        url += '&' + '&'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        
    #shows the http querey request
    print("Getting Data from ", url)

    def print_dict(d):
        for k, v in d.items():
            print("%s : %s " %(k, v))
            if (k == "pages" and v > 1):
                print("Warning!!! \n Not all data is captured by dictionary, Increase number of items per page")
    #actual request
    r = requests.get(url)
    
    # print_dict(r.json()[0])
    df = pd.json_normalize(r.json()[1])
    return df
# %%
from traitlets.traitlets import TraitType
import wbdata as wb
#####################################################################
# EXAMPLES OF API CALLS                                             #
# wb.get_source()  get all sources or groups                        #
# wb.search_indicators('income') search by keyword                  #
# wb.get_indicator(source=24) get all indicators from this group    #
#####################################################################

# %%
# remove rows that don't match the list of numbers(categories) in df.source
def refine_dataframe(df, listofsources):
    df = df[df['source']["id"].isin(listofsources)]
    return df


# %%
#split SEARCH string into list of words separated by spaces ....LATER USE NLP
def WB_search(x, exclude=False):
    if exclude == True:
        x = x.split("|")
        ex_terms = (x[1]).split(" ")
        x = x[0]
        # print(ex_terms)
        
    x = x.split(" ")
    print(x)
    output = list()
    for result in x:
        print(result)
        if len(result) > 2:
            result = wb.search_indicators(result)
        output.extend(result)
        print(len(output))
           
    df = pd.DataFrame(output)
    df = df[['id','name','source','sourceNote']]
    df['category'] = df['source'].apply(lambda x: x['id'])
   
    
    if exclude == True:
        #remove rows with excluded terms
        df = df[~df['sourceNote'].str.contains('|'.join(ex_terms),case=False)]
        df = df[~df['name'].str.contains('|'.join(ex_terms), case=False)]
    print(len(df))
    
    
  
        
    return df

# %%
''' 
SIMPLE USE OF WB_SEARCH
DF = WB_search('women are very much trouble') --> just search with list of terms

TO EXCLUDE TERMS TYPE A "|" AND IMMEDIATELY AFTER PLACE THE TERMS YOU WANT TO EXCLUDE
tree2 = WB_search("ginni gni gdp|male female youth school children maternal teacher young old education", exclude=True)
'''


tree = WB_search("ginni gni gdp|male female youth school children maternal teacher young old education", exclude=True)


# %%
def get_id_value(df):
    df['id'] = df['source'].apply(lambda x: x['id'])
    
# %%
# to further refine the data that you go with WB search drop unnecessary categories
# drop rows in df.category that don't match a given list of numbers in variable listofnumbers
def drop_data(df, listofnumbers):
    df = df[df['category'].isin(listofnumbers)]
    return df
desired_categories = ["2","6","15","24","27","32","60","70","81","83"]
refined_df=drop_data(tree, desired_categories)

# %%
#get and save dataframes with WB_get where the indicator is a list of indicators
def get_data(listofindicators, date='1900:2020', per_page=20000, path='./'):
    from IPython.core.display import display, HTML
    error_list = list()
    for i, indicator in enumerate(tqdm.tqdm(listofindicators)):
        try:
            tempdf = WB_get(indicator, date=date, per_page=per_page)
            if i < 10:
                tempdf.to_csv(f'{path}/0{i}.csv')
                print(f"{i}.  {indicator} saved\n") 
                
            else:
                tempdf.to_csv(f'{path}{i}.csv')
                print(f"{i}.  {indicator} save\n")
        except:
            print(f"{i}.  ----Exception!!! {indicator} failed to save") 
            display(HTML('<h1>Missing Data!! Check indicator</h>'))
            print(f"\n")
            error_list.append(i)
    
    temp_list = glob.glob(f'{path}*.csv')
    new_list = [x.replace(path, '') for x in temp_list]
    
    #need to convert strings to ints to sort and then back again to strings
    new_list = [x.replace('.csv', '') for x in new_list]
    new_list = list(map(int, new_list))
    new_list = sorted(new_list)
    new_list = list(map(str, new_list))
    #join ".csv" to each element in list
    new_list = [x + '.csv' for x in new_list]
    
    if len(new_list) != len(refined_df):
        print("Error: Some files were not saved \n check logs\n attempting to reflect missing files in dataframe")
        for error_ in error_list:
            print(len(new_list))
            new_list.insert(int(error_),"None")
    info_dataframe = pd.DataFrame(zip(new_list, list(refined_df['sourceNote'])), columns=['file', 'description'])
    print(info_dataframe)
    return info_dataframe

# %%
# new_list = glob.glob('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/Inflation/Data/*.csv')
# new_list = sorted(new_list)
# new_list = [x.replace('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/Inflation/Data/', '') for x in new_list]
# new_list = [x.replace('.csv', '') for x in new_list]
# new_list = list(map(int, new_list))
# new_list = sorted(new_list)
# new_list = list(map(str, new_list))
# #join ".csv" to each element in list
# new_list = [x + '.csv' for x in new_list]



# %%

info_dataframe = get_data(refined_df['id'], date='1900:2020', per_page=20000, path='/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/Inflation/Data/')
# %%