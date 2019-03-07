from flask import Flask, request, render_template, Response
from inferencer import infer, getAllImageURIs
import time
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form.html')

@app.route('/progress')
def progress():
   def generate():
      count = 200
      print('THIS IS COUNT: {}'.format(count))
      x = 0
      iterator = 0
      while x <= 100:
         yield "data:" + str(x) + "\n\n"
         iterator += 1
         print('THIS IS ITERATOR: {}'.format(iterator))
         if iterator >= count/100:
            x += 1
            iterator = 0
         time.sleep(2)

   return Response(generate(), mimetype= 'text/event-stream')

@app.route('/submit', methods=['POST'])
def submit():
   rawInput = request.form['textbox']

   formattedInput = rawInput.replace('\r\n',' ').split()

   allImageURIs = getAllImageURIs(formattedInput)
   progress()
   #print('THERE ARE {} IMAGES IN THIS MANIFEST'.format(len(allImageURIs)))
   #results = infer(formattedInput)  
   
   # USE THIS results TO TEST DISPLAYING IMAGES
   results = ['https://previews.123rf.com/images/lufimorgan/lufimorgan1509/lufimorgan150900005/45154060-blue-eyes-siberian-husky-puppy-lyingand-looking-on-green-grass.jpg', 'https://ih1.redbubble.net/image.451672470.1427/flat,550x550,075,f.u4.jpg']

   return render_template('results.html', imgURIs = results)

if __name__ == '__main__':
   app.run(debug=True)
