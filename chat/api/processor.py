import os
import re
import pandas as pd
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import tiktoken

# Cargar la clave de OpenAI desde .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class FeedbackProcessor:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self.df.dropna(subset=["comentario_limpio"], inplace=True)

        # Configurar la función de embedding de OpenAI
        self.embedding_function = OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY, model_name="text-embedding-3-small"
        )

        # Inicializar ChromaDB en modo persistente con la función de embedding
        self.client_chroma = chromadb.PersistentClient(path="chroma_store")
        self.collection = self.client_chroma.get_or_create_collection(
            name="opiniones", embedding_function=self.embedding_function
        )

        self._index_data()

    def _index_data(self):
        if self.collection.count() == 0:
            textos = self.df["comentario_limpio"].astype(str).tolist()
            secciones = self.df["seccion"].astype(str).tolist()
            ids = [f"doc_{i}" for i in range(len(textos))]
            metadatas = [{"seccion": sec} for sec in secciones]

            # Inicializar el codificador de tokens
            encoder = tiktoken.encoding_for_model("text-embedding-3-small")

            # Límite de tokens por solicitud
            MAX_TOKENS = 8191

            batch_texts = []
            batch_ids = []
            batch_metadatas = []
            batch_token_count = 0

            for texto, id_doc, metadata in zip(textos, ids, metadatas):
                tokens = encoder.encode(texto)
                num_tokens = len(tokens)

                # Si agregar este texto excede el límite, enviar el lote actual
                if batch_token_count + num_tokens > MAX_TOKENS:
                    self.collection.add(
                        documents=batch_texts, metadatas=batch_metadatas, ids=batch_ids
                    )
                    batch_texts = []
                    batch_ids = []
                    batch_metadatas = []
                    batch_token_count = 0

                batch_texts.append(texto)
                batch_ids.append(id_doc)
                batch_metadatas.append(metadata)
                batch_token_count += num_tokens

            # Agregar cualquier texto restante
            if batch_texts:
                self.collection.add(
                    documents=batch_texts, metadatas=batch_metadatas, ids=batch_ids
                )

    def detect_section_filter(self, pregunta: str):
        pregunta = pregunta.lower()

        # Mapeo de palabras a números
        palabras_a_numeros = {
            "uno": "1",
            "dos": "2",
            "tres": "3",
            "cuatro": "4",
            "cinco": "5",
            "seis": "6",
            "siete": "7",
            "ocho": "8",
            "nueve": "9",
            "diez": "10",
        }

        match = re.search(r"secci[oó]n\s+(\d+)", pregunta)
        if match:
            return match.group(1)

        match_palabra = re.search(r"secci[oó]n\s+(\w+)", pregunta)
        if match_palabra:
            palabra = match_palabra.group(1)
            return palabras_a_numeros.get(palabra)

        return None

    def search_similar_feedback(self, query: str, top_k: int = 10):
        seccion = self.detect_section_filter(query)
        filters = {"seccion": seccion} if seccion else None

        results = self.collection.query(
            query_texts=[query], n_results=top_k, where=filters
        )

        return {
            "pregunta": query,
            "seccion_detectada": seccion,
            "respuestas": (
                results["documents"][0] if results and results["documents"] else []
            ),
        }
