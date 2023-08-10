from flask import Flask, send_from_directory

PORT = 81
DIRECTORY = "/root/files"

app = Flask(__name__)


@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('/root/files', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
