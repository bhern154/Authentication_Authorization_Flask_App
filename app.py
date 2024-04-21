from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "jAjF22SW98fdDH203"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # encript the password
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        
        #redirect to form if registration info is invalid
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        
        # store the user in a session
        session['username'] = new_user.username

        flash('Welcome! Successfully Created Your Account!', "success")

        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/secret')
def secret(): 
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/')

    return render_template('secret.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # get encripted password
        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')

@app.route('/users/<username>')
def show_user(username):
   
    # make sure user is logged in 
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    
    # make sure user logged in matches username
    elif username != session["username"]:
        flash("You are not authorized to view this page!", "danger")
        return redirect('/')

    user_info = User.query.filter_by(username=username).first_or_404()
    feedbacks = Feedback.query.filter_by(username=username).all()

    return render_template('user.html', user_info=user_info, feedbacks=feedbacks)
    
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):

    # make sure user is logged in 
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    
    # make sure user logged in matches username
    elif username != session["username"]:
        flash("You don't have permission to do that!", "danger")
        return redirect('/')
    
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()

    session.pop('username')
    flash('User deleted successfully!', 'info')
    return redirect('/')
   
@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """GET and POST routes to render and post a form for adding a new pet."""

    form = FeedbackForm()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data

        new_feedback  = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()

        # flash a success message for creating a pet
        flash("New feedback added!", 'info')
        
        return redirect(f"/users/{username}")

    else:

        # if the form was not validated / properly filled out, rerender the form.
        return render_template("feedback.html", form=form)
    
@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def update_feedback(id):

    feedback = Feedback.query.filter_by(id=id).first_or_404()
    username = feedback.username
    form = FeedbackForm()
    
    # make sure user logged in matches username
    if username != session["username"]:
        flash("You don't have permission to do that!", "danger")
        return redirect('/')
    
    if form.validate_on_submit():

        # collect deited information from the EditPetForm
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        # flash a success message for editing a pet
        flash('Feedback updated successfully!', 'success')
        return redirect(f'/users/{username}')

    else:

        # pre fill out the form with the pet's information to make editing easier
        form.title.default = feedback.title
        form.content.default = feedback.content
        form.process()
        
        # if the form was not validated / properly filled out, rerender the form.
        return render_template("update_feedback.html", form=form, feedback=feedback)


@app.route('/feedback/<int:id>/delete', methods=["POST"])
def delete_feedback(id):

    feedback = Feedback.query.filter_by(id=id).first_or_404()
    username = feedback.username
    
    # make sure user logged in matches username
    if username != session["username"]:
        flash("You don't have permission to do that!", "danger")
        return redirect('/')
    
    db.session.delete(feedback)
    db.session.commit()

    flash('Feedback deleted successfully!', 'success')
    return redirect(f'/users/{username}')
