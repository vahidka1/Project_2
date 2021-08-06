from flask import Flask , render_template , request , redirect , url_for 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/project2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Register(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(12))
    
@app.route("/")
def index():
    result = Register.query.all()
    return render_template('home.html',result=result)

@app.route("/register/")
def register():
    return render_template('register.html')

@app.route("/process", methods=["POST","GET"])
def process():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    register_user= Register(name = first_name ,lastname = last_name,email = email,phone = phone)
    db.session.add(register_user)
    db.session.commit()
    #return render_template('home.html',first_name=first_name,last_name=last_name,email=email,phone=phone)
    return redirect(url_for('index'))
@app.route("/delete/<int:id>")
def delete(id):
    user_delete = Register.query.get_or_404(id)
    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "There was problem with deleting"

@app.route("/edit/<int:id>", methods=["POST","GET"])
def edit(id):
    user_edit = Register.query.get_or_404(id)
    if request.method == "POST":
        user_edit.name = request.form['name']
        user_edit.lastname = request.form['lastname']
        user_edit.email = request.form['email']
        user_edit.phone = request.form['phone']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "There was problem with editing"
    else:
        return render_template('edit.html',user_edit=user_edit )

@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        req = request.args.get('req')
        r = Register.query.filter(Register.name == req)
        return render_template('home.html',result=r )
    except:
        return "There was problem with searching"
if __name__ == '__main__':
    app.run(debug=True)


