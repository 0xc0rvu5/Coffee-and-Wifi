import csv, os
from csv import writer
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, url_for
from wtforms import StringField, SubmitField, SelectField, validators


#initiate global variables
SECRET_KEY = os.urandom(32)
APP = Flask(__name__, template_folder='templates', static_folder='static')
APP.config['SECRET_KEY'] = SECRET_KEY


#initiate bootstrap functionality
Bootstrap(APP)


class CafeForm(FlaskForm):
    '''Add a cafe and its relevant details to the `cafe-data.csv` file and display the content at `cafes` endpoint.'''
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), validators.url()])
    opening_time = StringField('Opening Time e.g. 2PM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 9:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=[('☕️'), ('☕️ ☕️'), ('☕️ ☕️ ☕️'), ('☕️ ☕️ ☕️ ☕️'), ('☕️ ☕️ ☕️ ☕️ ☕️')])
    wifi_strength_rating = SelectField('Wifi Strength Rating', choices=[('💪'), ('💪 💪'), ('💪 💪 💪'), ('💪 💪 💪 💪'), ('💪 💪 💪 💪 💪')])
    power_outlet_availability = SelectField('Power Outlet Availability', choices=[('🔌'), ('🔌 🔌'), ('🔌 🔌 🔌'), ('🔌 🔌 🔌 🔌'), ('🔌 🔌 🔌 🔌 🔌')])
    submit = SubmitField('Submit')


# all Flask routes below
@APP.route("/")
def home():
    return render_template("index.html")


@APP.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    #if form data is valid, append data to csv file and clear content from form
    if form.validate_on_submit():
        #gather form data into a list
        list = [form.cafe.data, form.location.data, form.opening_time.data, form.closing_time.data, form.coffee_rating.data, form.wifi_strength_rating.data, form.power_outlet_availability.data]
        #append form data to csv file
        with open('cafe-data.csv', 'a') as f:
            writer_object = writer(f)
            writer_object.writerow(list)
            f.close()
        #clear content from form upon completion
        return redirect(url_for('add_cafe'))
    return render_template('add.html', form=form)


@APP.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    APP.run(debug=True)