from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.blog_post import BlogPost
from database import db

blog_bp = Blueprint("blog", __name__)


@blog_bp.route("/", methods=["GET"])
def get_posts():
    """Público: artículos publicados, más recientes primero."""
    posts = BlogPost.query.filter_by(published=True).order_by(BlogPost.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200


@blog_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200


@blog_bp.route("/<int:pid>", methods=["GET"])
def get_post(pid):
    p = BlogPost.query.get_or_404(pid)
    if not p.published:
        return jsonify({"error": "No encontrado"}), 404
    return jsonify(p.to_dict()), 200


@blog_bp.route("/", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    p = BlogPost(
        title     = data.get("title", ""),
        excerpt   = data.get("excerpt", ""),
        content   = data.get("content", ""),
        category  = data.get("category", "Análisis"),
        read_time = data.get("readTime", "5 min"),
        published = data.get("published", True),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


@blog_bp.route("/<int:pid>", methods=["PUT"])
@jwt_required()
def update_post(pid):
    p = BlogPost.query.get_or_404(pid)
    data = request.get_json()
    p.title     = data.get("title",     p.title)
    p.excerpt   = data.get("excerpt",   p.excerpt)
    p.content   = data.get("content",   p.content)
    p.category  = data.get("category",  p.category)
    p.read_time = data.get("readTime",  p.read_time)
    p.published = data.get("published", p.published)
    db.session.commit()
    return jsonify(p.to_dict()), 200


@blog_bp.route("/<int:pid>", methods=["DELETE"])
@jwt_required()
def delete_post(pid):
    p = BlogPost.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Eliminado"}), 200
