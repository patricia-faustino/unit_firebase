from environs import Env

_env = Env()
_env.read_env()


class AppSettings:
    with _env.prefixed('FIRESTORE_'):
        firestore_certificate = _env('CERTIFICATE', default=None)
        firestore_db_id = _env('DB_ID', default="firestore_db_id")
        firestore_collection_db = _env('COLLECTION_DB', default="collection_db")