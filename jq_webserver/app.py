from flask import Flask, request, render_template
from inferencer import infer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
   rawInput = request.form['textbox']
   formattedInput = rawInput.replace('\r\n',' ').split()
   results = infer(formattedInput)  
   return render_template('results.html', imgURIs = results)

if __name__ == '__main__':
   app.run()