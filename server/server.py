from flask import Flask, request, jsonify
from etcd import Client, EtcdKeyNotFound


app = Flask(__name__)


client = Client(host='localhost', port=5007)


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
        return f"Error settin  {key}: {str(e)}", 500


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

@app.route('/getall', methods=['GET'])
def get_all_keys():
    try:
        response = client.read('/', recursive=True)
        key_values = {node.key: node.value for node in response.leaves}
        return jsonify(key_values)
    except Exception as e:
        return f"Error getting all key-value pairs: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
