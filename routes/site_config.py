from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.site_config import SiteConfig
from database import db
import os, base64, uuid
from werkzeug.utils import secure_filename

site_config_bp = Blueprint('site_config', __name__)

VALID_KEYS = {
    # ── Hero home ──────────────────────────────────────────────────
    'home_hero_tag', 'home_hero_title', 'home_hero_subtitle',
    'home_hero_cta_primary_text', 'home_hero_cta_primary_url',
    'home_hero_cta_secondary_text',
    'home_stats_projects', 'home_stats_clients', 'home_stats_years',
    'home_slider_label_left', 'home_slider_label_right',
    # ── Sección "¿Cómo le ayudamos?" ──────────────────────────────
    'home_services_title',
    'home_service_a_icon', 'home_service_a_name', 'home_service_a_desc',
    'home_service_b_icon', 'home_service_b_name', 'home_service_b_desc',
    'home_service_c_icon', 'home_service_c_name', 'home_service_c_desc',
    # ── Proceso ───────────────────────────────────────────────────
    'home_process_title',
    'home_process_1_num', 'home_process_1_title', 'home_process_1_desc',
    'home_process_2_num', 'home_process_2_title', 'home_process_2_desc',
    'home_process_3_num', 'home_process_3_title', 'home_process_3_desc',
    'home_process_4_num', 'home_process_4_title', 'home_process_4_desc',
    # ── CTA home ──────────────────────────────────────────────────
    'home_cta_title', 'home_cta_desc',
    # ── Imágenes hero ─────────────────────────────────────────────
    'hero_chaos_image', 'hero_order_image',
    # ── Servicios hero ────────────────────────────────────────────
    'services_hero_tag', 'services_hero_title', 'services_hero_subtitle',
    # ── Servicios cards ───────────────────────────────────────────
    'service_1_name', 'service_1_short', 'service_1_desc',
    'service_1_features', 'service_1_wa',
    'service_2_name', 'service_2_short', 'service_2_desc',
    'service_2_features', 'service_2_wa',
    'service_3_name', 'service_3_short', 'service_3_desc',
    'service_3_features', 'service_3_wa',
    'service_4_name', 'service_4_short', 'service_4_desc',
    'service_4_features', 'service_4_wa',
    # ── ¿Por qué EDO? ─────────────────────────────────────────────
    'services_why_title',
    'services_why_1_icon', 'services_why_1_title', 'services_why_1_desc',
    'services_why_2_icon', 'services_why_2_title', 'services_why_2_desc',
    'services_why_3_icon', 'services_why_3_title', 'services_why_3_desc',
    'services_why_4_icon', 'services_why_4_title', 'services_why_4_desc',
    'services_why_5_icon', 'services_why_5_title', 'services_why_5_desc',
    'services_why_6_icon', 'services_why_6_title', 'services_why_6_desc',
    # ── CTA servicios ─────────────────────────────────────────────
    'services_cta_title', 'services_cta_desc',
    # ── Nosotros hero ─────────────────────────────────────────────
    'about_hero_tag', 'about_hero_title', 'about_hero_subtitle',
    'about_stats_projects', 'about_stats_years',
    # ── Historia ──────────────────────────────────────────────────
    'about_history_title',
    'about_history_p1', 'about_history_p2', 'about_history_p3',
    # ── Valores ───────────────────────────────────────────────────
    'about_values_title',
    'about_value_1_icon', 'about_value_1_title', 'about_value_1_desc',
    'about_value_2_icon', 'about_value_2_title', 'about_value_2_desc',
    'about_value_3_icon', 'about_value_3_title', 'about_value_3_desc',
    'about_value_4_icon', 'about_value_4_title', 'about_value_4_desc',
    'about_value_5_icon', 'about_value_5_title', 'about_value_5_desc',
    'about_value_6_icon', 'about_value_6_title', 'about_value_6_desc',
    # ── Timeline ──────────────────────────────────────────────────
    'about_timeline_1_year', 'about_timeline_1_title', 'about_timeline_1_desc',
    'about_timeline_2_year', 'about_timeline_2_title', 'about_timeline_2_desc',
    'about_timeline_3_year', 'about_timeline_3_title', 'about_timeline_3_desc',
    'about_timeline_4_year', 'about_timeline_4_title', 'about_timeline_4_desc',
    'about_timeline_5_year', 'about_timeline_5_title', 'about_timeline_5_desc',
    # ── Contacto ──────────────────────────────────────────────────
    'contact_email', 'contact_phone', 'contact_whatsapp',
    'contact_address', 'contact_city', 'contact_schedule',
    # ── General / SEO ─────────────────────────────────────────────
    'site_name', 'site_tagline', 'site_description', 'site_keywords',
    'social_instagram', 'social_linkedin', 'social_facebook',
}

@site_config_bp.route('/', methods=['GET'])
def get_all():
    rows = SiteConfig.query.all()
    return jsonify({r.key: r.value for r in rows})

@site_config_bp.route('/<key>', methods=['GET'])
def get_one(key):
    row = SiteConfig.query.filter_by(key=key).first()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({row.key: row.value})

@site_config_bp.route('/bulk', methods=['POST'])
@jwt_required()
def bulk_update():
    data = request.get_json()
    updates = data.get('updates', {})
    invalid = [k for k in updates if k not in VALID_KEYS]
    if invalid:
        return jsonify({'error': f'Claves inválidas: {invalid}'}), 400
    try:
        for key, value in updates.items():
            row = SiteConfig.query.filter_by(key=key).first()
            if row:
                row.value = value
            else:
                db.session.add(SiteConfig(key=key, value=value))
        db.session.commit()
        return jsonify({'ok': True, 'updated': len(updates)})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@site_config_bp.route('/upload-image', methods=['POST'])
@jwt_required()
def upload_image():
    data = request.get_json()
    key      = data.get('key')
    file_b64 = data.get('file')
    filename = data.get('filename', 'image.jpg')
    if key not in ('hero_chaos_image', 'hero_order_image'):
        return jsonify({'error': 'Clave de imagen no válida'}), 400
    try:
        if ',' in file_b64:
            file_b64 = file_b64.split(',')[1]
        file_bytes = base64.b64decode(file_b64)
        ext        = os.path.splitext(secure_filename(filename))[1] or '.jpg'
        fname      = f"{key}_{uuid.uuid4().hex[:8]}{ext}"
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        with open(os.path.join(upload_dir, fname), 'wb') as f:
            f.write(file_bytes)
        path = f'/static/uploads/{fname}'
        row  = SiteConfig.query.filter_by(key=key).first()
        if row:
            row.value = path
        else:
            db.session.add(SiteConfig(key=key, value=path))
        db.session.commit()
        return jsonify({'ok': True, 'path': path})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
