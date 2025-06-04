# Sistema de Chat con Documentos Internos (Arquitectura RAG)

Este repositorio describe una arquitectura de referencia para construir un sistema que permite a los usuarios interactuar con sus propios documentos mediante una interfaz de chat. La solución está basada en la técnica de Retrieval-Augmented Generation (RAG), que combina búsqueda semántica y modelos de lenguaje para generar respuestas basadas en contenido previamente cargado.

## Objetivo

El sistema está diseñado para:

* Permitir la carga de documentos confidenciales (por ejemplo, transcripciones de entrevistas o focus groups).
* Procesar e indexar dichos documentos de manera segura y eficiente.
* Permitir a los usuarios seleccionar con qué documentos desean interactuar.
* Brindar una interfaz conversacional que genere respuestas basadas en el contenido cargado.

## Componentes

### Frontend

* Aplicación web desarrollada en Next.js.
* Permite subir documentos, gestionarlos y realizar preguntas a través de un chat.
* Incluye un selector para indicar con qué documentos debe trabajar el modelo.

### Backend

* API desarrollada en Python, encargada del procesamiento de documentos, generación de embeddings, recuperación semántica y conexión con el modelo de lenguaje.
* Se propone utilizar frameworks como LangChain o LlamaIndex. Ambos permiten construir flujos RAG de forma modular. Se recomienda realizar pruebas con ambos para evaluar su rendimiento, escalabilidad y facilidad de mantenimiento.

### Almacenamiento

* Documentos originales almacenados de forma segura en servicios como AWS S3 o Google Cloud Storage.
* Embeddings y metadatos almacenados en una base vectorial como FAISS, Chroma, Pinecone o bases SQL con extensión pgvector.

### Modelo de Lenguaje

* Puede utilizarse un modelo privado (por ejemplo, LLaMA 2 desplegado localmente) o un proveedor en la nube (OpenAI, Amazon Bedrock, Vertex AI).
* La elección debe considerar restricciones de privacidad, latencia y costo.

## Flujo de Ingesta de Documentos

El flujo de procesamiento comienza cuando un usuario carga un nuevo documento. A continuación se muestra un diagrama del proceso de carga e indexación, que incluye:

* Recepción del archivo por el backend.
* Almacenamiento seguro del documento.
* Extracción del texto y segmentación en fragmentos.
* Generación de embeddings de cada fragmento.
* Almacenamiento de los vectores junto con metadatos (por ejemplo, ID del documento, título, fecha).

![procesado_data](https://github.com/user-attachments/assets/9e60a1b8-903b-4a62-a60d-25b24ca13077)

## Flujo de Consulta y Generación

El flujo de consulta ocurre cuando el usuario desea hacer preguntas sobre los documentos cargados. El sistema realiza los siguientes pasos:

* Recepción de la pregunta desde el frontend.
* Generación del embedding de la pregunta.
* Consulta al vector store para recuperar fragmentos relevantes, aplicando filtros si el usuario ha seleccionado documentos específicos.
* Construcción de un prompt que incluye la pregunta y los fragmentos recuperados como contexto.
* Llamada al modelo de lenguaje para generar la respuesta.
* Envío de la respuesta al frontend.

![chat_data](https://github.com/user-attachments/assets/83166e0c-4074-405f-94b0-59af64276475)

## Seguridad y Privacidad

Dado que los documentos pueden contener información sensible, la arquitectura contempla lo siguiente:

* Almacenamiento cifrado en reposo y en tránsito.
* Acceso autenticado y autorizado por usuario.
* Filtrado de resultados en función de los documentos seleccionados por el usuario.
* Posibilidad de utilizar modelos de lenguaje autoalojados o servicios con garantías de no retención de datos.
* Eliminación de documentos implica también la eliminación de sus vectores asociados en la base vectorial.

## Opciones de Despliegue

El sistema puede desplegarse en:

* **AWS**: usando S3 para almacenamiento, Amazon OpenSearch o Bedrock para recuperación/generación, y servicios serverless o contenedores para el backend.
* **GCP**: usando Cloud Storage, Vertex AI para el modelo y AlloyDB con pgvector para embeddings.

La arquitectura es modular y puede adaptarse a diferentes proveedores o infraestructuras locales según los requisitos de la organización.

## Consideraciones adicionales

* **Uso de GraphRAG:** En casos donde el volumen de documentos aumente considerablemente, o si los documentos presentan una estructura temática compleja (por ejemplo, múltiples relaciones entre conceptos, tópicos recurrentes o secuencias temporales), se considerará el uso de enfoques tipo **GraphRAG**. Esta variante del paradigma RAG construye un grafo de conocimiento entre fragmentos y conceptos, permitiendo una recuperación más estructurada y explicativa. Puede implementarse como complemento o sustituto parcial de la base vectorial, dependiendo del análisis de rendimiento y calidad de respuestas en pruebas reales.

* **Técnicas de Chunking:** Por defecto se utilizará una estrategia de **chunking semántico**, que divide el texto en fragmentos coherentes en función del contenido (por ejemplo, por secciones o tópicos). Sin embargo, durante la fase de pruebas también se evaluarán otras estrategias como chunking por longitud fija, sliding window o chunking híbrido. El objetivo será encontrar el balance óptimo entre precisión en la recuperación, desempeño y costo de procesamiento.
