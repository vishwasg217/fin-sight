from bs4 import BeautifulSoup
from llmsherpa.readers import LayoutPDFReader
from langchain.text_splitter import HTMLHeaderTextSplitter, TokenTextSplitter

import logging
from logger_config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)


class Ingestion:

    def __init__(self, path_or_url):
        self.path_or_url = path_or_url

    def extract(self):
        llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
        logger.info(f"Extracting from {self.path_or_url}")
        pdf_reader = LayoutPDFReader(llmsherpa_api_url)
        self.pdf = pdf_reader.read_pdf(path_or_url=self.path_or_url)
        logger.info(f"Extraction successful")

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
    
    def get_documents(self):
        logger.info(f"Getting documents...")
        headers = [
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3")
        ]

        html_splitter = HTMLHeaderTextSplitter(headers_to_split_on=headers, return_each_element=True)
        token_splitter = TokenTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 100,
        )

        documents = []
        
        sections = self.pdf.sections()
        for section in sections:
            content = section.to_html(include_children=True, recurse=True)
            splits = html_splitter.split_text(content)
            splits = token_splitter.split_documents(splits)
            documents.extend(splits)

        logger.info(f"Got {len(documents)} documents")
        
        return documents
    
    def get_mapped_sections(self):
        logger.info(f"Mapping sections to items...")
        all_headers = []

        sections = self.pdf.sections()
        for header in sections:
            all_headers.append(header.to_html(recurse=True))

        def strip_html_tags(html):
            return BeautifulSoup(html, "html.parser").get_text()

        mapped_sections = {}
        current_item = None
        for header in all_headers:
            text = strip_html_tags(header)
            if 'Item' in text or 'ITEM' in text:
                current_item = text
            else:
                if current_item:
                    mapped_sections[text] = current_item

        logger.info(f"Mapped {len(mapped_sections)} sections to items")
        return mapped_sections
    
    def add_item_metadata(self, documents, mapped_sections):
        logger.info(f"Adding item metadata...")
        final_documents = []
        for doc in documents:
            if 'Header 1' in doc.metadata:
                header1 = doc.metadata['Header 1']
                if header1 in mapped_sections:
                    doc.metadata['Item'] = mapped_sections[header1]
            elif 'Header 2' in doc.metadata:
                header2 = doc.metadata['Header 2']
                if header2 in mapped_sections:
                    doc.metadata['Item'] = mapped_sections[header2]
            elif 'Header 3' in doc.metadata:
                header3 = doc.metadata['Header 3']
                if header3 in mapped_sections:
                    doc.metadata['Item'] = mapped_sections[header3]

            final_documents.append(doc)

        logger.info(f"Added item metadata to {len(final_documents)} documents")
        return final_documents
    
    def ingest(self):
        self.extract()
        documents = self.get_documents()
        mapped_sections = self.get_mapped_sections()
        final_docs = self.add_item_metadata(documents=documents, mapped_sections=mapped_sections)

        chunks = []

        for doc in final_docs:
            chunk = {}
            chunk['content'] = doc['page_content']
            chunk['metadata'] = doc['metadata']
            chunks.append(chunk)

        logger.info("Ingestion Complete!!")
        return chunks


