from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.forms import SignUpForm, LogInForm, PostForm
from app.models import User, Post

# Create routes for our app
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('index.html', posts=posts)



@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Hooray our form submitted!')
        # Get data from form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        # Check to see if we have a user with username and/or password:
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).first()
        if check_user is not None:
            flash('User with username and/or email already exists', 'danger')
            return redirect(url_for('signup'))
        # Add a new user to the database
        new_user = User(email=email, username=username, password=password)
        # Flash a success message
        flash(f"{new_user} has successfully signed up!", "success")
        # Redirect back to home
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        # Get the form data
        username = form.username.data
        password = form.password.data
        # Check to see if there is a user with that username and password
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            # log the user in
            login_user(user)
            flash(f"{user} is now logged in.", 'primary')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username and/or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        # Get the data from the form
        title = form.title.data
        body = form.body.data
        # Create a new instance of Post with the info from the form
        new_post = Post(title=title, body=body, user_id=current_user.id)
        # flash a message of success
        flash(f"{new_post.title} has been created.", "success")
        # Redirect back to the home page
        return redirect(url_for('index'))

    return render_template('create.html', form=form)

@app.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    return render_template('post.html', post=post)

@app.route('/posts/<post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    if post.author != current_user:
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('index'))
    form = PostForm()
    if form.validate_on_submit():
        # Get the form data
        new_title = form.title.data
        new_body = form.body.data
        # update the post
        post.update(title=new_title, body=new_body)
        flash(f"{post.title} has been updated", "success")
        return redirect(url_for('get_post', post_id=post.id))
    return render_template('edit_post.html', post=post, form=form)

@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"Post with id #{post_id} does not exist", "warning")
        return redirect(url_for('index'))
    if post.author != current_user:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('index'))
    post.delete()
    flash(f"{post.title} has been deleted", 'info')
    return redirect(url_for('index'))
