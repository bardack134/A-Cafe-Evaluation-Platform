from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired()])
    open = StringField('Opening Time e.g 8AM', validators=[DataRequired()])
    close = StringField('Closing Time e.g 5:30PM', validators=[DataRequired()])
    rating = StringField('Coffee Rating', validators=[DataRequired()])
    wifi_rating = StringField('Wife Strength Rating', validators=[DataRequired()])
    Power_socket_availability = StringField('Power Socket Availability', validators=[DataRequired()])
    submit = SubmitField('Submit')



# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    
    form = CafeForm()
    
    if form.validate_on_submit():
        
        print("True is valid")
        print("True is valid")
        return render_template('index.html')
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    else:
        
        return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        
        csv_data = csv.reader(csv_file, delimiter=',')
        
        list_of_rows = []
        
        for row in csv_data:
            print(row)
            list_of_rows.append(row)
    print()        
    print(list_of_rows)      
    print()     
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
