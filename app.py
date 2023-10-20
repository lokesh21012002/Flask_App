from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
# app.app_context().push()
# 
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(3000),nullable=False)
    completed = db.Column(db.Boolean,nullable=False)

    # def __init__(self,title,description,completed):
    #     self.title=title
    #     self.description=description
    #     self.completed=completed
    #     db.session.add(self)
    #     db.session.commit()
    #     db.session.close()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    password=db.Column(db.String(200))


@app.route("/login",methods=["POST","GET"])

def login():

    if request.method=="POST":
        user_id=int(request.form.get("user_id"))
        password=request.form.get("password")

        print(user_id,password)
        users=list(User.query.with_entities(User.user_id).all())

        # print(users)
        # user=db.session.query(User).filter_by(user_id=user_id)
        # print(user)
        # print(len(user))
        # print(user)
        # print((user_id)  not  in users)

        if (user_id,) not in users:
            # redirect(url_for("signup"))
            return redirect(url_for("signup"))
        
        else:
            with app.app_context():
                user=User.query.filter_by(user_id=user_id).first()
                if user and user.password==password:
                    return redirect(url_for("index"))
                else:
                    # print("invalid")
                    return render_template("login.html",isValid="Invalid username or password")
    
    return render_template("login.html")

    # if request.method=="POST":
    #     user_id=request.form.get("user_id")
    #     password=request.form.get("password")
        



    #     with app.app_context():
    #         user=User.query.filter_by(user_id=user_id).first()
    #         if user and user.password==password:
    #             return redirect(url_for("index"))
    # return render_template("login.html")

@app.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":
        user_id=int(request.form.get("user_id"))
        password=request.form.get("password")
        users=list(User.query.with_entities(User.user_id).all())
        if (user_id,) in users:
            return render_template("signup.html",msg="user already exist")

        # user=db.session.query(User).filter(user_id=user_id)
        with app.app_context():
                new_user=User(user_id=user_id,password=password)
                db.session.add(new_user)
                db.session.commit()
        return redirect(url_for("login"))
    

    return render_template("signup.html")
    #     if user is None:
            
            
    #         with app.app_context():
    #             new_user=User(password=password)
    #             db.session.add(new_user)
    #             db.session.commit()
    #         return redirect(url_for("login"))
    #     else:
    #         return render_template("login.html")
    
    # return render_template("signup.html")    

    # if request.method=="POST":
    #     user_id=request.form.get("user_id")
    #     password=request.form.get("password")
    #     with app.app_context():
    #         new_user=User(user_id=user_id,password=password)
    #         db.session.add(new_user)
    #         db.session.commit()
    #     return redirect(url_for("login"))
    # if request.method=="POST":
    # user_id=request.form.get("user_id")
    # password=request.form.get("password")
    # tmp=User.query.filter(user_id)
    # if tmp is None:
    #     with app.app_context():
    #         new_user=User(user_id=user_id,password=password)
    #         db.session.add(new_user)
    #         db.session.commit()
    #     return redirect(url_for("login"))
    # else:
        
    # if User.query.filter(user_id):



    # new_user=User(user_id=user_id,password=password)



    # with app.app_context():
    #     db.session.add(new_user)
    #     db.session.commit()
    # return render_template("signup.html")



    
    # # return redirect(url_for("signup"))






@app.route("/logout")
def logout():
    with app.app_context():
        db.session.remove()
    return redirect(url_for("login"))

@app.route("/")
def index():
    todo_list=Todo.query.all()
    # print(todo_list[0].id)
    # for i in todo_list:
    #     print(i.title)
    return render_template("index.html",todo_list=todo_list)


@app.route('/add',methods=["POST"])
def add():
    title=request.form.get("title")
    description=request.form.get("description")
    new_todo=Todo(title=title,description=description,completed=False)
    with app.app_context():
        db.session.add(new_todo)
        db.session.commit()

    return redirect(url_for("index"))


@app.route('/update/<id_todo>')
def update(id_todo):
    print(id_todo)
    todo=db.session.query(Todo).filter_by(id=id_todo).first()
    todo.completed=not todo.completed
    print(todo.completed)
    # with app.app_context():
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/delete/<id_todo>')
def delete(id_todo):
    print(id_todo)
    todo=db.session.query(Todo).filter_by(id=id_todo).first()
    todo.completed=not todo.completed
    # with app.app_context():

    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))



    # title=request.form.get("title")
    # new_todo=Todo(title=title,description="random...",completed=False)
    # with app.app_context():
    #     db.session.add(new_todo)
    #     db.session.commit()

    # return redirect(url_for("index"))



    # description=request.form.get("")

# @app.route("/add",methods=["GET","POST"])
# def add():
#     if request.method=="POST":
#         title=request.form["title"]
#         description=request.form["description"]
#         completed=request.form["completed"]
#         todo=Todo(title=title,description=description,completed=completed)
#         db.session.add(todo)
#         db.session.commit()
#         return redirect("/")
#     return render_template("add.html")
# @app.route("/delete/<id>")
# def delete(id):
#     todo=Todo.query.filter_by(id=id).first()
#     db.session.delete(todo)
#     db.session.commit()
#     return redirect("/")
# @app.route("/edit/<id>",methods=["GET","POST"])
# def edit(id):
#     if request.method=="POST":
#         title=request.form["title"]
#         description=request.form["description"]
#         completed=request.form["completed"]
#         todo=Todo.query.filter_by(id=id).first()
#         todo.title=title
#         todo.description=description
#         todo.completed=completed
#         db.session.commit()
#         return redirect("/")
#     todo=Todo.query.filter_by(id=id).first()
#     return render_template("edit.html",todo=todo)
# @app.route("/complete/<id>")
# def complete(id):
#     todo=Todo.query.filter_by(id=id).first()
#     todo.completed=True
#     db.session.commit()
#     return redirect("/")
# @app.route("/uncomplete/<id>")
# def uncomplete(id):
#     todo=Todo.query.filter_by(id=id).first()
#     todo.completed=False
#     db.session.commit()
#     return redirect("/")
# @app.route("/completed")
# def completed():
#     todos=Todo.query.filter_by(completed=True).all()
#     return render_template("completed.html",todos=todos)
# @app.route("/uncompleted")
# def uncompleted():
#     todos=Todo.query.filter_by(completed=False).all()
#     return render_template("uncompleted.html",todos=todos)
        
        
            
    




# @app.route("/")

# def index():
#     return render_template("index.html")





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    # db.create_all()
        # new_todo=Todo(title="New work",description="random......",completed=False)
        # new_user=User(password="lokesh")
        # db.session.add(new_todo)
        # db.session.add(new_user)
        # db.session.commit()


        app.run(debug=True,use_reloader=True)






