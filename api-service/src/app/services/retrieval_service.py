# TODO:
# Conectarme con la vectorialdb
# Realizar búsquedas semánticas segun queries
class RetrievalService:
    def __init__(self, vs_client):
        self.vectorstore = vs_client
