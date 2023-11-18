from functools import wraps

from bson.objectid import ObjectId
from flask import Flask, redirect, render_template, request, session, url_for

from banco import Connection

connection = Connection()

app = Flask(__name__)
app.secret_key = "xmqwoidmwqo"  

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        isLoggedIn = 'username' in session
        if not isLoggedIn:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/', methods=['GET'])
@login_required
def index():
    quantity, filter = request.args.get('quantity'), request.args.get('filter') 
        
    products = connection.get_produto()
    
    if quantity and filter:
        if filter == 'greater':
            products = connection.filter_by_quantity_greater_than(products, int(quantity))
        elif filter == 'lesser':
            products = connection.filter_by_quantity_lesser_than(products, int(quantity))
      

    return render_template('index.html', username=session['username'], products=products)


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
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/product/new', methods=['POST', 'GET'])
@login_required
def add():
    if request.method == 'POST':
        new_produto = {
            'armazem': ObjectId(request.form['storage']),
            'categoria': ObjectId(request.form['category']),
            'nome': request.form['name'],
            'preco': int(request.form['price']),
            'quantidade': int(request.form['quantity']),
        }
        
        connection.post_produto(new_produto)
        
        return redirect(url_for('index'))
    return render_template('new_product.html', categories=connection.get_categoria(), storages=connection.get_armazem())

@app.route('/product/<id>/delete', methods=['GET'])
@login_required
def delete(id):
    connection.delete_produto(id)
    return redirect(url_for('index'))

@app.route('/category/new', methods=['POST', 'GET'])
@login_required
def add_category():
    if request.method == 'POST':
        new_categoria = {
            'nome': request.form['name']
        }
        
        connection.post_categoria(new_categoria)
        
        return redirect(url_for('index'))
    return render_template('new_category.html')

@app.route('/storage/new', methods=['POST', 'GET'])
@login_required
def add_storage():
    if request.method == 'POST':
        new_armazem = {
            'nome': request.form['name'],
            "endereco": request.form['address']
        }
        
        connection.post_armazem(new_armazem)
        
        return redirect(url_for('index'))
    return render_template('new_storage.html')

if __name__ == '__main__':
    app.run(debug=True)