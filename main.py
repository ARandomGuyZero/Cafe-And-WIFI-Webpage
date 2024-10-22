"""
Coffee and Wifi

Author: Alan
Date: October 22nd, 2024

This script generates webpage where the user can add

"""
from csv import reader

from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

Bootstrap5(app)


class CafeForm(FlaskForm):
    """
    This cafeform has the data of the form, which is later rendered in the add.html file
    """
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired()])
    opening_time = StringField('Opening Time (e.g. 8AM)', validators=[DataRequired()])
    closing_time = StringField('Closing Time (e.g. 8PM)', validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Strength Rating", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"],
                              validators=[DataRequired()])
    power_rating = SelectField("Power Socket Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"],
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    """
    Home page for the app
    :return: Renders the html file index.html
    """
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    """
    Form page to add more apps
    :return: Renders the html file add.html
    """
    form = CafeForm()

    # If the user clicks on submit, it will append the new data to the cafe-data.csv file
    if form.validate_on_submit():
        # Opening the file, we append the new data
        with open("cafe-data.csv", mode="a", encoding="utf-8") as csv_file:
            csv_file.write(f"\n{form.cafe_name.data},"
                           f"{form.cafe_location.data},"
                           f"{form.opening_time.data},"
                           f"{form.closing_time.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data},")
        # Redirects to cafes once we finish
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    """
    Cafe page to show a list of the cafes saved by the user
    :return: Renders the html file cafes.html
    """
    # Opening the file, we get the data and save it in a list
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        # We read the data
        csv_data = reader(csv_file, delimiter=',')
        list_of_rows = []
        # For each row in csv_fata
        for row in csv_data:
            # We append the data
            list_of_rows.append(row)
    # Renders the cafes.html page and shows the list of rows
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
