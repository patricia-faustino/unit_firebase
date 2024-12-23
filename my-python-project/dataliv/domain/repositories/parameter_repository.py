from dataliv.infra.repositories.firestore_connection import FirestoreConnection
from dataliv.domain.entities.parameter_entity import ParameterEntity

class ParameterRepository:
    
    def __init__(self, firestore_connection: FirestoreConnection):
        self.collection = firestore_connection.get_collection()
        
        
    def get_parameter(self, source_object_name, source_schema_name):
       
        doc_ref = self.collection.document(f"{source_object_name}_{source_schema_name}")
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None
        
    def set_parameter(self, parameter_table: ParameterEntity):
        try:
            doc_ref = self.collection.document(f"{parameter_table.source_object_name}_{parameter_table.source_schema_name}").set(parameter_table.model_dump())
            return doc_ref
        except Exception as e:
            print(f'Error setting parameter: {e}')
            return None