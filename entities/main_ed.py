from flask import Blueprint, render_template, request, session, redirect, url_for, flash, make_response, jsonify

from werkzeug.utils import secure_filename

from entities.location import rule3
from entities.address import pred

main = Blueprint("main", __name__, static_folder="static", template_folder="templates")

@main.route('/home')
@main.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST" and ("input-submit" in request.form):
        input = request.form['input']

        if input:
            return redirect(url_for('main.results', input=input))
        else:
            flash("No inputs given. Please give your inputs in the text box below.")

    if (request.method == "POST") and ("file-submit" in request.form):    
        file = request.files['filename']
        if file:
            file = request.files['filename']
            data = []
            filename = secure_filename(file.filename)
            for line in file:
                data.append(line) 
            text = ''.join(map(bytes.decode,data))
  
            return redirect(url_for('main.results', text=text))
        else:
            flash("Please upload a file")
    
    return render_template("home.html")




@main.route('/results', methods=["POST", "GET"])
def results():
    input = request.args.get('input') #input text
    loc, response = rule3(input)
    locations = pred(input)
    text = request.args.get('text') # file upload text
    res = {}
    res['loc'] = locations
    res['text'] = input
    resp = jsonify(res)
    return render_template('results_file.html', resp=resp)

