
from llama_index.node_parser.extractors import (
    MetadataExtractor,
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
    EntityExtractor,
    MetadataFeatureExtractor,
)
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser import SimpleNodeParser
from llama_index import SimpleDirectoryReader

document = SimpleDirectoryReader("data/apple").load_data()

print(len(document[0].text))
chunk_size = len(document[0].text) // 25

text_splitter = TokenTextSplitter(separator=" ", chunk_size=chunk_size, chunk_overlap=chunk_size//10)
metadata_extractor = MetadataExtractor(
    extractors=[
        # TitleExtractor(),
        # SummaryExtractor(),
        KeywordExtractor(keywords=1),
        # QuestionsAnsweredExtractor(questions=3),
    ],
)

node_parser = SimpleNodeParser.from_defaults(
    text_splitter=text_splitter,
    metadata_extractor=metadata_extractor,
)
# assume documents are defined -> extract nodes
nodes = node_parser.get_nodes_from_documents(document)
print(len(nodes))
print(nodes[0].metadata)
print(nodes[0])
print(nodes[1].metadata)
print(nodes[1])
