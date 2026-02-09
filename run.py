from flask import Flask, render_template, request, redirect, url_for
import os

def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
        

    @app.route('/')
    def home():
        return render_template('home.html')
    return app  

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)