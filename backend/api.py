from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/health")
def health_check():
    return {"status": "ok"}
