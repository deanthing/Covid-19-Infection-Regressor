# covid19_outbreak_by_age_predictor

Link to live project: http://www.virustrackercovid19.com/

This project uses a Flask framework to deploy to the web and uses Python data analysis techniques. Data is read from a number of sources including:
- https://www.google.com/covid19/mobility/
- Census data: living conditions, age-sex-data, population density data
- Confirmed covid case data https://pipedream.com/@pravin/http-api-for-latest-jhu-csse-2019-ncov-wuhan-coronavirus-data-set-p_G6CLVM

The python environment utilises sklearn models and pandas to sort and store data.

Python requirements:
astroid==2.3.3
certifi==2020.4.5.1
chardet==3.0.4
click==7.1.1
cycler==0.10.0
Flask==1.1.2
Flask-WTF==0.14.3
geographiclib==1.50
geopy==1.21.0
gunicorn==20.0.4
heroku==0.1.4
idna==2.9
isort==4.3.21
itsdangerous==1.1.0
Jinja2==2.11.2
joblib==0.14.1
kiwisolver==1.2.0
lazy-object-proxy==1.4.3
MarkupSafe==1.1.1
matplotlib==3.2.1
mccabe==0.6.1
numpy==1.18.3
pandas==1.0.3
pickle-mixin==1.0.2
pylint==2.4.4
pyparsing==2.4.7
python-dateutil==2.8.1
pytz==2019.3
requests==2.23.0
scikit-learn==0.22.2.post1
scipy==1.4.1
six==1.14.0
sklearn==0.0
urllib3==1.25.9
Werkzeug==1.0.1
wrapt==1.11.2
WTForms==2.3.1
