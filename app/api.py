from flask import jsonify, request
from app import app
from bson import ObjectId
from datetime import datetime

@app.route('/items', methods=['GET'])
def get_items():
    collection = app.db["items"]
    items = list(collection.find({}, {"_id": 0}))
    return jsonify(items)

@app.route('/api/users')
def get_users():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))
    skip = (page - 1) * limit
    collection = app.db["users"]
    total = collection.count_documents({})
    total_pages = (total + limit - 1) // limit
    users = list(collection.find({}, {"_id": 0, "name": 1, "email": 1}).skip(skip).limit(limit))
    return jsonify({ "users": users, "totalPages": total_pages, "total": total, "page": page })

@app.route('/api/users/<email>', methods=['GET'])
def get_user_by_mail(email):
    user = app.db["users"].find_one({"email": email}, {"_id": 0, "name": 1, "email": 1})
    if user:
        return jsonify(user)
    return jsonify({"message": "ไม่พบผู้ใช้"}), 404

@app.route('/api/users/<email>', methods=['DELETE'])
def delete_user(email):
    result = app.db["users"].delete_one({"email": email})
    if result.deleted_count == 1:
        return jsonify({"message": "ลบสำเร็จ"}), 200
    else:
        return jsonify({"message": "ไม่พบผู้ใช้"}), 404

@app.route('/api/users/<email>', methods=['PUT'])
def update_user(email):
    data = request.get_json()
    updated = app.db["users"].update_one(
        {"email": email},
        {"$set": {
            "name": data.get("name"),
            "email": data.get("email")
        }}
    )
    if updated.modified_count:
        return jsonify({"message": "อัปเดตเรียบร้อย"}), 200
    else:
        return jsonify({"message": "ไม่พบหรือไม่มีการเปลี่ยนแปลง"}), 404

@app.route('/api/movies/landing', methods=['GET'])
def get_movies_landing():
    collection = app.db["movies"]
    movies = list(collection.find({}, {"_id": 0}).limit(10)) 
    return jsonify(movies)

@app.route('/api/movies/pagination')
def get_movies_paginated():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 14))
    skip = (page - 1) * limit

    total = app.db["movies"].count_documents({})
    total_pages = (total + limit - 1) // limit

    movies = list(app.db["movies"].find({}, {
        "title": 1,
        "poster": 1,
        "imdb": 1
    }).skip(skip).limit(limit))

    for m in movies:
        m["_id"] = str(m["_id"])

    return jsonify({
        "movies": movies,
        "totalPages": total_pages,
        "page": page
    })

@app.route('/api/movies/table')
def get_movies_table():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 5))
    skip = (page - 1) * limit
    total = app.db["movies"].count_documents({})
    total_pages = (total + limit - 1) // limit
    
    movies = list(app.db["movies"].find({}, {
        "_id": 0,
        "title": 1,
        "poster": 1,
        "imdb": 1,
        "year": 1,
        "genres": 1
    }).skip(skip).limit(limit))

    return jsonify({
        "movies": movies,
        "totalPages": total_pages,
        "page": page
    })

@app.route('/api/movies/<title>', methods=['GET'])
def get_movie_by_tilte(title):
    movie = app.db["movies"].find_one({"title": title}, {"_id": 0})
    if movie:
        return jsonify(movie)
    return jsonify({"message": "ไม่พบภาพยนตร์"}), 404

@app.route('/api/movies/<title>', methods=['PUT'])
def update_movie(title):
    data = request.get_json()
    updated = app.db["movies"].update_one(
        {"title": title},
        {"$set": {
            "title": data.get("title"),
            "year": data.get("year"),
            "genres": data.get("genres"),
            "poster": data.get("poster"),
            "imdb.rating": data.get("imdb", {}).get("rating")
        }}
    )
    if updated.modified_count:
        return jsonify({"message": "อัปเดตเรียบร้อย"}), 200
    else:
        return jsonify({"message": "ไม่พบหรือไม่มีการเปลี่ยนแปลง"}), 404

@app.route('/api/movies/<title>', methods=['DELETE'])
def delete_movie(title):
    result = app.db["movies"].delete_one({"title": title})
    if result.deleted_count == 1:
        return jsonify({"message": "ลบหนังเรียบร้อยแล้ว"})
    return jsonify({"message": "ไม่พบหนัง"}), 404

def get_movie_by_id(movie_id):
    try:
        object_id = ObjectId(movie_id)
    except Exception:
        return None

    movie = app.db["movies"].find_one({"_id": object_id})
    return movie

def get_comments_by_movie_id(movie_id):
    try:
        object_id = ObjectId(movie_id)
    except Exception:
        return []
    
    from datetime import datetime

    # เพิ่มในส่วนที่คุณ query comments
    comments = list(app.db["comments"].find({"movie_id": ObjectId(movie_id)}))

    # แปลง datetime ให้อยู่ในรูปแบบที่ Jinja render ได้
    for c in comments:
        if isinstance(c.get("date"), datetime):
            c["formatted_date"] = c["date"].strftime("%d %b %Y, %H:%M")  # เช่น 21 Jan 1975, 00:31

    return comments

@app.route("/api/comments", methods=["POST"])
def add_comment():
    data = request.get_json()
    movie_id = data.get("movie_id")
    name = data.get("name")
    text = data.get("text")

    if not all([movie_id, name, text]):
        return jsonify({"error": "Missing data"}), 400

    app.db["comments"].insert_one({
        "movie_id": ObjectId(movie_id),
        "name": name,
        "text": text,
        "date": datetime.utcnow()
    })

    return jsonify({"message": "Comment added successfully"})
