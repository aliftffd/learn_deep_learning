import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import speedtest
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Global data storage for speed measurements
data = {
    'time': [],
    'download': [],
    'upload': []
}

# Define the layout
app.layout = html.Div([
    html.H1("Real-Time Internet Speed Dashboard"),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # Update every 10 seconds (adjust as needed)
        n_intervals=0
    )
])

# Callback to update the graph
@app.callback(Output('live-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    # Get current time for x-axis
    now = datetime.datetime.now()

    # Perform speed test measurement
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1e6  # Convert to Mbps
        upload_speed = st.upload() / 1e6      # Convert to Mbps
    except Exception as e:
        # In case of an error, you can log it or set default values
        download_speed, upload_speed = 0, 0

    # Append new data
    data['time'].append(now)
    data['download'].append(download_speed)
    data['upload'].append(upload_speed)

    # Create traces for download and upload speeds
    download_trace = go.Scatter(
        x=data['time'],
        y=data['download'],
        mode='lines+markers',
        name='Download Speed (Mbps)'
    )
    upload_trace = go.Scatter(
        x=data['time'],
        y=data['upload'],
        mode='lines+markers',
        name='Upload Speed (Mbps)'
    )

    # Return the figure object with updated data
    return {
        'data': [download_trace, upload_trace],
        'layout': go.Layout(
            title='Real-Time Internet Speed',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Speed (Mbps)'),
            margin={'l': 40, 'r': 20, 't': 40, 'b': 40},
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
