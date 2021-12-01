

# %%
base = http://api.worldbank.org/v2/
country = all
indicator = indicator
format = json
daterange = 2000:2015


# %%
# get World Bank API data
#example api call
# http://api.worldbank.org/v2/country/all/indicator/EN.ATM.CO2E.PC?format=json&date=1961:2011&per_page=2000
def worldbank_get(indicator, *args, **kwargs):
    import requests
    
    """
    Get World Bank API data
    :param base: base url
    :param country: country code
    :param indicator: indicator code
    :param format: json or xml
    :param args: additional arguments
    :param kwargs: additional keyword arguments
    :return: dataframe
    """
    
    base = "http://api.worldbank.org/v2/"
    country = "all"
    indicator = indicator
    format = "json"
    url = base + 'country/' + country + '/indicator/' + indicator + '?format=' + format
    if args:
        url += '&' + '&'.join(args)
    if kwargs:
        url += '&' + '&'.join(['{}={}'.format(k, v) for k, v in kwargs.items()])
        
    print("Getting Data from ", url)

    def print_dict(d):
        for k, v in d.items():
            print("%s : %s " %(k, v))
            
    r = requests.get(url)
    print_dict(r.json()[0])
    df = pd.json_normalize(r.json()[1])
    
    
    return df


# %%
# print key and values of a dictionary  (for debugging)
def print_dict(d):
    for k, v in d.items():
        print("%s : %s " %(k, v))
        "%s : %s " %(k, v
        if k == "pages" && v > 1:
            print("Warning!!! Not all data is captured by dictionary, Increase number of items per page")
        

# %%

import wbdata as wb
# %%
wb.get_source()
# %%
wbdata.search_indicators('wage')
# %%
wb.search_indicators('Housing')
# %%
wb.search_indicators('average wages')
# %%
wb.search_indicators('income')
# %%
wb.get_indicator(source=24)
# %%
wb.search_indicators('Health')
# %%
wb.search_indicators('Startup')
# %%
