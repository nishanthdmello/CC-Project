from flask import Flask, request
from etcd import Client, EtcdKeyNotFound

# Initialize Flask application
app = Flask(__name__)

# Initialize etcd client
client = Client(host='localhost', port=5007)

# Controller for setting a key-value pair in etcd
@app.route('/set', methods=['POST'])
def set_key():
    key = request.json.get('key')
    value = request.json.get('value')
    if not key or not value:
        return "Key and value must be provided in JSON format.", 400

    try:
        client.write(key, value)
        return f"Successfully set {key} to {value}"
    except Exception as e:
        return f"Error setting {key}: {str(e)}", 500

# Controller for getting the value of a key from etcd
@app.route('/get', methods=['GET'])
def get_key():
    key = request.args.get('key')
    if not key:
        return "Key must be provided as a query parameter.", 400

    try:
        response = client.read(key)
        return response.value
    except EtcdKeyNotFound:
        return f"Key {key} not found in etcd", 404
    except Exception as e:
        return f"Error getting value for {key}: {str(e)}", 500


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
