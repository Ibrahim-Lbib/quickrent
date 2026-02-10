# homepage, landing pages
from flask import Blueprint, app, render_template

@app.route('/')
def home():
    return render_template('home.html')