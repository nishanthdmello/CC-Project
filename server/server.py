from flask import Flask, request, jsonify
import etcd3

app = Flask(__name__)
etcd = etcd3.client(port=2379)

# PUT operation
@app.route('/put', methods=['POST'])
def put():
    data = request.get_json()
    key = data['key']
    value = data['value']
    etcd.put(key, value)
    return jsonify({'message': 'Key {} set to {}'.format(key, value)}), 200

# GET operation
@app.route('/get', methods=['GET'])
def get():
    key = request.args.get('key')
    if key is None:
        return jsonify({'error': 'Key parameter is required'}), 400

    try:
        value_bytes = etcd.get(key)
        print(value_bytes)
        if value_bytes:
            value_string = value_bytes[0].decode('utf-8')
            return jsonify({'value': value_string}), 200
        else:
            return jsonify({'message': 'Key not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET all keys
@app.route('/getall', methods=['GET'])
def get_all_keys():
    try:
        value_list=[]
        for key, value in etcd.get_all():
            decoded_value=key.decode('utf-8')
            decoded_key=value.key.decode('utf-8')
            value_list.append((decoded_key, decoded_value))
        print(value_list)
        return jsonify({"key-value-pairs":value_list}), 200
    except Exception as e:
        return f"Error getting all key-value pairs: {str(e)}", 500

# DELETE  Operation 
@app.route('/delete',methods=['DELETE'])
def delete_key():
        key=request.args.get('key')
        if key is None:
            return jsonify({'error': 'Key parameter is required'}), 400
        try:
            val=etcd.delete(key,prev_kv=True,return_response=False)
            return f"  deleted succesfully",200
        except Exception as e:
            return f"Error deleting the key-value pairs: {str(e)}", 500
        

if __name__ == '__main__':
    app.run(debug=True)
