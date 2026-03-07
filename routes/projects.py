from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.project import Project
from database import db

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/", methods=["GET"])
def get_projects():
    """Público: devuelve proyectos visibles ordenados."""
    projects = Project.query.filter_by(visible=True).order_by(Project.order).all()
    return jsonify([p.to_dict() for p in projects]), 200


@projects_bp.route("/all", methods=["GET"])
@jwt_required()
def get_all_projects():
    """Admin: devuelve todos los proyectos."""
    projects = Project.query.order_by(Project.order).all()
    return jsonify([p.to_dict() for p in projects]), 200


@projects_bp.route("/", methods=["POST"])
@jwt_required()
def create_project():
    data = request.get_json()
    p = Project(
        name        = data.get("name", ""),
        category    = data.get("category", ""),
        stack       = ",".join(data.get("stack", [])),
        status      = data.get("status", "En producción"),
        description = data.get("description", ""),
        highlights  = "|".join(data.get("highlights", [])),
        color       = data.get("color", "#1B4B8A"),
        featured    = data.get("featured", False),
        order       = data.get("order", 99),
        visible     = data.get("visible", True),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


@projects_bp.route("/<int:pid>", methods=["PUT"])
@jwt_required()
def update_project(pid):
    p = Project.query.get_or_404(pid)
    data = request.get_json()
    p.name        = data.get("name", p.name)
    p.category    = data.get("category", p.category)
    p.stack       = ",".join(data.get("stack", p.stack.split(",") if p.stack else []))
    p.status      = data.get("status", p.status)
    p.description = data.get("description", p.description)
    p.highlights  = "|".join(data.get("highlights", p.highlights.split("|") if p.highlights else []))
    p.color       = data.get("color", p.color)
    p.featured    = data.get("featured", p.featured)
    p.order       = data.get("order", p.order)
    p.visible     = data.get("visible", p.visible)
    db.session.commit()
    return jsonify(p.to_dict()), 200


@projects_bp.route("/<int:pid>", methods=["DELETE"])
@jwt_required()
def delete_project(pid):
    p = Project.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Eliminado"}), 200
