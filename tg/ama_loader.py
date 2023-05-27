from tvariables import *

ama_file_name = 'files/ama.txt'

ama_loader = ''
if ama_file_name.endswith('.pdf'): ama_loader = PyPDFLoader(ama_file_name)
if ama_file_name.endswith('.txt') and ama_file_name != 'system_prompt.txt': ama_loader = TextLoader(ama_file_name, encoding='utf8')
if ama_file_name.endswith('.docx') or ama_file_name.endswith('.doc'): ama_loader = UnstructuredWordDocumentLoader(ama_file_name)
if ama_file_name.endswith('.pptx') or ama_file_name.endswith('.ppt'): ama_loader = UnstructuredPowerPointLoader(ama_file_name)

if ama_loader:
    ama_documents = ama_loader.load()
    ama_text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    ama_texts = ama_text_splitter.split_documents(ama_documents)
    ama_db = Chroma.from_documents(ama_texts, embeddings)
    ama_retriever = ama_db.as_retriever()
    ama_qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=ama_retriever)

    logging.info(f"AMA loaded from {ama_file_name}")