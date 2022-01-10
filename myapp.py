import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.layouts import widgetbox, row
from bokeh.models import Select
from bokeh.models import DateRangeSlider
import datetime as dt
from bokeh.models.widgets import Tabs, Panel


dataset = pd.read_csv("dataset.csv")

index = dataset[dataset["Location Level"] == "Country"].index
dataset.drop(index,axis=0,inplace=True)

df = dataset.iloc[:,:12]
coloumn = ["Location ISO Code","New Deaths","New Cases","Total Deaths","Location Level"]
df.drop(coloumn,axis=1,inplace=True)

coloumn = {
    "New Recovered":"New_Recovered",
    "New Active Cases":"New_Active_Cases",
    "Total Cases":"Total_Cases",
    "Total Recovered":"Total_Recovered",
    "Total Active Cases":"Total_Active_Cases"
}

df.rename(coloumn,axis=1,inplace=True)

df["Date"] = pd.to_datetime(df["Date"]).dt.date
df["Location_STR"] = df["Location"]
#print(df.head(5))
x_location = df['Location'].value_counts().sort_index().index.tolist()



source = ColumnDataSource(data={ #total covid cases
    'Date'  : df[df['Location'] == 'DKI Jakarta']['Date'],
    'Total_Cases' : df[df['Location'] == 'DKI Jakarta']['Total_Cases']
})

source_group = ColumnDataSource(data={
    'Date'  : df[df['Location'] == 'DKI Jakarta']['Date'],
    'Total_Active_Cases' : df[df['Location'] == 'DKI Jakarta']['Total_Active_Cases']
}) 

source_group_2 = ColumnDataSource(data={
    'Date'  : df[df['Location'] == 'DKI Jakarta']['Date'],
    'Total_Active_Cases' : df[df['Location'] == 'DKI Jakarta']['Total_Active_Cases'],
    'New_Active_Cases' : df[df['Location'] == 'DKI Jakarta']['New_Active_Cases']
})

tooltip_data = [
        ('Date', '@Date{%F}'),
        ('Total Cases', '@Total_Cases')
]

tooltip_group = [
        ('Date', '@Date{%F}'),
        ('Total Active Cases', '@Total_Active_Cases')
]

tooltip_group_2 = [
        ('Date', '@Date{%F}'),
        ('Total Active Cases', '@Total_Active_Cases'),
        ('New Active Cases', '@New_Active_Cases')
]

#print(source)
fig_data = figure(x_axis_type='datetime',
        plot_height=500, plot_width=750,
        title='Province Total Covid Cases',
        x_axis_label='Date', y_axis_label='Total Cases')

fig_data2 = figure(x_axis_type='datetime',
        plot_height=500, plot_width=750,
        title='Province Total Active Cases',
        x_axis_label='Date', y_axis_label='Total Active Cases')

fig_data3 = figure(x_axis_type='datetime',
        plot_height=500, plot_width=750,
        title='Province New Active Cases',
        x_axis_label='Date', y_axis_label='New Active Cases')

fig_data.add_tools(HoverTool(tooltips = tooltip_data, formatters={'@Date':'datetime'}))
fig_data2.add_tools(HoverTool(tooltips = tooltip_group, formatters={'@Date':'datetime'}))
fig_data3.add_tools(HoverTool(tooltips = tooltip_group_2, formatters={'@Date':'datetime'}))

fig_data.line('Date', 'Total_Cases',  
                color='#CE1141',
                source=source)

fig_data2.line('Date', 'Total_Active_Cases',  
                color='#CE1141',
                source=source_group)

fig_data3.line('Date', 'New_Active_Cases',  
                color='#CE1141',
                source=source_group_2)

def update_data(attr,old,new):
    [start, end] = slider.value
    date_from = dt.datetime.fromtimestamp(start/1000.0).date()
    date_until = dt.datetime.fromtimestamp(end/1000.0).date()

    data_location = str(location_select.value)

    #new data
    loc_date = df[(df['Date'] >= date_from) & (df['Date'] <= date_until)]
    new_data = {
        'Date' : loc_date[loc_date['Location'] == data_location]['Date'],
        'Total_Cases' : loc_date[loc_date['Location'] == data_location]['Total_Cases'],
    }
    source.data = new_data

def update_data2(attr,old,new):
    [start, end] = slider2.value
    date_from = dt.datetime.fromtimestamp(start/1000.0).date()
    date_until = dt.datetime.fromtimestamp(end/1000.0).date()

    data_location = str(location_select2.value)

    #new data
    loc_date = df[(df['Date'] >= date_from) & (df['Date'] <= date_until)]
    new_data = {
        'Date' : loc_date[loc_date['Location'] == data_location]['Date'],
        'Total_Active_Cases' : loc_date[loc_date['Location'] == data_location]['Total_Active_Cases']
    }
    source_group.data = new_data

def update_data3(attr,old,new):
    [start, end] = slider3.value
    date_from = dt.datetime.fromtimestamp(start/1000.0).date()
    date_until = dt.datetime.fromtimestamp(end/1000.0).date()

    data_location = str(location_select3.value)

    #new data
    loc_date = df[(df['Date'] >= date_from) & (df['Date'] <= date_until)]
    new_data = {
        'Date' : loc_date[loc_date['Location'] == data_location]['Date'],
        'Total_Active_Cases' : loc_date[loc_date['Location'] == data_location]['Total_Active_Cases'],
        'New_Active_Cases' : loc_date[loc_date['Location'] == data_location]['New_Active_Cases']
    }
    source_group_2.data = new_data

location_select = Select(
    options=[str(x) for x in x_location],
    value = 'DKI Jakarta',
    title = 'Location'
)

location_select2 = Select(
    options=[str(x) for x in x_location],
    value = 'DKI Jakarta',
    title = 'Location'
)

location_select3 = Select(
    options=[str(x) for x in x_location],
    value = 'DKI Jakarta',
    title = 'Location'
)

location_select.on_change('value',update_data)
location_select2.on_change('value',update_data2)
location_select3.on_change('value',update_data3)

init_value = (df['Date'].min(), df['Date'].max())

slider = DateRangeSlider(start = init_value[0], end = init_value[1], value=init_value)
slider2 = DateRangeSlider(start = init_value[0], end = init_value[1], value=init_value)
slider3 = DateRangeSlider(start = init_value[0], end = init_value[1], value=init_value)

slider.on_change('value' ,update_data) 
slider2.on_change('value' ,update_data2) 
slider3.on_change('value' ,update_data3)

layout = row(widgetbox(location_select, slider), fig_data)
layout2 = row(widgetbox(location_select2,slider2), fig_data2)
layout3 = row(widgetbox(location_select3,slider3), fig_data3)

panel = Panel(child=layout, title='Province Total Covid Cases')
panel_2 = Panel(child=layout2, title= 'Province Total Active Cases')
panel_3 = Panel(child=layout3, title= 'Province New Active Cases')
tabs = Tabs(tabs=[panel,panel_2,panel_3])  

curdoc().add_root(tabs)