from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.json
    qr_data = data.get('data')
    print(f'Received QR Code Data: {qr_data}')
    # Here you can add logic to update the inventory or database
    return jsonify({'message': 'QR Code data received'})

if __name__ == '__main__':
    app.run(debug=True)
