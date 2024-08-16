from flask import Flask, request
from scraper import get_package

app = Flask(__name__)

@app.route('/')
def test():
    return "HELLO USER !!"

@app.route('/package', methods=['POST'])
def fetch_package_details():
    data = request.get_json()
    url = data['url']
    try:
        package = get_package(url)
        return package
    except Exception as e:
        return "URL NOT FOUND"

if __name__ == '__main__':
    app.run(debug=True)