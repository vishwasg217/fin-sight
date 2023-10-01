import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import plotly.io as pio
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image
from io import BytesIO
from PIL import Image as PILImage


from src.utils import create_donut_chart

def create_pdf_flowable_with_plotly(data, type_of_data):
    # Convert the Plotly figure to an image (in this case PNG format)
    fig = create_donut_chart(data, type_of_data)
    img_bytes = pio.to_image(fig, format="png")
    img = BytesIO(img_bytes)
    img = Image(img)
    return [img]

data = {
    "fruits": {"Apple": 18, "Banana": 20, "Cherry": 30}
}
type_of_data = "fruits"


flowables = create_pdf_flowable_with_plotly(data, type_of_data)

doc = SimpleDocTemplate("output.pdf", pagesize=letter)
doc.build(flowables)
