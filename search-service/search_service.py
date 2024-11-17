from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://bookmark_user:password@postgres-service/bookmark_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Bookmark model (same as in Bookmark service)
class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    user_id = db.Column(db.Integer, nullable=False)

# Search API route
@app.route('/search', methods=['GET'])
def search_bookmarks():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    # Perform search on title and URL fields
    results = Bookmark.query.filter(
        (Bookmark.title.ilike(f'%{query}%')) | (Bookmark.url.ilike(f'%{query}%'))
    ).all()

    # Serialize results into JSON format
    bookmarks = [{'id': b.id, 'title': b.title, 'url': b.url, 'description': b.description, 'user_id': b.user_id} for b in results]

    return jsonify(bookmarks), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

