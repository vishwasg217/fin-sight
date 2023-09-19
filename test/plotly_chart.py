import plotly.graph_objects as go

def create_donut_chart(data, hole_size=0.3):
    """
    Create a donut chart using Plotly.

    Parameters:
    - data_dict: Dictionary where keys are labels and values are the corresponding data values.
    - hole_size: Size of the hole in the donut chart (default is 0.3).

    Returns:
    - A Plotly Figure object representing the donut chart.
    """
    
    labels = list(data.keys())
    values = list(data.values())
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=hole_size)])
    
    return fig

# Example usage:
data = {
    'Oxygen': 4500,
    'Hydrogen': 2500,
    'Carbon_Dioxide': 1053,
    'Nitrogen': 500
}
chart = create_donut_chart(data)
chart.show()
