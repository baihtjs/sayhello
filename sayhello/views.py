from flask import flash, redirect, url_for, render_template

from sayhello.forms import HelloForm
from sayhello.models import Message
from sayhello import db
from sayhello import app


@app.route('/', methods=['GET', 'POST'])
def index():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    form = HelloForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(name=name, body=body)
        db.session.add(message)
        db.session.commit()
        flash('You leave the message success!')
        return redirect(url_for('index'))
    return render_template('index.html', form=form, messages=messages)



