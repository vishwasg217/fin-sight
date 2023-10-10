import tabula
file1 = "https://nbviewer.jupyter.org/github/kuruvasatya/Scraping-Tables-from-PDF/blob/master/data1.pdf"
table = tabula.read_pdf(file1,pages=1)
print(table[0])