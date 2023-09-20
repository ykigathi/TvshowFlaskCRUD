from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.tvshow import Tvshow


@app.route('/tvshows/<int:id>')
def show_tvshow(id):
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    data = {
        'id': id,
    }
    user_id = {
        'id' : session['user_id']
    }
    return render_template('view_tvshow.html', tvshow=Tvshow.get_one(data), user=User.get_one(user_id))


#GET route to show add-tvshow page
@app.route("/addtvshow")
def add_tvshow():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    return render_template('add_tvshow.html')


#POST : route to create tvshow
@app.post('/create-tvshow')
def create_tvshow():
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    
    data = {
        'user_id' : session['user_id'],
        'title' : request.form['title'],
        'network' : request.form['network'],
        'description' : request.form['description'],
        'release_date' : request.form['release_date'],
    }

    if (Tvshow.validate_tvshow(data)):
        Tvshow.insert(request.form)
    else :  
        flash('All fields are required.')
        return redirect('/addtvshow')

    return redirect('/dashboard')



        
#GET :edit page
@app.route('/tvshows/<int:id>/edit')
def edit_tvshow(id):
    data = {
        'id': id,
    }
    tvshow = Tvshow.get_one(data)
    if 'user_id' not in session:
        flash('You must be logged in to view this page.')
        return redirect('/')
    if tvshow.user_id != session['user_id']:
        flash('You did not create this tvshow to be able to udpate it.')
        return redirect('/dashboard')
    return render_template('edit_tvshow.html', tvshow=tvshow)


@app.post('/tvshows/update/<int:id>')
def update_tvshow_in_db(id):
    data = {
        "id" : id,
        'user_id' : session['user_id'],
        'title' : request.form['title'],
        'network' : request.form['network'],
        'description' : request.form['description'],
        'release_date' : request.form['release_date']
    }

    if (Tvshow.validate_tvshow(data)):
        Tvshow.update(data)

    return redirect('/dashboard')



#Delete tvshow
@app.route('/tvshows/<int:id>/delete')
def delete_tvshow(id):
    data = {
        "id": id,
    }
    Tvshow.delete(data)
    return redirect('/dashboard')

