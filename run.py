from flask import Flask, render_template, request, redirect, url_for
def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('home.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)