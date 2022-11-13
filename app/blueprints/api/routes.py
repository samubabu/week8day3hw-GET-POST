from flask import jsonify, request
from . import api
from app.models import Post, User


@api.route('/')
def index():
    return 'Hello this is the API'


@api.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@api.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@api.route('/posts', methods=['POST'])
def create_post():
    # Check to see that the request sent a request body that is JSON
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get the data from the request body
    data = request.json
    # Validate the incoming data
    for field in ['title', 'body', 'user_id']:
        if field not in data:
            # If the field is not in the request body, throw an error saying they are missing a field
            return jsonify({"error": f"'{field}' must be in request body"}), 400

    # pull the fields from the request data
    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')
    # Create a new instance of Post (which auto adds to db)
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201

@api.route('/users/<user_id>')
def get_user(user_id):
    user=User.query.get_or_404(user_id)
    print(user)
    return jsonify(user.to_dict())

#HAVE TO OVERWRITE METHOD AND WILL ONLY TAKE POST REQUEST
@api.route('/users', methods=["POST"])
def create_user():
    print (request)
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    data=request.json
    for field in ['username', 'email', 'password']:
        if field not in data:
            return jsonify({'error': f"'{field}' must be in request body"}), 400
    
    username=data.get('username')
    email=data.get('email')
    password=data.get('password')
    print(username, email, password)
    check_user = User.query.filter( (User.username == username) | (User.email == email) ).first()
    if check_user is not None:
        return jsonify({'error':'User with username and/or email already exist'}), 400
    
    
    new_user = User(username=username, email=email, password=password)  
    return jsonify(new_user.to_dict()), 201