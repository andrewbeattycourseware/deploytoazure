from flask import Flask,session, url_for, request, redirect, abort, jsonify, render_template
from BookDao import bookDao

app = Flask(__name__, static_url_path='', static_folder='staticpages')


@app.route('/')
def home():
    if not 'username' in session:
        return redirect(url_for('login'))

    return 'welcome ' + session['username'] +\
        '<br><a href="'+url_for('logout')+'">logout</a>'



@app.route('/books')
def getAll():
    return jsonify(bookDao.getAll())
# find By id


@app.route('/books/<int:ISBN>')
def findById(ISBN):
    return jsonify(bookDao.findById(ISBN))


@app.route('/books/searchtitle/<string:title>')
def searchbytitle(title):
    print(title)
    return jsonify(bookDao.searchbytitle(title))

# create
# curl -X POST -i -H "Content-Type:application/json" -d "{\"ISBN\":\"1234\",\"title\":\"test\", \"author\":\"some guy\", \"price\":123}" http://127.0.0.1:5000/books


@app.route('/books', methods=['POST'])
def create():

    if not request.json:
        abort(400)

    book = {
        "ISBN": request.json["ISBN"],
        "title": request.json["title"],
        "author": request.json["author"],
        "price": request.json["price"]
    }
    return jsonify(bookDao.create(book))

    return "served by Create "

#update
# curl -X PUT -i -H "Content-Type:application/json" -d "{\"Title\":\"new Title\", \"Price\":999}" -H "content-type:application/json" http://127.0.0.1:5000/books/1


@app.route('/books/<int:ISBN>', methods=['PUT'])
def update(ISBN):
    foundBook = bookDao.findById(ISBN)
    print(foundBook)
    if foundBook == {}:
        return jsonify({}), 404
    currentBook = foundBook
    if 'title' in request.json:
        currentBook['title'] = request.json['title']
    if 'author' in request.json:
        currentBook['author'] = request.json['author']
    if 'price' in request.json:
        currentBook['price'] = request.json['price']
    bookDao.update(currentBook)

    return jsonify(currentBook)

#delete
# curl -X DELETE http://127.0.0.1:5000/books/1


@app.route('/books/<int:ISBN>', methods=['DELETE'])
def delete(ISBN):
    bookDao.delete(ISBN)

    return jsonify({"done": True})


@app.route('/books/display/<int:ISBN>')
def display(ISBN):
    book = bookDao.findById(ISBN)
    print(book)
    return render_template('displayxss.html', title=book['title'])


@app.route('/books/baddisplay/<int:ISBN>')
def baddisplay(ISBN):
    book = bookDao.findById(ISBN)
    print(book)
    return '<html><body> you like '+ book['title'] + '</body></html>'


@app.route('/books/badhello')
def badhello():
    name = request.args.get('username')
    return '<html><body> hello ' + name + '</body></html>'


#### login urls
app.secret_key = 'someSecrtetasdrgsadfgsdfg3ko'


@app.route('/login')
def login():
    return '<h1> login</h1> ' +\
        '<button>' +\
        '<a href="'+url_for('proccess_login')+'">' +\
        'login' +\
        '</a>' +\
        '</button>'

@app.route('/processlogin')
def proccess_login():
    #check credentials
    #if bad redirect to login page again

    #else
    print("logging in")
    session['username'] = "I dunno2"
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    print(session['username'])
    session.pop('username', None)
    if 'username' in session:
        print('o no')
        print(session['username'])
    else:
        print("nowt here")
    #session['username'] ='3434'
    #print(session['username'])

    #return 'done'
    return redirect(url_for('home'))


@app.route('/secure')
def getData():
    if not 'username' in session:
        abort(401)

    print(session['username'])
    return '{"data":"Top Secret stuff"}'





if __name__ == "__main__":
    app.run(debug=True)
