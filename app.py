from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'your_secret_key'

# Data file to store responses
data_file = "valentine_data.json"

# Route for main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/next', methods=['POST'])
def next_page():
    username = request.form['username']
    sender = request.form['sender']
    
    # Store the data in the session
    session['username'] = username
    session['sender'] = sender

    # Store the data in a temporary file for later use
    with open(data_file, 'a') as file:
        file.write(f"User: {username}, Sender: {sender}\n")

    return redirect('/question')

# Route for question page
@app.route('/question')
def question():
    # Check if 'username' and 'sender' are in the session
    if 'username' not in session or 'sender' not in session:
        return redirect('/')
    
    return render_template('question.html')

# Route to handle the answer ('yes' or 'no')
@app.route('/answer', methods=['POST'])
def answer():
    response = request.form['response']
    
    # Retrieve the username and sender from the session
    username = session['username']
    sender = session['sender']

    if response == 'yes':
        with open(data_file, 'a') as file:
            file.write(f"User: {username}, Sender: {sender}, Accepted: Yes\n")
        return redirect('/love')
    else:
        with open(data_file, 'a') as file:
            file.write(f"User: {username}, Sender: {sender}, Rejected: Nuh uh\n")
        return redirect('/funny')

# Route for love page
@app.route('/love')
def love():
    return render_template('love.html')

# Route for funny page
@app.route('/funny')
def funny():
    return render_template('funny.html')

if __name__ == '__main__':
    app.run(debug=True)
