from flask import Flask, request, render_template
from inferencer import infer

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
   rawInput = request.form['text']

   formattedInput = rawInput.replace('\r\n',' ').split()

   return('You got: {}'.format(infer(formattedInput)))
   


if __name__ == '__main__':
   app.run()