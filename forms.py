from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

class Query(FlaskForm):
  usrCounty = StringField("County*", [Required('County Required')], render_kw={"placeholder": "e.g. 'Los Angeles'"})
  usrState = StringField("State*", [Required('State Required')], render_kw={"placeholder": "e.g. 'California'"})
  usrAge = IntegerField("Age*", [Required('Age Required/Must be a number')], render_kw={"placeholder": "e.g. '21'"})
  submit = SubmitField('Submit', validators=[Required()])