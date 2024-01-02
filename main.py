from flask_app import app


DOCKER_PORT = 5000
LOCAL_PORT = 5001


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=DOCKER_PORT)
