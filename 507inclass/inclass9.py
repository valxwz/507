
import plotly.graph_objs as go
import csv

f = open('CA-airports.csv')
csv_data = csv.reader(f)

big_lat_vals = []
big_lon_vals = []
big_text_vals = []
small_lat_vals = []
small_lon_vals = []
small_text_vals = []


for row in csv_data:
    if row[0] != 'iata':
    	traffic=int(row[7])
    	lat = row[5]
        lon = row[6]
        text = row[0]
        if traffic > 1000:
            big_lat_vals.append(row[5])
            big_lon_vals.append(row[6])
            big_text_vals.append(row[0])

        else:
            small_lat_vals.append(row[5])
            small_lon_vals.append(row[6])
            small_text_vals.append(row[0])

trace1 = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = big_lon_vals,
        lat = big_lat_vals,
        text = big_text_vals,
        mode = 'markers',
        marker = dict(
            size = 15,
            symbol = 'star',
            color = 'red'
        ))



trace2 = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = small_lon_vals,
        lat = small_lat_vals,
        text = small_text_vals,
        mode = 'markers',
        marker = dict(
            size = 8,
            symbol = 'circle',
            color = 'blue'
        ))
data = [trace1, trace2]

fig = go.Figure(data=data
    )

fig.update_layout(
(
    title = 'Most trafficked US airports<br>(Hover for airport names)',
    geo_scope='usa',
    )
fig.show()