import json
import os
from bs4 import BeautifulSoup
from llmsherpa.readers import LayoutPDFReader
from langchain.text_splitter import HTMLHeaderTextSplitter


class Ingestion:

    def __init__(self, pdf):
        self.pdf = pdf

    

    def extract(self):
        llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
        pdf_reader = LayoutPDFReader(llmsherpa_api_url)
        self.pdf = pdf_reader.read_pdf(path_or_url="data/streamlit/from_streamlit.pdf")

    def get_tables(self):
        str_tables = self.pdf.tables()
        str_tables = [table.to_html() for table in str_tables]
        if str_tables:
            return str_tables
        else:
            documents = self.pdf.chunks()
            html_docs = []
            for doc in documents:
                html_docs.append(doc.to_html())

            def contains_table(html):
                soup = BeautifulSoup(html, "html.parser")
                return bool(soup.find("table"))

            # Identify documents that contain tables
            str_tables = [html for html in html_docs if contains_table(html)]
            return str_tables

    def extract_items_table(self):
        all_tables = self.get_tables()
        items_table = None
        for table in all_tables:
            soup = BeautifulSoup(table, 'html.parser')
            if soup.find('td', string='Risk Factors'):
                items_table = table
            if items_table:
                return items_table
            
    def extract_items(self):
        items_table = self.extract_items_table()
        soup = BeautifulSoup(items_table, 'html.parser')
        table_rows = soup.find_all('tr')

        items = []

        for row in table_rows:
            row_content = [cell.text.strip() for cell in row.find_all(['td', 'th'])]
            if len(row_content) > 1:
                row_content = f"{row_content[0]} {row_content[1]}"
                items.append(row_content)
        return items
    
    def get_documents(pdf):
        headers = [
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3")
        ]

        splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers, return_each_element=True)
        documents = []
        
        sections = pdf.sections()
        for section in sections:
            content = section.to_html(include_children=True, recurse=True)
            splits = splitter.split_text(content)
            splits
            documents.extend(splits)
        
        return documents

