from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), url()])
    open = StringField('Opening Time e.g 8AM', validators=[DataRequired()])
    close = StringField('Closing Time e.g 5:30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"])
    wifi_rating = SelectField('Wifi Strength Rating', validators=[DataRequired()], choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power = SelectField('Power Socket Availability', validators=[DataRequired()], choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods= ['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    row = []
    if form.validate_on_submit():
        with open("cafe-data.csv", 'a', encoding='UTF8') as file:
            file.write(f"\n"
                       f"{form.cafe.data}"
                       f",{form.location.data}"
                       f",{form.open.data}"
                       f",{form.close.data}"
                       f",{form.coffee_rating.data}"
                       f",{form.wifi_rating.data}"
                       f",{form.power.data}")
            return redirect(url_for('cafes'))
    print(row)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)

@app.route('/cafes', methods= ['GET', 'POST'])
def cafes():
    with open('cafe-data.csv', newline= '', encoding= "utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes= list_of_rows, length= len(list_of_rows), no_col = len(list_of_rows[0]))


if __name__ == '__main__':
    app.run(debug=True)
