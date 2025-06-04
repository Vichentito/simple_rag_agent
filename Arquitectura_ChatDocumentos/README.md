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


## Diagnóstico y Evolución del Sistema

A continuación se presentan estrategias específicas para abordar dos desafíos comunes en la operación y mantenimiento de sistemas basados en RAG y modelos de lenguaje.

### 1. Diagnóstico y mejora ante respuestas imprecisas o demasiado generales

Si el sistema comienza a generar respuestas poco precisas, genéricas o irrelevantes, se debe realizar un diagnóstico estructurado considerando los siguientes puntos:

**Diagnóstico del problema:**

* **Revisar el proceso de recuperación (retrieval):**

  * Verificar si el embedding de la pregunta está recuperando fragmentos relevantes.
  * Analizar el top-k retornado por la base vectorial o grafo (en caso de usar GraphRAG).
  * Comprobar si hay falta de filtrado efectivo por documento o contexto temático.

* **Auditar el contenido del índice vectorial:**

  * Validar que los documentos estén correctamente segmentados y embebidos.
  * Confirmar que los metadatos estén completos (por ejemplo, `doc_id`, `tipo`, `tema`, etc.).
  * Detectar posibles errores en el chunking que provoquen pérdida de contexto.

* **Evaluar el prompt enviado al modelo de lenguaje:**

  * Asegurarse de que el prompt contenga suficiente contexto útil.
  * Verificar si la longitud o el formato del prompt está afectando el rendimiento del modelo.

* **Analizar el modelo de lenguaje utilizado:**

  * Comparar el desempeño con otros modelos (por ejemplo, cambiar entre GPT-4, Claude, o modelos open-source).
  * Comprobar si se requiere ajuste en parámetros como temperatura, top\_p o max\_tokens.

**Medidas correctivas y de mejora:**

* Mejorar la estrategia de chunking utilizando métodos semánticos o mixtos (por ejemplo, sliding window con delimitación lógica).
* Implementar una capa de re-ranking (por ejemplo, con modelos cross-encoder) para priorizar los fragmentos más útiles antes de construir el prompt.
* Aplicar logging y trazabilidad para depurar qué documentos y fragmentos se usan en cada respuesta.
* Realizar fine-tuning de un modelo propio si el dominio lo justifica (por ejemplo, entrenamiento adicional con ejemplos de entrevistas del negocio).
* Ajustar el top-k dinámicamente en función de la longitud de la pregunta o el tema.

### 2. Introducción de una nueva política de respuesta (por ejemplo: no mencionar temas sensibles)

Cuando es necesario introducir una política nueva (por ejemplo, evitar respuestas que mencionen temas sensibles como religión, salud personal, etc.), esta debe implementarse de forma transparente para el usuario final. Las siguientes estrategias están alineadas con prácticas actuales del mercado:

**Estrategia de implementación no disruptiva:**

* **Inyección de instrucciones en el prompt:**

  * Incorporar políticas directamente en el prompt de sistema enviado al modelo.
  * Ejemplo: “Responde con base en los documentos seleccionados, evitando mencionar temas relacionados con salud, religión o política a menos que sea estrictamente relevante y esté contenido explícitamente en los documentos.”

* **Uso de content filters o moderation layers:**

  * Implementar una capa de moderación posterior (post-processing) que detecte y bloquee respuestas que violen políticas mediante clasificadores ligeros o reglas.
  * Herramientas como OpenAI’s content filter, Google’s safety settings, o clasificadores custom (zero-shot o few-shot) pueden integrarse sin alterar la experiencia.

* **Refuerzo mediante recuperación filtrada:**

  * Excluir fragmentos que contengan información sensible durante la fase de recuperación.
  * Esto se logra mediante metadatos temáticos o etiquetas asignadas en el momento de la indexación (por ejemplo, `tema: salud` → excluido si está en blacklist activa).

* **Validación y testeo en entorno sombra:**

  * Antes de aplicar en producción, validar las nuevas políticas usando un entorno de "shadow deployment" para comparar la salida del modelo con y sin política.
  * Esto permite medir impacto, identificar excepciones y ajustar sin interrupciones.

**Ventajas de este enfoque:**

* No requiere detener el servicio ni cambiar el modelo base.
* Permite actualizar políticas rápidamente.
* Escalable a múltiples idiomas, dominios o niveles de sensibilidad.
* Transparente para el usuario final mientras refuerza el cumplimiento normativo.

---