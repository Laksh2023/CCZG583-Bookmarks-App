from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Configure PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bookmark_user:password@postgres-service/bookmark_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Bookmark Model
class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, nullable=False)

# Routes for API

@app.route('/bookmarks', methods=['POST'])
def create_bookmark():
    data = request.get_json()
    new_bookmark = Bookmark(
        title=data['title'],
        url=data['url'],
        description=data.get('description', ""),
        user_id=data['user_id']
    )
    db.session.add(new_bookmark)
    db.session.commit()
    return jsonify({"message": "Bookmark created successfully"}), 201

@app.route('/bookmarks/<int:id>', methods=['GET'])
def get_bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    return jsonify({
        "id": bookmark.id,
        "title": bookmark.title,
        "url": bookmark.url,
        "description": bookmark.description,
        "user_id": bookmark.user_id
    }), 200

@app.route('/bookmarks/<int:id>', methods=['DELETE'])
def delete_bookmark(id):
    bookmark = Bookmark.query.get_or_404(id)
    db.session.delete(bookmark)
    db.session.commit()
    return jsonify({"message": "Bookmark deleted successfully"}), 200

# New route to get all bookmarks by user_id
@app.route('/bookmarks/user/<int:user_id>', methods=['GET'])
def get_bookmarks_by_user(user_id):
    # Query all bookmarks for the given user_id
    bookmarks = Bookmark.query.filter_by(user_id=user_id).all()

    # Serialize results into JSON format
    result = [
        {
            'id': b.id,
            'title': b.title,
            'url': b.url,
            'description': b.description,
            'user_id': b.user_id
        } for b in bookmarks
    ]

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

