from flask_app import app
from flask import render_template, redirect, request, session, flash, Flask
from flask_app.models.email_model import User



# Home Route
@app.route('/')
def input_home():
    return render_template("index.html")

# route to validate submitted data
@app.route('/process', methods = ['POST'])
def process_submit():
    if not User.validate_email(request.form):
        return redirect('/')
    # insert form into becoming the user
    emails = User.save_submission(request.form)

    return redirect('/success')

# route to show all validated emails
@app.route('/success')
def validated_emails():
    all_emails = User.get_all()
    return render_template('success.html', all_emails = all_emails)

