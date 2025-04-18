class MultiDBRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'resumes':
            return 'mongo'
        return 'default'

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'resumes':
            return db == 'mongo'
        return db == 'default'
