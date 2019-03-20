from flask import Flask, render_template, request

from mbta_helper import find_stop_near

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def calculate():
   if request.method == 'POST':
       Location = request.form['location']
       Near_stop,wheelchair = find_stop_near(Location)
       # Country Code = float(request.form['country code'])
       # we want results from api
       if Near_stop and wheelchair:
           return render_template('mbta_result.html',location=Location,near_stop=Near_stop,wheelchair=wheelchair)
       else:
           return render_template('mbta_form.html',error=True)
   return render_template('mbta_form.html', error=None)


