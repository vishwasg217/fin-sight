import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image
import tempfile
import os

def create_plotly_chart_image(data, labels):
    """
    Create a Plotly chart and save it to a temporary image file.
    Returns the path to the temporary image file.
    """
    fig = go.Figure(data=[go.Bar(y=data, x=labels)])
    img_bytes = fig.to_image(format="png")

    # Save the image bytes to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_file.write(img_bytes)
    temp_file.close()
    img = Image(temp_file.name, width=5*inch, height=3*inch)

    return img

def main():
    # Create two charts and get their image paths
    chart1_path = create_plotly_chart_image([2, 1, 3], ["a", "b", "c"])
    # chart2_path = create_plotly_chart_image([5, 3, 4], ["d", "e", "f"])

    # Create a list of flowables
    flowables = [
        chart1_path,
        # chart2_path
    ]

    # Create a PDF and add the flowables
    doc = SimpleDocTemplate("charts.pdf", pagesize=letter)
    doc.build(flowables)

    # Clean up the temporary files
    # os.unlink(chart1_path)
    # os.unlink(chart2_path)

    print("PDF with two Plotly charts created!")

if __name__ == "__main__":
    main()