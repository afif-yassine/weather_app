#installation

pip install -r requirements.txt
pip install fastapi
uvicorn main:app --reload --port 5000
DOCS: http://127.0.0.1:5000/docs

#test
python -m pytest -v
