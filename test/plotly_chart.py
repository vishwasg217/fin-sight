import plotly.graph_objects as go

def create_time_series_chart(data, labels):
    fig = go.Figure(data=[go.Scatter(x=labels, y=data, mode='lines+markers')])

    # Set y-axis to start from 0
    fig.update_layout(yaxis=dict(range=[0, max(data)]))

    return fig

# Sample data
dates = ['2022-01-01', '2022-01-02', '2022-01-03', '2022-01-04', '2022-01-05']
values = [10, 15, 12, 17, 14]

chart = create_time_series_chart(values, dates)
chart.show()
