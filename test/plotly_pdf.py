# import sys
# from pathlib import Path
# script_dir = Path(__file__).resolve().parent
# project_root = script_dir.parent
# sys.path.append(str(project_root))

# import plotly.io as pio
# import plotly.graph_objects as go

# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
# from reportlab.platypus import SimpleDocTemplate, Image
# from io import BytesIO
# from PIL import Image as PILImage
# import tempfile



# from src.utils import create_donut_chart, create_bar_chart

# def create_pdf_flowable_with_plotly(data, type_of_data):
#     # Convert the Plotly figure to an image (in this case PNG format)
#     fig = go.Figure(data=[go.Bar(y=[2, 1, 3], x=["a", "b", "c"])])
#     img_bytes = fig.to_image(format="png")

#     temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
#     temp_file.write(img_bytes)
#     temp_file.close()
#     img = Image(temp_file.name, width=5*inch, height=3*inch)
#     return img

# data = {
#     "fruits": {"Apple": 18, "Banana": 20, "Cherry": 30}
# }
# type_of_data = "fruits"

# flowables = []

# flowables.append(create_pdf_flowable_with_plotly(data, type_of_data))

# doc = SimpleDocTemplate("output.pdf", pagesize=letter)
# doc.build(flowables)
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
    flowables = []
    flowables.append(chart1_path)

    # Create a PDF and add the flowables
    doc = SimpleDocTemplate("out1put.pdf", pagesize=letter)
    doc.build(flowables)

    # Clean up the temporary files
    # os.unlink(chart1_path)
    # os.unlink(chart2_path)

    print("PDF with two Plotly charts created!")

if __name__ == "__main__":
    main()