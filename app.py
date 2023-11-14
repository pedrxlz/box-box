from flask import Flask, redirect, render_template, request, session, url_for

from banco import Connection

connection = Connection()

app = Flask(__name__)
app.secret_key = "xmqwoidmwqo"  


@app.route('/', methods=['GET'])
def index():
    isLoggedIn = 'username' in session
    
    if isLoggedIn:
        products = connection.get_produto()
        
        return render_template('index.html', username=session['username'], products=products)

    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        result = connection.register(request.form['name'], request.form['username'], request.form['pass'])
        
        if result:
            return redirect(url_for('login'))
        
        return 'That username already exists!'
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        result = connection.login(request.form['username'], request.form['pass'])

        if result:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)