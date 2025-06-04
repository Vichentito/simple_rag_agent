# 🧠 Simple RAG Agent

Asistente local para explorar opiniones de clientes por sucursal y tema usando RAG (Retrieval-Augmented Generation) con FastAPI + Chroma + OpenAI Embeddings.

---

## 🚀 ¿Qué hace?

Este proyecto carga opiniones de clientes desde un archivo CSV (`base.csv`), genera embeddings con OpenAI y permite realizar preguntas en lenguaje natural como:

- "¿Qué opinan de la sección 5?"
- "¿Qué dicen del café?"
- "¿Qué les pareció el servicio en la sucursal de Lomas Verdes?"

Utiliza un modelo RAG básico para recuperar los comentarios más relevantes y (opcionalmente) generar una respuesta resumida basada en ellos.

---

## 🧱 Estructura del proyecto

```

simple\_rag\_agent/
│
├── chat/
│   ├── api/
│   │   ├── main.py          ← API con FastAPI
│   │   ├── processor.py     ← Procesador de feedback y embeddings
│   │   └── base.csv         ← Fuente de datos
│   └── frontend/            ← (Pendiente) Interfaz web
│
├── .env                     ← Clave de API de OpenAI
└── README.md

````

---

## ⚙️ Requisitos

- Python 3.13 o superior
- Cuenta de OpenAI con clave de API

---

## 📦 Instalación

1. **Clona el repositorio**

```bash
git clone https://github.com/Vichentito/simple_rag_agent.git
cd simple_rag_agent/chat/api
````

2. **Crea y activa un entorno virtual (opcional pero recomendado)**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala dependencias**

```bash
pip install -r requirements.txt
```

4. **Crea el archivo `.env`**

En `chat/api/.env` coloca tu clave de OpenAI:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## ▶️ Ejecutar el API

Desde `chat/api/`:

```bash
python main.py
```

Esto lanzará el servidor en:

```
http://localhost:3000
```

---

## ⏳ Nota importante

> **La primera vez que ejecutes el proyecto puede tardar varios minutos**, ya que se generarán los embeddings de todos los comentarios utilizando la API de OpenAI.

---

## 📤 Endpoint de consulta

`POST /chat`

**Ejemplo de payload JSON:**

```json
{
  "pregunta": "¿Qué opinan de la sección 4?"
}
```

**Respuesta:**

```json
{
  "pregunta": "¿Qué opinan de la sección 4?",
  "seccion_detectada": "4",
  "respuestas": [
    "El estacionamiento es malo.",
    "Lo único malo es que cobran el estacionamiento.",
    ...
  ]
}
```

---

## 🖥️ Frontend

Se planea agregar una interfaz web con Vue o React para realizar preguntas al agente de forma visual. Por ahora, puedes usar herramientas como [Hoppscotch](https://hoppscotch.io/) o Postman para probar la API.

---

## 📌 TODO

* [ ] Interfaz web en `chat/frontend/`
* [ ] Panel para ver sucursales y temas frecuentes
* [ ] Almacenamiento en la nube para evitar regenerar embeddings

---

## 📄 Licencia

MIT - Hecho con ❤️ por [Vichentito](https://github.com/Vichentito)
