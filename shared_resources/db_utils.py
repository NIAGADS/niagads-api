from filer.cache import initialize_metadata_cache

def create_tables(db, app, bind):
    with app.app_context():
        if bind in ['filer', 'all']:
            # db.drop_all('filer')
            # db.create_all('filer')
            initialize_metadata_cache(db, app.config['FILER_METADATA_TEMPLATE_FILE'], app.config['DEBUG'])
            
        if bind in ['cache', 'all']:
            True
            # db.drop_all('cache')
            # db.create_all('cache')
    