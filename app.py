from flask import Flask

from errors import errors_bp
from routes import tasks_bp


app = Flask(__name__)


app.register_blueprint(tasks_bp)
app.register_blueprint(errors_bp)

if __name__ == "__main__":
    app.run(debug=True)