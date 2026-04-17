from flask import Flask, render_template
from main import run_pipeline

app = Flask(__name__)

@app.route("/")
def home():
    results = run_pipeline()

    if results is None:
        results = []
    return render_template("index.html", results=results)
    
if __name__ == "__main__":
	app.run(debug=True)
