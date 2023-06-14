from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database'
)

# Create the users table if it doesn't exist
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (username VARCHAR(255), password VARCHAR(255))''')
conn.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password))
        conn.commit()
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                       (username, password))
        user = cursor.fetchone()
        if user:
            return f'Logged in as {username}'
        return 'Invalid username or password'
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
