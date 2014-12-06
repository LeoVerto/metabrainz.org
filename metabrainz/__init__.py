from flask import Flask


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config.from_object('metabrainz.config')

    if app.debug:
        # Debug toolbar
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True

    # Database
    from model import db
    db.init_app(app)

    from utils import reformat_datetime
    app.jinja_env.filters['datetime'] = reformat_datetime

    # Blueprints
    from views import index_bp
    from finances.views import finances_bp
    from support.views import support_bp
    from reports.views import reports_bp
    from donations.views import donations_bp

    app.register_blueprint(index_bp)
    app.register_blueprint(finances_bp, url_prefix='/finances')
    app.register_blueprint(support_bp, url_prefix='/support')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(donations_bp, url_prefix='/donations')

    # Admin section
    from flask_admin import Admin
    admin = Admin(app, name='Danger Zone')

    from metabrainz.model.tier import TierAdminView
    from metabrainz.model.organization import OrganizationAdminView
    from metabrainz.model.donation import DonationAdminView

    admin.add_view(TierAdminView(db.session))
    admin.add_view(OrganizationAdminView(db.session))
    admin.add_view(DonationAdminView(db.session))

    return app
