from flask import Flask, render_template, flash, redirect, url_for
from config import Config
from forms import Query
import pandas as pd
import finalModeling as fM
import getData as gD


app = Flask(__name__)
app.config.from_object(Config)



userCalc = []

@app.route('/', methods=['GET', 'POST'])
def index():
  form = Query()
  if form.validate_on_submit(): 

    usrCounty = form.usrCounty.data
    usrState = form.usrState.data
    usrAge = form.usrAge.data

    usrCounty = usrCounty.lower()
    usrState = usrState.lower()

    if 'county' in usrCounty: 
      usrCounty = usrCounty.replace('county', '')

    usrCounty = usrCounty.title().strip()
    usrState = usrState.title().strip()

    global userCalc

    print(usrAge, usrCounty, usrState)

    userCalc = fM.userInput(usrAge, usrCounty, usrState)
    
    if userCalc == 'error' or len(userCalc)!=3 :
      flash('Incorrect inputs! Make sure you spelled everything correctly and try again.')
    else:
      return redirect(url_for('query'))

  else:
    return render_template('index.html', index=gD.locations, form=form)


  return render_template('index.html', index=gD.locations, form=form)

@app.route('/query')
def query():
  return render_template('query.html', index=gD.locations, tables=userCalc[0], titles=userCalc[1], ageCol=userCalc[2])

@app.route('/about')
def about():
  return render_template('about.html')


if __name__ == '__main__':
  app.run()