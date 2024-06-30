from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test')
def test():
    return jsonify(message="Test route is working")

@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    """Return data about all cupcakes."""
    cupcakes = Cupcake.query.all()
    cupcakes_data = [{"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image} for cupcake in cupcakes]
    return jsonify(cupcakes=cupcakes_data)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    """Return data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake_data = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
    return jsonify(cupcake=cupcake_data)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake and return its data."""
    data = request.json

    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data.get('image', 'https://tinyurl.com/demo-cupcake')
    )

    db.session.add(new_cupcake)
    db.session.commit()

    cupcake_data = {
        "id": new_cupcake.id,
        "flavor": new_cupcake.flavor,
        "size": new_cupcake.size,
        "rating": new_cupcake.rating,
        "image": new_cupcake.image
    }
    return jsonify(cupcake=cupcake_data), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update a cupcake and respond with the updated data."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    cupcake_data = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
    return jsonify(cupcake=cupcake_data)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake and respond with a message."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

if __name__ == '__main__':
    app.run(host='10.0.4.23', port=5000, debug=True)
