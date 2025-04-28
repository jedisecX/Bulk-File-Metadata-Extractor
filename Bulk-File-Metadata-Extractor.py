#!/usr/bin/env python3
# JediSecX Bulk File Metadata Extractor
# jedisec.com | jedisec.us | jedisec.cloud | jedisec.online | jedisec.me

import os
import sys
import exifread
import PyPDF2
from docx import Document

def extract_exif(file_path):
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
            return {tag: str(tags[tag]) for tag in tags}
    except Exception as e:
        return {"Error": str(e)}

def extract_pdf_metadata(file_path):
    try:
        with open(file_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            return pdf.metadata
    except Exception as e:
        return {"Error": str(e)}

def extract_docx_metadata(file_path):
    try:
        doc = Document(file_path)
        props = doc.core_properties
        return {
            "Author": props.author,
            "Title": props.title,
            "Created": props.created,
            "Last Modified": props.modified
        }
    except Exception as e:
        return {"Error": str(e)}

def scan_folder(folder):
    print(f"[*] Scanning {folder} for metadata...\n")
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            print(f"[*] Analyzing: {path}")
            ext = file.lower().split('.')[-1]

            if ext in ["jpg", "jpeg", "png"]:
                metadata = extract_exif(path)
            elif ext == "pdf":
                metadata = extract_pdf_metadata(path)
            elif ext == "docx":
                metadata = extract_docx_metadata(path)
            else:
                continue

            if metadata:
                for key, value in metadata.items():
                    print(f"    {key}: {value}")
                print("")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/folder")
        sys.exit(1)
    scan_folder(sys.argv[1])
