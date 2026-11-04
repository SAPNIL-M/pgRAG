import pymupdf

def extract_text_from_pdf(pdf_path:str)->tuple[int,list[dict]]:
    book1=[]
    with pymupdf.open(pdf_path) as doc:
        for page_num,page in enumerate(doc,start=1): # type: ignore
            raw_text=page.get_text()
            cleaned_text=" ".join(raw_text.split())
            book1.append({"page_number":page_num,"text":cleaned_text})
        total_pages = doc.page_count
    return total_pages,book1