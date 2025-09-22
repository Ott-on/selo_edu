from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == 'mauro@gmail.com' and password == '123':
            session['email'] = email
            session['token'] = '123'
            return redirect(url_for('user.home'))
        else:
            return "Credencias inválidas!", 401
    
    return render_template('auth/login.html')




