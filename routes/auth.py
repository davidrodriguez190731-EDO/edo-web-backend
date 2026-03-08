from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from models.admin_user import AdminUser
from database import db

auth_bp = Blueprint("auth", __name__)

# ── Login ──────────────────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    data     = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    user = AdminUser.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Credenciales incorrectas"}), 401
    if not user.is_active:
        return jsonify({"error": "Usuario desactivado"}), 403
    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token, "user": user.to_dict()}), 200

# ── Me ─────────────────────────────────────────────────────────
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = AdminUser.query.get(get_jwt_identity())
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.to_dict()), 200

# ── Cambiar contraseña propia ──────────────────────────────────
@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    user = AdminUser.query.get(get_jwt_identity())
    data = request.get_json()
    if not check_password_hash(user.password_hash, data.get("currentPassword", "")):
        return jsonify({"error": "Contraseña actual incorrecta"}), 400
    if len(data.get("newPassword", "")) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
    user.password_hash = generate_password_hash(data["newPassword"])
    db.session.commit()
    return jsonify({"message": "Contraseña actualizada"}), 200

# ── Listar usuarios ────────────────────────────────────────────
@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    users = AdminUser.query.order_by(AdminUser.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users]), 200

# ── Crear usuario ──────────────────────────────────────────────
@auth_bp.route("/users", methods=["POST"])
@jwt_required()
def create_user():
    data = request.get_json()
    username  = data.get("username", "").strip()
    password  = data.get("password", "")
    email     = data.get("email", "").strip()
    full_name = data.get("full_name", "").strip()

    if not username or not password:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400
    if len(password) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
    if AdminUser.query.filter_by(username=username).first():
        return jsonify({"error": "El nombre de usuario ya existe"}), 400
    if email and AdminUser.query.filter_by(email=email).first():
        return jsonify({"error": "El email ya está registrado"}), 400

    user = AdminUser(
        username=username,
        email=email or None,
        full_name=full_name or None,
        password_hash=generate_password_hash(password),
        is_active=True
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# ── Editar usuario ─────────────────────────────────────────────
@auth_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    user = AdminUser.query.get_or_404(user_id)
    data = request.get_json()

    new_username = data.get("username", "").strip()
    if new_username and new_username != user.username:
        if AdminUser.query.filter_by(username=new_username).first():
            return jsonify({"error": "El nombre de usuario ya existe"}), 400
        user.username = new_username

    new_email = data.get("email", "").strip()
    if new_email and new_email != user.email:
        if AdminUser.query.filter_by(email=new_email).first():
            return jsonify({"error": "El email ya está registrado"}), 400
    user.email     = new_email or None
    user.full_name = data.get("full_name", "").strip() or None
    user.is_active = data.get("is_active", user.is_active)

    if data.get("new_password"):
        if len(data["new_password"]) < 6:
            return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
        user.password_hash = generate_password_hash(data["new_password"])

    db.session.commit()
    return jsonify(user.to_dict()), 200

# ── Eliminar usuario ───────────────────────────────────────────
@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    current_id = int(get_jwt_identity())
    if current_id == user_id:
        return jsonify({"error": "No puedes eliminar tu propio usuario"}), 400
    user = AdminUser.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200
