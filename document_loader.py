import logging
import tkinter as tk
from tkinter import filedialog
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
import json
import csv

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return Document(page_content=json.dumps(data))

def load_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        content = "\n".join([",".join(row) for row in reader])
        return Document(page_content=content)

def load_code_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return Document(page_content=content)

def load_documents(config):
    choice = input("Choose document loading method (1: Specify files, 2: Preload files, 3: Load directory, 4: None): ")
    file_docs = []

    if choice == '1':
        file_paths = filedialog.askopenfilenames(title="Select files", filetypes=[(ft.split(': ')[0], ft.split(': ')[1]) for ft in config['document_loading']['filetypes']])
        for file_path in file_paths:
            try:
                if file_path.endswith(".txt"):
                    logging.info(f"Loading {file_path}")
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        file_docs.append(Document(page_content=content))
                elif file_path.endswith(".pdf"):
                    logging.info(f"Loading {file_path}")
                    pdf_loader = PyPDFLoader(file_path)
                    file_docs.extend(pdf_loader.load())
                elif file_path.endswith(".json"):
                    logging.info(f"Loading {file_path}")
                    file_docs.append(load_json(file_path))
                elif file_path.endswith(".csv"):
                    logging.info(f"Loading {file_path}")
                    file_docs.append(load_csv(file_path))
                elif file_path.endswith((".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".rb", ".php", ".sh")):
                    logging.info(f"Loading {file_path}")
                    file_docs.append(load_code_file(file_path))
            except Exception as e:
                logging.error(f"Error loading file {file_path}: {e}")

    elif choice == '2':
        for file_path in config['document_loading']['predefined_paths']:
            try:
                if file_path.endswith(".txt"):
                    logging.info(f"Loading {file_path}")
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        file_docs.append(Document(page_content=content))
                elif file_path.endswith(".pdf"):
                    logging.info(f"Loading {file_path}")
                    pdf_loader = PyPDFLoader(file_path)
                    file_docs.extend(pdf_loader.load())
                elif file_path.endswith(".json"):
                    logging.info(f"Loading {file_path}")
                    file_docs.append(load_json(file_path))
                elif file_path.endswith(".csv"):
                    logging.info(f"Loading {file_path}")
                    file_docs.append(load_csv(file_path))
                elif file_path.endswith((".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".rb", ".php", ".sh")):
                    logging.info(f"Loading {file_path}")
                    file_docs.append(load_code_file(file_path))
            except Exception as e:
                logging.error(f"Error loading predefined file {file_path}: {e}")

    elif choice == '3':
        directory_path = filedialog.askdirectory(title="Select directory")
        try:
            directory_loader = DirectoryLoader(directory_path)
            file_docs.extend(directory_loader.load())
        except Exception as e:
            logging.error(f"Error loading directory {directory_path}: {e}")

    elif choice == '4':
        logging.info("No documents selected for loading.")
        return None

    else:
        raise ValueError("Invalid choice")

    if not file_docs:
        raise ValueError("No documents loaded from local files.")

    logging.info("Splitting and embedding documents...")
    text_splitter = RecursiveCharacterTextSplitter()
    split_file_docs = text_splitter.split_documents(file_docs)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = FAISS.from_documents(split_file_docs, embeddings)

    logging.info("Data loaded and indexed successfully.")
    return vector_store
