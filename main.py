import pprint
from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import DateTimeField, SelectField, StringField, SubmitField, URLField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import csv
import pandas as pd

# Create a Flask application instance
app = Flask(__name__)

 # Set the secret key for form security
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Initialize Bootstrap5 for the Flask app
Bootstrap5(app)


# Define a form class for cafe data input using Flask-WTF
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    
    
    location = URLField('Cafe Location on Google Maps (URL)', validators=[DataRequired()])
    
    
    open = StringField('Opening Time e.g 8AM', validators=[DataRequired()])
    
    
    close = StringField('Closing Time e.g 5:30PM', validators=[DataRequired()])
    
    
    coffee_rating = SelectField('Coffee Rating', validators=[DataRequired()], choices=[('', 'Select'), ('☕️', '☕️'), ('☕️☕️', '☕️☕️'), ('☕️☕️☕️', '☕️☕️☕️'), ('☕️☕️☕️☕️', '☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'),  ],  validate_choice=True)
    
    
    wifi_rating = SelectField('Wife Strength Rating', validators=[DataRequired()], choices=[('', 'Select'), ('☕️', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪'),  ],  validate_choice=True)
    
    
    power_socket_availability = SelectField('Power Socket Availability', validators=[DataRequired()], choices=[('', 'Select'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'),  ],  validate_choice=True)
    
    
    # Submit button
    submit = SubmitField('Submit')



# Render the homepage template
@app.route("/")
def home():
    
    return render_template("index.html")



@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    
    # Instantiate the CafeForm
    form = CafeForm()
    
    if form.validate_on_submit():
        
        # Collect form data
        cafe = form.cafe.data 
        location = form.location.data 
        open = form.open.data 
        close = form.close.data 
        coffee_rating = form.coffee_rating.data 
        wifi_rating = form.wifi_rating.data 
        power_socket_availability = form.power_socket_availability.data 
        
        # Prepare data as a list of tuple
        data=[(cafe, location, open, close, coffee_rating, wifi_rating, power_socket_availability)]
        
        # for bugging proccess
        print(data)
        
        # Converting lists of tuples into pandas Dataframe.
        new_dataframe= pd.DataFrame(data, index=None,
                        columns=['Cafe Name', 'Location', 'Open', 'Close', 'Coffee', 'Wifi', 'Power'])
        
        #for buggin proccess
        print()
        print(f"new data:\n {new_dataframe}")
        
        
        try:
            #  Read existing data from CSV file into a DataFrame.
            old_dataframe = pd.read_csv('cafe-data.csv')
            
            print()
            print(f"old data:\n {old_dataframe}")
                
            # Concatenate old and new data
            all_data_frame=pd.concat([old_dataframe, new_dataframe], ignore_index=True)
            
            print()
            print(f'all data together: \n {all_data_frame}')
            
            # Write all data back to the CSV file
            all_data_frame.to_csv('cafe-data.csv',  index=False)
            
            return redirect(url_for('cafes'))
        
        except:
            
            # If the CSV file does not exist, create it with the new data
            new_dataframe.to_csv('cafe-data.csv', index=False)
            
            return redirect(url_for('cafes'))    
   
    else:
        
        # Render the form template
        return render_template('add.html', form=form)
        
        


@app.route('/cafes')
def cafes():
    
    # Open the CSV file and read its contents
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        
        csv_data = csv.reader(csv_file, delimiter=',')
        
        list_of_rows = []
        
        for row in csv_data:
            
            # print(row)
            
            list_of_rows.append(row)
            
    # print()        
    # print(list_of_rows)      
    # print()   
    
    # Render the cafes template with the data  
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
