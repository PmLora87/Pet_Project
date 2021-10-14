from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.pet import Pet
from flask_app.models.user import User
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/new/pet')
def new_pet():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('add_pet.html',user=User.get_by_id(data))


@app.route('/create/pet',methods=['POST'])
def create_pet():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pet.validate_pet(request.form):
        return redirect('/new/pet')

    image = None
    if "image" in request.files and request.files["image"]:
        if not allowed_file(request.files['image']):
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            redirect('/create/pet')
        f = request.files['image']
        f.seek(0)
        f.save(os.path.join("flask_app/static/images/", f.filename))
        image = os.path.join("static/images/", f.filename)
        
    data = {
        "pet_type": request.form["pet_type"],
        "name": request.form["name"],
        "breed": request.form["breed"],
        "age": int(request.form["age"]),
        "diet": request.form["diet"],
        "date_made": request.form["date_made"],
        'conditions': request.form['conditions'],
        'vaccinations': ', '.join(request.form.getlist('vaccinations')),
        "user_id": session["user_id"],
        "image": image
    }
    Pet.save(data)
    return redirect('/dashboard')

@app.route('/edit/pet/<int:id>')
def edit_pet(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_pet.html",edit=Pet.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/pet',methods=['POST'])
def update_Pet():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Pet.validate_pet(request.form):
        return redirect('/edit/pet/<int:id>')

    # Instantiate image to none
    image = None
    # Chceck if image passed from html form
    if "image" in request.files and request.files["image"]:
        # Check file type
        if not allowed_file(request.files['image']):
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            redirect('/update/pet')
        # Get File called Image from HTML
        f = request.files['image']
        # Set Buffer to begining of Image
        f.seek(0)
        # Set Path to Save Image
        # os path gets parent directory and adds path to join ... parent = '/' and joined = 'flask_app/static/images/ => returns parent+join => '/flask_app/static/images/'
        f.save(os.path.join("flask_app/static/images/", secure_filename(f.filename)))
        # Get Path of Image to save to DB
        image = os.path.join("static/images/", secure_filename(f.filename))

    data = {
        "pet_type": request.form["pet_type"],
        "name": request.form["name"],
        "breed": request.form["breed"],
        "age": int(request.form["age"]),
        "diet": request.form["diet"],
        'conditions': request.form['conditions'],
        'vaccinations': ', '.join(request.form.getlist('vaccinations')), # request.form.getlist('vaccinations') returns list ... use join to make it string
        "date_made": request.form["date_made"],
        "id": request.form['id'],
        "image": image
    }

    Pet.update(data)
    return redirect('/dashboard')


@app.route('/destroy/pet/<int:id>')
def destroy_pet(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Pet.destroy(data)
    return redirect('/dashboard')