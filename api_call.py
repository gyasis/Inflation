

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
    # print_dict(r.json()[0])
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
# remove rows that don't match the list of numbers(categories) in df.source
def refine_dataframe(df, listofsources):
    df = df[df['source']["id"].isin(listofsources)]
    return df
# %%
#split string into list of words separated by spaces 
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
df = WB_search('women are very much trouble')
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
tree = WB_search("ginni gni gdp wage salary inflation|male female youth school children maternal teacher young old education", exclude=True)


# %%
tree2 = WB_search("ginni gni gdp|male female youth school children maternal teacher young old education", exclude=True, sourcel=['2','6','81'])

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

#strip id value from dict from df.source and put into column
def get_id_value(df):
    df['id'] = df['source'].apply(lambda x: x['id'])
    
# %%
# drop rows in df.category that don't match a given list of numbers in variable listofnumbers
def drop_data(df, listofnumbers):
    df = df[df['category'].isin(listofnumbers)]
    return df
# %%
desired_categories = ["2","6","15","24","27","32","60","70","81","83"]
# %%
drop_data(tree, desired_categories)
# %%
refined_df = drop_data(tree, desired_categories)
# %%
#save dataframe
refined_df.to_csv('refined_df.csv')
# %%
# the next part involved exporting to excel and reimporting ashortend version from a highlighted copy to pandas dataframe

df5 = pd.read_excel('refined_df2.xlsx', sheet_name='Sheet1')
df5 = df5.drop([1])
# %%

testdf= WB_get('NY.GNP.ATLS.CD', date='1900:2020',per_page=20000)


# %%
#get and save dataframes with WB_get where the indicator is a list of indicators
def get_data(listofindicators, date='1900:2020', per_page=20000):
    from IPython.core.display import display, HTML
    
    for i, indicator in enumerate(listofindicators):
        try:
            tempdf = WB_get(indicator, date=date, per_page=per_page)
            if i < 10:
                tempdf.to_csv(f'Data/0{i}.csv')
                print(f"{i}.  {indicator} saved\n") 
                
            else:
                tempdf.to_csv(f'Data/{i}.csv')
                print(f"{i}.  {indicator} save\n")
        except:
            print(f"{i}.  ----Exception!!! {indicator} failed to save") 
            display(HTML('<h1>Missing Data!! Check indicator</h>'))
            print(f"\n")
            
   
# %%
        
    r
# %%

get_data(df5['id'], date='1900:2020', per_page=20000)

# %%
import dtale

example_df = pd.read_csv('Data/4.csv')
example_df.dropna(subset=['value'], inplace=True)
d = dtale.show(example_df)

# %%
d.open_browser()
# %%
# DISCLAIMER: 'df' refers to the data you passed in when calling 'dtale.show'

import pandas as pd
df = example_df
if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
	df = df.to_frame(index=False)

# remove any pre-existing indices for ease of use in the D-Tale code, but this is not required
df = df.reset_index().drop('index', axis=1, errors='ignore')
df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

chart_data = pd.concat([
	df['date'],
	df['value'],
	df['countryiso3code'],
], axis=1)
chart_data = chart_data.query("""(`countryiso3code` == 'USA') or (`countryiso3code` == 'AUS') or (`countryiso3code` == 'SWZ') or (`countryiso3code` == 'GBR') or (`countryiso3code` == 'CHN')""")
chart_data = chart_data.sort_values(['countryiso3code', 'date'])
chart_data = chart_data.rename(columns={'date': 'x'})
chart_data = chart_data.dropna()
# WARNING: This is not taking into account grouping of any kind, please apply filter associated with
#          the group in question in order to replicate chart. For this we're using '"""`countryiso3code` == 'AUS'"""'
# chart_data = chart_data.query("""(`countryiso3code` == 'USA') or (`countryiso3code` == 'SWZ') or (`countryiso3code` == 'DEU') or (`countryiso3code` == 'ITA') or (`countryiso3code` == 'AUS')""")

import plotly.graph_objs as go

charts = []
line_cfg = {'line': {'shape': 'spline', 'smoothing': 0.3}, 'mode': 'lines'}
charts.append(go.Scatter(
	x=chart_data['x'], y=chart_data['value'], name='value', **line_cfg
))
figure = go.Figure(data=charts, layout=go.Layout({
    'legend': {'orientation': 'h'},
    'title': {'text': 'value by date'},
    'xaxis': {'tickformat': '0:g', 'title': {'text': 'date'}},
    'yaxis': {'title': {'text': 'value'}, 'type': 'linear'}
}))

# If you're having trouble viewing your chart in your notebook try passing your 'chart' into this snippet:
# %%
from plotly.offline import iplot, init_notebook_mode

init_notebook_mode(connected=True)
for chart in charts:
    chart.pop('id', None) # for some reason iplot does not like 'id'
iplot(figure)
# %%
# DISCLAIMER: 'df' refers to the data you passed in when calling 'dtale.show'

import pandas as pd

if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):
	df = df.to_frame(index=False)

# remove any pre-existing indices for ease of use in the D-Tale code, but this is not required
df = df.reset_index().drop('index', axis=1, errors='ignore')
df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers

chart_data = pd.concat([
	df['date'],
	df['value'],
	df['countryiso3code'],
], axis=1)
chart_data = chart_data.query("""(`countryiso3code` == 'USA') or (`countryiso3code` == 'SWZ') or (`countryiso3code` == 'DEU') or (`countryiso3code` == 'ITA') or (`countryiso3code` == 'AUS')""")
s = chart_data['countryiso3code']
def drop_repeated_words(val):
    def _load():
        val_segs = val.split(' ')
        for i, v2 in enumerate(val_segs):
            if i == 0:
                yield v2
            elif val_segs[i - 1] != v2:
                yield v2
            return ' '.join(list(_load()))
s = s.apply(drop_repeated_words)
chart_data.loc[:, 'countryiso3code'] = s
chart_data = chart_data.sort_values(['countryiso3code', 'date'])
chart_data = chart_data.rename(columns={'date': 'x'})
chart_data_mean = chart_data.groupby(['countryiso3code', 'x'])[['value']].mean()
chart_data_mean.columns = ['value|mean']
chart_data = chart_data_mean.reset_index()
chart_data = chart_data.dropna()
# WARNING: This is not taking into account grouping of any kind, please apply filter associated with
#          the group in question in order to replicate chart. For this we're using '"""`countryiso3code` == 'AUS'"""'
chart_data = chart_data.query("""(`countryiso3code` == 'USA') or (`countryiso3code` == 'SWZ') or (`countryiso3code` == 'DEU') or (`countryiso3code` == 'ITA') or (`countryiso3code` == 'AUS')""")

import plotly.graph_objs as go

charts = []
line_cfg = {'line': {'shape': 'spline', 'smoothing': 0.3}, 'mode': 'lines'}
charts.append(go.Scatter(
	x=chart_data['x'], y=chart_data['value|mean'], name='value|mean', **line_cfg
))
figure = go.Figure(data=charts, layout=go.Layout({
    'legend': {'orientation': 'h'},
    'title': {'text': 'Mean of value by date'},
    'xaxis': {'tickformat': '0:g', 'title': {'text': 'date'}},
    'yaxis': {'title': {'text': 'Mean of value'}, 'type': 'linear'}
}))
# %%
# If you're having trouble viewing your chart in your notebook try passing your 'chart' into this snippet:

from plotly.offline import iplot, init_notebook_mode

init_notebook_mode(connected=True)
for chart in charts:
    chart.pop('id', None) # for some reason iplot does not like 'id'
iplot(figure)
# %%
# %%
from IPython.display import IFrame
display(IFrame(src='/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/Inflation/html/line_export_1639277198872.html', width=700, height=600))
# %%
%%html
<H1>Hello</H1>
# %%
def single_chart(df,referencedf,i):
    import plotly.express as px
    # print(df.head(5))
    chart_data = df
    chart_data = chart_data[['date', 'value', 'countryiso3code']]
    chart_data = chart_data.query("""(`countryiso3code` == 'USA') or (`countryiso3code` == 'AUS') or (`countryiso3code` == 'SWZ') or (`countryiso3code` == 'GBR') or (`countryiso3code` == 'CHN')""")
    chart_data = chart_data.dropna()
    
    
    fig = px.line(chart_data, 
                  x='date', 
                  y='value',
                  color='countryiso3code',
                  title=referencedf.name[i]
                  )
    fig.show()
# %%
def create_charts(reference_df, dffolder,chart_type='line'):
    
    file_list = glob.glob(dffolder + '/*.csv')
    for x, file in enumerate(file_list):
        print(file)
        df = pd.read_csv(file)
        # print(df.head(5))
        try:
            single_chart(df, reference_df,x)
        except:
            print('failed to create chart for file: ' + file)
           

# %%
reference_df = pd.read_excel('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/Inflation/refined_df2.xlsx')
reference_df = reference_df.drop([1])
reference_df.head(5)

# %%
create_charts(reference_df, '/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/Inflation/Data')
# %%
reference_df.head(5)
# %%

chart_data = pd.read_csv('/media/gyasis/Blade 15 SSD/Users/gyasi/Google Drive (not syncing)/Collection/Inflation/Data/00.csv')
chart_data = chart_data[['date', 'value', 'countryiso3code']]
print(chart_data.head(5))
chart_data = chart_data.query("""(`countryiso3code` == 'USA') or (`countryiso3code` == 'AUS') or (`countryiso3code` == 'SWZ') or (`countryiso3code` == 'GBR') or (`countryiso3code` == 'CHN')""")
chart_data = chart_data.dropna()

print(chart_data.head(5))
fig = px.line(df, x='date', y='value'
              ,color='countryiso3code',
            # title=referencedf.name[i]
                )
fig.show()
# %%
len(chart_data)
# %%
chart_data.countryiso3code.unique()
# %%
