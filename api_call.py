

# %%
# base = http://api.worldbank.org/v2/
# country = all
# indicator = indicator
# format = json
# daterange = 2000:2015


# %%
# get World Bank API data
#example api call
# http://api.worldbank.org/v2/country/all/indicator/EN.ATM.CO2E.PC?format=json&date=1961:2011&per_page=2000
def worldbank_get(indicator, *args, **kwargs):
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
        "%s : %s " %(k, v)
        if (k == "pages" and v > 1):
            print("Warning!!! Not all data is captured by dictionary, Increase number of items per page")
        

# %%

from traitlets.traitlets import TraitType
import wbdata as wb
# %%
wb.get_source()
# %%
# %%
wb.search_indicators('income')
# %%
wb.get_indicator(source=24)

# %%

# %%
#split string into list of words separated by spaces 
def WorldBank_search(x, exclude=False):
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
    df = df[['id','name','sourceNote']]
    
    if exclude == True:
        #remove rows with excluded terms
        df = df[~df['sourceNote'].str.contains('|'.join(ex_terms),case=False)]
        df = df[~df['name'].str.contains('|'.join(ex_terms), case=False)]
    print(len(df))
    return df
# %%
df = WorldBank_search('women are very much trouble')
# %%
import ipywidgets as widgets
# %%
widgets.IntSlider(
    min=0,
    max=10,
    step=1,
    description='Slider:',
    value=3
)
# %%
import panel as pn
pn.extension(comms='ipywidgets')

# %%
# df_widget = pn.widgets.DataFrame(df, name='DataFrame')
# %%

pn.extension(comms='vscode')
# %%
# df_widget = pn.widgets.DataFrame(df, name='DataFrame')
# df_widget
# %%
df_widget = pn.widgets.Tabulator(tree, selectable='checkbox',pagination='local',pagesize = '50')
df_widget
# %%
# needed for tabulator support

# %%html
# <script>
# requirejs.config(
#     {paths: { 'tabulator': ['https://unpkg.com/tabulator-tables@4.7.2/dist/js/tabulator.min']},}
# );
# if(!window.Tabulator) {
#     require(['tabulator'],function(tabulator) {window.Tabulator=tabulator;});
# }
# </script>
# %%
tree = WorldBank_search("ginni gni gdp wage salary inflation|male female youth school children maternal teacher young old education", exclude=True)


# %%
import sys
import uuid
import logging
import panel as pn

pn.extension('terminal')

terminal = pn.widgets.Terminal(
    "Welcome to the Panel Terminal!\nI'm based on xterm.js\n\n",
    options={"cursorBlink": True},
    height=300, sizing_mode='stretch_width'
)

terminal
# %%
6.0.GNIpc

