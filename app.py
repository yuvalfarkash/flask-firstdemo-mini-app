from flask import Flask

from errors import errors_bp
from routes import tasks_bp

# Main Flask app instance for the todo API.
app = Flask(__name__)

# Register the task routes and shared error handlers.
app.register_blueprint(tasks_bp)
app.register_blueprint(errors_bp)

if __name__ == "__main__":
    app.run(debug=True)