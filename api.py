from flask import Flask, jsonify, request
app = Flask(__name__)

# In-memory mock data for testing 
orders = {
    "OY123": {"order_id": "OY123", "item": "Laptop", "status": "Shipped"},
    "OY124": {"order_id": "OY124", "item": "Phone", "status": "Processing"}
         }


# Endpoint for getting order details
@app.route('/order/<order_id>', methods=['GET'])
def get_order_details(order_id):
    order = orders.get(order_id)
    if order:
        return jsonify({"status": "success", "data": order}), 200
    else:
        return jsonify({"status": "error", "message": "Order not found"}), 404


# Endpoint for getting order details
@app.route('/order/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    if order_id in orders:
        orders[order_id]["status"] = "Canceled"
        return jsonify({"status": "success", "message": f"Order {order_id} has been canceled"}), 200
    else:
        return jsonify({"status": "error", "message": "Order not found"}), 404


if __name__ == "__main__":
    app.run(port=3001)

