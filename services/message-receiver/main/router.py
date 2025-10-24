from .settings import DATABASE_APPS_MAPPING


class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in DATABASE_APPS_MAPPING:
            return DATABASE_APPS_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in DATABASE_APPS_MAPPING:
            return DATABASE_APPS_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db1 = DATABASE_APPS_MAPPING.get(obj1._meta.app_label)
        db2 = DATABASE_APPS_MAPPING.get(obj2._meta.app_label)
        if db1 and db2:
            return db1 == db2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in DATABASE_APPS_MAPPING:
            return DATABASE_APPS_MAPPING[app_label] == db
        return None
