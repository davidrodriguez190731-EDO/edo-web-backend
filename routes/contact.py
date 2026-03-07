from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.contact_message import ContactMessage
from database import db

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/", methods=["POST"])
def send_message():
    data = request.get_json()
    msg = ContactMessage(
        name         = data.get("name", ""),
        company      = data.get("company", ""),
        email        = data.get("email", ""),
        project_type = data.get("projectType", ""),
        message      = data.get("message", ""),
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"message": "Mensaje recibido. Le responderemos pronto."}), 201


@contact_bp.route("/", methods=["GET"])
@jwt_required()
def get_messages():
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return jsonify([m.to_dict() for m in msgs]), 200


@contact_bp.route("/<int:mid>/read", methods=["PUT"])
@jwt_required()
def mark_read(mid):
    msg = ContactMessage.query.get_or_404(mid)
    msg.read = True
    db.session.commit()
    return jsonify(msg.to_dict()), 200
