from pyexpat.errors import messages

from flask import Flask, jsonify, url_for, redirect, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add():
    """
     This function handles the addition of a new Post
    """
    data = request.get_json()
    #validate required fields
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error" : "Invalid request, missing fields"})
    # Generate a new ID for new_post
    new_id = max(post['id'] for post in POSTS) + 1
    new_post = {
        "id": new_id,
        "title": data["title"],
        "content": data["content"]
    }
    POSTS.append(new_post)
    return jsonify({"message" : "Post created successfully"}), 201


def find_post_by_id(post_id):
    """ Find the book with the id `book_id`.
      If there is no book with this id, return None. """
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    # Find the book with the given ID
    post = find_post_by_id(id)
    index = 0
    # If the book wasn't found, return a 404 error
    if post is None:
        return '', 404

    # Remove the book from the list
    for i, post in enumerate(POSTS):
        if post["id"] == id:
            index = i
    POSTS.pop(index)
    # Return the deleted book
    return jsonify(post)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
