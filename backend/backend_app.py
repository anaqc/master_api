from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
    {"id": 3, "title": "Third post", "content": "This is the third post."},
    {"id": 4, "title": "Fourth post", "content": "This is the fourth post."},
    {"id": 5, "title": "Fifth post", "content": "This is the fifth post."},
    {"id": 6, "title": "Sixth post", "content": "This is the sixth post."},
    {"id": 7, "title": "Seventh post", "content": "This is the seventh post."},
    {"id": 8, "title": "Eighth post", "content": "This is the eighth post."},
    {"id": 9, "title": "Ninth post", "content": "This is the ninth post."},
    {"id": 10, "title": "Tenth post", "content": "This is the tenth post."},
    {"id": 11, "title": "Eleventh post", "content": "This is the eleventh post."},
    {"id": 12, "title": "Twelfth post", "content": "This is the twelfth post."},
    {"id": 13, "title": "Thirteenth post", "content": "This is the thirteenth post."},
    {"id": 14, "title": "Fourteenth post", "content": "This is the fourteenth post."},
    {"id": 15, "title": "Fifteenth post", "content": "This is the fifteenth post."},
    {"id": 16, "title": "Sixteenth post", "content": "This is the sixteenth post."},
    {"id": 17, "title": "Seventeenth post", "content": "This is the seventeenth post."},
    {"id": 18, "title": "Eighteenth post", "content": "This is the eighteenth post."},
    {"id": 19, "title": "Nineteenth post", "content": "This is the nineteenth post."},
    {"id": 20, "title": "Twentieth post", "content": "This is the twentieth post."}
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    This function shows the posts list and sorted it
    if a user get query parameters
    """
    # Get query parameters
    sort = request.args.get("sort", "").lower()
    direction = request.args.get("direction", "").lower()
    sort_values = ["title", "content"]
    direction_values = ["asc", "desc"]
    page = request.args.get("page")
    limit = request.args.get("limit")
    if not sort and not direction and not page and not limit:
        return jsonify(POSTS)
    elif sort in sort_values and direction in direction_values:
        direction = direction != "asc"
        sorted_posts = sorted(POSTS, key=lambda post:post[sort].lower(), reverse=direction)
        return jsonify(sorted_posts)
    elif page and limit:
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 10))
        except ValueError:
            return jsonify({
                "error": "Invalid page or limit parameter"
            }), 400
        if page < 1 or limit < 1:
            return jsonify({"error": "Page and limit must be greater than 0"}), 400

        start_index = (page - 1) * limit
        end_index = start_index + limit

        paginated_posts = POSTS[start_index:end_index]

        return jsonify(paginated_posts)
    else:
        return jsonify({
            "error": "Bad Request",
            "status": 400
        }), 400


@app.route('/api/posts', methods=['POST'])
def add_post():
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
        "title": data.get("title"),
        "content": data.get("content")
    }
    POSTS.append(new_post)
    return jsonify({"message" : "Post created successfully"}), 201


def find_post_by_id(post_id):
    """ Find the post with the id `post_id`.
      If there is no post with this id, return None. """
    # validate post_id
    if not 0 < post_id <= len(POSTS):
        return None
    for post in POSTS:
        if post["id"] == post_id:
            return post
    return None


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """
    Delete a blog post by its ID and return the deleted
    post data  message.
    """
    # Find the post with the given ID
    post = find_post_by_id(id)
    index = 0
    # If the post wasn't found, return a 404 error
    if post is None:
        return jsonify({
            "error": "Post not found",
            "status": 404
        }), 404
    # Remove the post from the list
    for i, post in enumerate(POSTS):
        if post["id"] == id:
            index = i
    POSTS.pop(index)
    # Return the deleted post id
    return jsonify({"message": f"Post with id {id} has been deleted successfully."})


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
    """
    Update a blog post by its ID and return JSON response.
    Returns the updated post data or error message.
    """
    # Find the post with the given ID
    post = find_post_by_id(id)

    # If the post wasn't found, return a 404 error
    if post is None:
        return jsonify({
            "error" : "Post not found",
            "status" : 404
        }), 404
    # Update the post with the new data
    new_post = request.get_json()
    post.update({
        "id" : id,
        "title" : new_post.get("title", post.get("title")),
        "content" : new_post.get("content", post.get("content"))
    })
    # Return the updated post
    return jsonify({"message" : f"Post {id} updated successfully"})


@app.route("/api/posts/search", methods=["GET"])
def search():
    # Get query parameters
    title = request.args.get("title", "").lower()
    content = request.args.get("content", "").lower()
    searched_post = []
    if title is not "" and content is not "":
        for post in POSTS:
            if  title in post.get("title").lower() or content in post.get("content").lower():
                searched_post.append(post)
    elif title is not "":
        for post in POSTS:
            if  title in post.get("title").lower():
                searched_post.append(post)
    elif content is not "":
        for post in POSTS:
            if  content in post.get("content").lower():
                searched_post.append(post)
    return jsonify(searched_post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
