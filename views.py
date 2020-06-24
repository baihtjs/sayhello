from flask import flash, redirect, url_for, render_template

from forms import HelloForm
from models import Message
from sayhello import db
from sayhello import app


@app.route('/', methods=['GET', 'POST'])
def index():
    messages = Message.query.all()
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.name.data
        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash('You leave the message success!')
        return redirect(url_for('index'))
    return render_template('index.html',form=form,messages=messages)


