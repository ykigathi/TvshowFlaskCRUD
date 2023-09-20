from flask_app import app
import flask_app.controllers.users
import flask_app.controllers.tvshows


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)
