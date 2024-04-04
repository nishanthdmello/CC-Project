from flask import Flask, request, jsonify
import etcd3,requests
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


etcd = etcd3.client(port=2379)

# PUT operation
@app.route('/put', methods=['POST'])
def put():
    data = request.get_json()
    key = data['key']
    value = data['value']
    keypresent=False
    response= requests.get('http://127.0.0.1:5000/getall')
    list_=response.json()
    print(list_)
    for i in list_:
        if i['key']==key:
            keypresent=True
            break
    if keypresent:
        return f"error : key is already present ", 403
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
        # print(value_bytes)
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
            value_list.append({"key":decoded_key, "value": decoded_value})
        # print(value_list)
        return jsonify(value_list), 200
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
            if(val):
                return f"  deleted succesfully",200
            else:
                return f" error deleting key : key not found",404
        except Exception as e:
            return f"Error deleting the key-value pairs: {str(e)}", 500
  
@app.route('/update', methods=['PUT'])
def update():
        data = request.get_json()
        key = data.get('key') 
        value = data.get('value') 

        if not key or not value:
            return jsonify({'error': 'Both key and value are required'}), 400

        try:
            # Check if the key exists before attempting an update
            etcd.get(key) 

            etcd.put(key, value)
            return jsonify({'message': 'Key {} updated to {}'.format(key, value)}), 200
        except etcd3.exceptions.KeyNotFoundError:
            return jsonify({'error': 'Key not found'}), 404
        
        except Exception as e:  
            return jsonify({'error': f'An unexpected error occurred {str(e)}'}), 500  

if __name__ == '__main__':
    app.run(debug=True)