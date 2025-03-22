from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse
import requests
import os

app = FastAPI()

backend_url = f"http://{BACKEND_VM_IP}:9567"

html_content = f"""
<!DOCTYPE html>
<html>
<head><title>Elasticsearch Frontend</title></head>
<body>
    <h1>Elasticsearch Frontend</h1>
    <input type="text" id="docInput" placeholder="Enter document text"><br><br>
    <button onclick="insertDocument()">Insert Document</button>
    <input type="text" id="searchInput" placeholder="Enter search query"><br><br>
    <button onclick="searchDocument()">Search Document</button>
    <p id="output"></p>
    <script>
        async function insertDocument() {{
            let text = document.getElementById('docInput').value;
            let response = await fetch('{backend_url}/insert', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify({{ text: text }})
            }});
            let data = await response.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }}
        async function searchDocument() {{
            let query = document.getElementById('searchInput').value;
            let response = await fetch('{backend_url}/search?query=' + encodeURIComponent(query));
            let data = await response.json();
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }}
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=html_content)

@app.post("/insert")
async def insert_document(request: Request):
    data = await request.json()
    response = requests.post(f"{backend_url}/insert", json=data)
    return response.json()

@app.get("/search")
async def search_document(query: str):
    response = requests.get(f"{backend_url}/search", params={"query": query})
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=9567)
