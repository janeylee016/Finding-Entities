from flask import Flask, render_template
from entities.main import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'greenfield'
app.register_blueprint(main, url_prefix="")

@app.route('/')
def home():
    return "<p>Test</p>"

if __name__ == "__main__":
    app.run(debug=True)