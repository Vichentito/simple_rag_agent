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

---

### 2. Introducción de una nueva política de respuesta (por ejemplo: no mencionar temas sensibles)

Cuando es necesario introducir una política nueva (por ejemplo, evitar respuestas que mencionen temas sensibles como religión, salud personal, política, etc.), esta debe implementarse de forma **segura, gradual y sin afectar la experiencia del usuario final**. A continuación se detallan las estrategias recomendadas, alineadas con las mejores prácticas actuales:

**Estrategia de implementación no disruptiva:**

* **Instrucciones inyectadas en el prompt del modelo:**

  * Se agregan instrucciones claras sobre los temas prohibidos o restringidos al momento de construir el prompt para el modelo de lenguaje.
  * Ejemplo: “Evita responder sobre temas sensibles como salud, religión o política, a menos que estén explícitamente cubiertos en los documentos y sean requeridos por el contexto.”

* **Moderación en capa intermedia (post-procesamiento):**

  * Se introduce un módulo que analiza las respuestas generadas antes de enviarlas al usuario, bloqueando o reformulando aquellas que violen las políticas establecidas.
  * Se pueden usar clasificadores ligeros (zero-shot o few-shot), filtros semánticos o herramientas de proveedores como OpenAI, Vertex AI o moderadores propios.

* **Filtrado anticipado en recuperación:**

  * Se etiquetan los fragmentos de documentos con metadatos temáticos durante el proceso de indexación.
  * Se excluyen de la recuperación aquellos fragmentos que correspondan a temas sensibles, si así lo establece la política activa.

**Estrategias para el despliegue seguro de estos cambios:**

* **Shadow deployment:**

  * Se ejecuta el nuevo flujo de generación (con las políticas aplicadas) en paralelo al actual.
  * Las respuestas generadas no se muestran al usuario, pero se registran para análisis interno y comparación con las actuales.
  * Permite evaluar la efectividad de las nuevas reglas sin impacto en producción.
 
 ![Captura de pantalla 2025-06-04 011814](https://github.com/user-attachments/assets/2ea671eb-5274-48ef-ab90-bbf240bd2702)

* **Canary release:**

  * La nueva política se habilita inicialmente solo para un subconjunto controlado de usuarios reales.
  * Se observa su comportamiento en condiciones reales y se valida que la experiencia no se degrade ni se introduzcan errores.
  * En función de los resultados, se amplía gradualmente su disponibilidad al resto de los usuarios.

 ![Captura de pantalla 2025-06-04 011835](https://github.com/user-attachments/assets/1a651f1f-10b5-4f82-994c-78b2f6acf31e)

**Beneficios de este enfoque combinado:**

* Permite validar cambios complejos sin riesgos.
* Minimiza el impacto negativo en usuarios finales.
* Facilita la toma de decisiones basada en métricas reales (tasa de error, calidad percibida, tasa de rechazo).
* Aumenta la confianza en la robustez del sistema ante nuevas reglas o requisitos regulatorios.

---
