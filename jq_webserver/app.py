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
   
   #USE THIS results TO TEST DISPLAYING IMAGES
   #results = ['https://previews.123rf.com/images/lufimorgan/lufimorgan1509/lufimorgan150900005/45154060-blue-eyes-siberian-husky-puppy-lyingand-looking-on-green-grass.jpg', 'https://ih1.redbubble.net/image.451672470.1427/flat,550x550,075,f.u4.jpg']

   return render_template('results.html', imgURIs = results)


if __name__ == '__main__':
   app.run()