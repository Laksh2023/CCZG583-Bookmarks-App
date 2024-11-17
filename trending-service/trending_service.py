from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

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

# API route to get trending bookmarks
@app.route('/trending', methods=['GET'])
def get_trending_bookmarks():
    # Query to get the most frequently saved bookmarks (group by URL)
    trending_bookmarks = (
        db.session.query(Bookmark.url, func.count(Bookmark.id).label('count'))
        .group_by(Bookmark.url)
        .order_by(func.count(Bookmark.id).desc())  # Order by frequency of saves
        .limit(3)  # Limit to top 3 trending bookmarks
        .all()
    )

    # Serialize results into JSON format
    results = [{'url': b[0], 'count': b[1]} for b in trending_bookmarks]

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
