from flask import Flask, request, jsonify, send_file
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

products = {}
next_id = 1

def generate_id():
    global next_id
    current = next_id
    next_id += 1
    return current

def is_valid_product(data, require_all=False):
    if not data:
        return False
    if require_all:
        return 'name' in data and 'description' in data
    return 'name' in data or 'description' in data

@app.route('/products', methods=['GET'])
def list_all_products():
    return jsonify(list(products.values())), 200

@app.route('/product/<int:product_id>', methods=['GET'])
def fetch_product(product_id):
    product = products.get(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({"status": "error", "message": "Товар не найден"}), 404

@app.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    
    if not is_valid_product(data, require_all=True):
        return jsonify({"status": "error", "message": "Необходимы name и description"}), 400
    
    product_id = generate_id()
    new_product = {
        "id": product_id,
        "name": data['name'].strip(),
        "description": data['description'].strip(),
        "icon": None
    }
    products[product_id] = new_product
    
    return jsonify(new_product), 201

@app.route('/product/<int:product_id>', methods=['PUT'])
def modify_product(product_id):
    if product_id not in products:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    
    data = request.get_json()
    
    if not is_valid_product(data):
        return jsonify({"status": "error", "message": "Нет данных для обновления"}), 400
    
    if 'name' in data and data['name']:
        products[product_id]['name'] = data['name'].strip()
    if 'description' in data and data['description']:
        products[product_id]['description'] = data['description'].strip()
    
    return jsonify(products[product_id]), 200

@app.route('/product/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    if product_id not in products:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    
    if products[product_id].get('icon'):
        icon_path = os.path.join(app.config['UPLOAD_FOLDER'], products[product_id]['icon'])
        if os.path.exists(icon_path):
            os.remove(icon_path)
    
    removed = products.pop(product_id)
    return jsonify({
        "status": "success",
        "message": "Товар удален",
        "deleted_item": removed
    }), 200

@app.route('/product/<int:product_id>/image', methods=['POST'])
def upload_image(product_id):
    if product_id not in products:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "Нет файла"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"status": "error", "message": "Пустой файл"}), 400
    
    filename = f"product_{product_id}_{file.filename}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    if products[product_id].get('icon'):
        old_icon = os.path.join(app.config['UPLOAD_FOLDER'], products[product_id]['icon'])
        if os.path.exists(old_icon):
            os.remove(old_icon)
    
    products[product_id]['icon'] = filename
    
    return jsonify({"status": "success", "icon": filename}), 200

@app.route('/product/<int:product_id>/image', methods=['GET'])
def get_image(product_id):
    if product_id not in products:
        return jsonify({"status": "error", "message": "Товар не найден"}), 404
    
    if not products[product_id].get('icon'):
        return jsonify({"status": "error", "message": "Нет иконки"}), 404
    
    icon_path = os.path.join(app.config['UPLOAD_FOLDER'], products[product_id]['icon'])
    return send_file(icon_path)

if __name__ == '__main__':
    app.run(debug=False, port=5000)