from flask import Flask, send_from_directory

PORT = 8889
DIRECTORY = "/home/ubuntu/files"

app = Flask(__name__)


@app.route('/<path:filename>')
def serve_file(filename):
    import os

    print(os.getcwd())
    print(filename)
    return send_from_directory('/home/ubuntu/files', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
