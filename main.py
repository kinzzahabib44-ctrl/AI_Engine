from pathlib import Path
from datetime import datetime
from Document_loading.document_loader import (
    ensure_file,
    convert_to_pdf,
    iter_pdf_pages,
    load_csv
)
from Chunking.chunking import chunk_documents
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

SOURCE_PATH = r"D:\Softoo\ML Task\AI_Engine\test_files\sample.pptx"
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.txt', '.ppt', '.pptx', '.csv']
all_docs = []
source = Path(SOURCE_PATH)
processed_files = []

if source.is_file():
    files_to_process = [source]
elif source.is_dir():
    files_to_process = [f for f in source.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]
else:
    raise FileNotFoundError(f"Path not found: {SOURCE_PATH}")

logging.info(f"Found {len(files_to_process)} files to process.")

for file_path in files_to_process:
    try:
        file_path = ensure_file(file_path)
    except (FileNotFoundError, IsADirectoryError) as e:
        logging.warning(e)
        continue

    loaded_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ext = file_path.suffix.lower()

    if ext == ".csv":
        docs = load_csv(file_path)  # Already returns list of dicts
    else:
        pdf_path = convert_to_pdf(file_path)
        docs = list(iter_pdf_pages(pdf_path))
    docs = [d for d in docs if d.get("page_content", "").strip()]
    if not docs:
        logging.warning(f"Document {file_path.name} is empty, skipping.")
        continue

    all_docs.extend(docs)
    processed_files.append({
        "file_path": file_path,
        "loaded_date": loaded_date,
        "total_pages": len(docs)
    })

logging.info("\n================ DOCUMENT SUMMARY ================\n")
for f in processed_files:
    logging.info(f"Processed on: {f['loaded_date']}")
    logging.info(f"File Name: {f['file_path'].name}")
    logging.info(f"Directory: {f['file_path'].resolve()}")
    logging.info(f"Total Pages/Rows: {f['total_pages']}")
    logging.info("Status: Document Ready for processing")
    
logging.info("=================================================\n")

logging.info(f"Total pages/rows loaded from folder: {len(all_docs)}")

chunks = chunk_documents(
    all_docs,
    chunk_size=500,
    chunk_overlap=100
)

logging.info(f"Total chunks created: {len(chunks)}")

if chunks:
    print("\nSample Chunk:\n")
    sample = chunks[0]
    print(f"Text:\n{sample['text']}\n")
    print(f"File Name: {sample['metadata'].get('file_name')}")
else:
    print("No chunks were created.")
