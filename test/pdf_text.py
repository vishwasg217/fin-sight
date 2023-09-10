import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


import pypdf

def pdf_to_text(pdf_file_path):
    text = ""
    with open(pdf_file_path, 'rb') as file:
        file = pypdf.PdfReader(file)
        for page in file.pages:
            text += str(page.extract_text())
    return text

ans = pdf_to_text("AAPL.pdf")

# write ans to file
with open("AAPL.txt", "w") as file:
    file.write(ans)


