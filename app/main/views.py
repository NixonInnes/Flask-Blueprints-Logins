from flask import render_template, redirect, url_for
from app.main import main

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('main/index.html')