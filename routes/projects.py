import os, uuid, base64
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.project import Project
from database import db

projects_bp = Blueprint("projects", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads', 'projects')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_base64_image(b64_string):
    """Guarda imagen base64 en disco y retorna la URL relativa."""
    if b64_string.startswith('data:'):
        header, data = b64_string.split(',', 1)
        ext = header.split('/')[1].split(';')[0]
    else:
        data = b64_string
        ext = 'jpg'
    filename  = f"{uuid.uuid4().hex}.{ext}"
    filepath  = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(data))
    return f"/static/uploads/projects/{filename}"

def process_images(images_list, existing_urls=None):
    """Procesa lista de imágenes: guarda base64, conserva URLs existentes."""
    result = []
    for img in images_list:
        if img.startswith('data:'):
            result.append(save_base64_image(img))
        elif img.startswith('/') or img.startswith('http'):
            result.append(img)  # URL existente, conservar
    return result

@projects_bp.route("/", methods=["GET"])
def get_projects():
    projects = Project.query.filter_by(visible=True).order_by(Project.order).all()
    return jsonify([p.to_dict() for p in projects]), 200

@projects_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_projects():
    projects = Project.query.order_by(Project.order).all()
    return jsonify([p.to_dict() for p in projects]), 200

@projects_bp.route("/", methods=["POST"])
@jwt_required()
def create_project():
    data   = request.get_json()
    imgs   = process_images(data.get("images", []))
    p = Project(
        name        = data.get("name", ""),
        category    = data.get("category", ""),
        status      = data.get("status", "En producción"),
        description = data.get("description", ""),
        highlights  = "|".join(data.get("highlights", [])),
        color       = data.get("color", "#1B4B8A"),
        featured    = data.get("featured", False),
        order       = data.get("order", 99),
        visible     = data.get("visible", True),
        images      = "|".join(imgs),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201

@projects_bp.route("/<int:pid>", methods=["PUT"])
@jwt_required()
def update_project(pid):
    p    = Project.query.get_or_404(pid)
    data = request.get_json()
    imgs = process_images(data.get("images", []))
    p.name        = data.get("name", p.name)
    p.category    = data.get("category", p.category)
    p.status      = data.get("status", p.status)
    p.description = data.get("description", p.description)
    p.highlights  = "|".join(data.get("highlights", p.highlights.split("|") if p.highlights else []))
    p.color       = data.get("color", p.color)
    p.featured    = data.get("featured", p.featured)
    p.order       = data.get("order", p.order)
    p.visible     = data.get("visible", p.visible)
    if imgs:
        p.images  = "|".join(imgs)
    db.session.commit()
    return jsonify(p.to_dict()), 200

@projects_bp.route("/<int:pid>", methods=["DELETE"])
@jwt_required()
def delete_project(pid):
    p = Project.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Eliminado"}), 200
