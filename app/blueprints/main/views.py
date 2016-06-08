from flask import render_template, redirect, url_for
from flask_login import login_required
from . import main
from .forms import ExampleForm
from app.models import db, Example


@main.route('/', methods=['GET'])
def index():
    return render_template('main/index.html')


@login_required
@main.route('/add', methods=['GET', 'POST'])
def add():
    form = ExampleForm()
    if form.validate_on_submit():
        example = Example(
            text = form.text.data
        )
        db.session.add(example)
        db.session.commit()
        return redirect(url_for('main.browse'))
    return render_template('main/add.html', form=form)


@main.route('/view', methods=['GET'])
def browse():
    examples = Example.query.all()
    return render_template('main/browse.html', examples=examples)


@main.route('/get/<int:id>', methods=['GET'])
def get(id):
    example = Example.query.get_or_404(id)
    return render_template('main/get.html', example=example)
