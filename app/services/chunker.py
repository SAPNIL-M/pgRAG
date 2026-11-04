from spacy.lang.en import English
nlp = English()
nlp.add_pipe("sentencizer")

def chunk_pages(page:list[dict], chunk_size:int=10, min_chars:int = 30)-> list[dict]:
    
    chunk_index=0
    all_chunks=[]


    for item in page:
        doc=nlp(item["text"])
        sentences = [str(sent) for sent in doc.sents]

        for i in range(0,len(sentences),chunk_size):
            chunked_text =" ".join(sentences[i:i+chunk_size]).strip()
            if len(chunked_text)> min_chars:
                all_chunks.append({
                    "chunk_index":chunk_index,  
                    "page_number": item["page_number"],
                    "text": chunked_text
                })
                chunk_index+=1
    return all_chunks