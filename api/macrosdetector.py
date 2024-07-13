from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Dummy analysis result
    analysis_result = "This is a dummy analysis of the uploaded macro file."
    return jsonify({'analysis': analysis_result})

if __name__ == '__main__':
    app.run(debug=True)
