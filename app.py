from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from database import db
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.blog import blog_bp
from routes.contact import contact_bp
from routes.site_config import site_config_bp
import os
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)

    # ── Config ──────────────────────────────────────────────────
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/edo_web"
    ).replace("postgres://", "postgresql://")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "edo-secret-dev-2025")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400  # 24h

    # ── Extensions ──────────────────────────────────────────────
    db.init_app(app)
    JWTManager(app)
    CORS(app, resources={r"/api/*": {"origins": os.environ.get("FRONTEND_URL", "*")}})

    # ── Blueprints ──────────────────────────────────────────────
    app.register_blueprint(auth_bp,         url_prefix="/api/auth")
    app.register_blueprint(projects_bp,     url_prefix="/api/projects")
    app.register_blueprint(blog_bp,         url_prefix="/api/blog")
    app.register_blueprint(contact_bp,      url_prefix="/api/contact")
    app.register_blueprint(site_config_bp,  url_prefix="/api/site-config")

    # ── Init DB + seed ──────────────────────────────────────────
    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    from models.project import Project
    from models.blog_post import BlogPost
    from models.admin_user import AdminUser
    from werkzeug.security import generate_password_hash

    if not AdminUser.query.first():
        admin = AdminUser(
            username="admin",
            password_hash=generate_password_hash("edo2025")
        )
        db.session.add(admin)

    if not Project.query.first():
        projects = [
            Project(
                name="EDO Gestión Mantenimiento",
                category="Sistema de Gestión",
                stack="Angular,Flask,PostgreSQL,Railway",
                status="En producción",
                description="Sistema integral GMAO multi-sede. Órdenes de trabajo, inspecciones móviles, PAC, Kanban y dashboard con KPIs en tiempo real.",
                highlights="Ciclo completo de órdenes con PDF automático|Inspecciones con foto y voz a texto|PAC con importación masiva desde Excel|Roles y permisos por empresa",
                color="#1B4B8A", featured=True, order=1
            ),
            Project(
                name="DYD Suministros y Servicios",
                category="E-commerce B2B",
                stack="Angular,Flask,PostgreSQL",
                status="En producción",
                description="Plataforma B2B para suministros de construcción. Catálogo, aprobación de clientes y programa de fidelización por puntos.",
                highlights="Catálogo responsivo con filtros avanzados|Registro con aprobación admin|Sistema de puntos por niveles|Panel de métricas de ventas",
                color="#2563EB", featured=False, order=2
            ),
            Project(
                name="Sistemas de Facturación DIAN",
                category="Automatización",
                stack="Google Apps Script,Sheets,Drive",
                status="Activo",
                description="Automatización completa de importación y gestión de facturas DIAN con detección de duplicados por CUFE/CUDE.",
                highlights="Importador dual DIAN/Sistema|Detección automática de duplicados|Generación de PDFs de facturas|Multi-empresa TTM Builders LLC",
                color="#0F766E", featured=False, order=3
            ),
            Project(
                name="Préstamos Flex",
                category="Gestión Financiera",
                stack="Google Apps Script,Sheets",
                status="Activo",
                description="Sistema de cartera con cobranza quincenal al 5% sobre saldo, reestructuración de planes y seguimiento de pagos.",
                highlights="Cobranza quincenal automatizada|Reestructuración de planes|Historial de pagos por cliente|Formato fecha colombiano DD-MM-AAAA",
                color="#7C3AED", featured=False, order=4
            ),
        ]
        db.session.bulk_save_objects(projects)

    if not BlogPost.query.first():
        posts = [
            BlogPost(
                title="¿Por qué su empresa sigue usando Excel para gestionar el mantenimiento?",
                excerpt="El 68% de las empresas colombianas medianas aún dependen de hojas de cálculo. Le mostramos el costo real de esa decisión.",
                content="Contenido completo del artículo...",
                category="Análisis", read_time="5 min", published=True
            ),
            BlogPost(
                title="De WhatsApp a sistema: cómo digitalizamos la gestión de 3 sedes en 60 días",
                excerpt="Caso real de implementación de EDO Gestión Mantenimiento para una empresa de servicios industriales en Córdoba.",
                content="Contenido completo del artículo...",
                category="Caso de éxito", read_time="8 min", published=True
            ),
            BlogPost(
                title="Angular + Flask + PostgreSQL: el stack ideal para sistemas empresariales en Colombia",
                excerpt="Por qué elegimos esta combinación tecnológica para todos nuestros proyectos y qué ventajas concretas tiene para el cliente final.",
                content="Contenido completo del artículo...",
                category="Técnico", read_time="6 min", published=True
            ),
        ]
        db.session.bulk_save_objects(posts)

    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    # Puerto 5001 – no interfiere con EDO Gestión Mantenimiento (:5000)
    app.run(debug=True, host="0.0.0.0", port=5001)
