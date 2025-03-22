from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch

app = FastAPI()

es = Elasticsearch([f"http://{ELASTICSEARCH_VM_IP}:9200"])

@app.get("/search")
def search_document(query: str = Query(..., min_length=1)):
    response = es.search(index="myindex", body={"query": {"match": {"text": query}}})
    return response["hits"]["hits"] if response["hits"]["hits"] else "No match found"

@app.post("/insert")
def insert_document(text: str = Query(..., min_length=1)):
    doc = {"text": text}
    es.index(index="myindex", body=doc)
    return {"message": "Inserted successfully!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9567)
