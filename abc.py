from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/libmange'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'ssl': {"disabled": True}
    }
}
db = SQLAlchemy(app)

class Books(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    bookid = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.Boolean, default=True)

class User_record(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    bookid = db.Column(db.String(20), unique=True, nullable=False)
    contact = db.Column(db.Integer, nullable=False)


@app.route('/')
def show_books():
    books = Books.query.all()
    return render_template('books.html',books=books)


@app.route('/newbooks', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        bookid = request.form['bookid']
        title = request.form['title']
        author = request.form['author']
        availability = request.form.get('availability') == 'on'

        new_book = Books(bookid=bookid, title=title, author=author, availability=availability)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('show_books'))

    return render_template('book_form.html')


@app.route('/books/edit/<int:sno>', methods=['GET', 'POST'])
def update_book(sno):
    book = Books.query.get_or_404(sno)
    if request.method == 'POST':
        book.availability = request.form.get('availability') == 'on'
        db.session.commit()
        return redirect(url_for('show_books'))

    return render_template('book_form.html', book=book)


@app.route('/books/delete/<int:sno>', methods=['POST'])
def delete_book(sno):
    book = Book.query.get_or_404(sno)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('show_books'))

@app.route('/userrecords')
def show_user_records():
    user_records = User_record.query.all()
    return render_template('userrecords.html', user_records=user_records)


@app.route('/userrecords/new', methods=['GET', 'POST'])
def add_user_record():
    if request.method == 'POST':
        userid = request.form['userid']
        name = request.form['name']
        bookid = request.form['bookid']
        contact = request.form['contact']

        new_record = User_record(userid=userid, name=name, bookid=bookid, contact=contact)
        db.session.add(new_record)
        db.session.commit()

        return redirect(url_for('show_user_records'))

    return render_template('user_form.html')


@app.route('/userrecords/edit/<int:sno>', methods=['GET', 'POST'])
def update_user_record(sno):
    user_record = UserRecord.query.get_or_404(sno)
    if request.method == 'POST':
        user_record.bookid = request.form['bookid']
        db.session.commit()
        return redirect(url_for('show_user_records'))

    return render_template('user_form.html', user_record=user_record)

@app.route('/userrecords/delete/<int:sno>', methods=['POST'])
def delete_user_record(sno):
    user_record = UserRecord.query.get_or_404(sno)
    db.session.delete(user_record)
    db.session.commit()
    return redirect(url_for('show_user_records'))

if __name__ == '__main__':
    app.run(debug=True)