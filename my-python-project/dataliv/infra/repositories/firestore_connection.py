import json
import firebase_admin
from firebase_admin import credentials, firestore
from dataliv.infra.settings import AppSettings

settings = AppSettings()

class FirestoreConnection:
    def __init__(self):
        self.jls_extract_def()

    def jls_extract_def(self):
        try:
            self.certificate = settings.firestore_certificate
            self.db_id =settings.firestore_db_id
            self.collection_db = settings.firestore_collection_db

            if not self.certificate:
                raise ValueError("Firestore certificate is not set")

            json_cert = json.loads(self.certificate, strict=False)
            cred = credentials.Certificate(json_cert)
            firebase_admin.initialize_app(cred)
            self.db = firestore.client(database_id=self.db_id)
            self.collection = self.db.collection(self.collection_db)
        except Exception as e:
            raise ValueError(f"Failed to initialize a certificate credential: {e}")

    def initialize(self):
        return self.collection
        # try:
        #     return self.collection
        # except Exception as e:
        #     print(f'Error initializing Firestore: {e}')
        #     return None

    def get_collection(self):
        if self.collection is None:
            return self.initialize()
        return self.collection