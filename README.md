# Low Light Image Enhancement Project

## Project Note / Disclaimer

- **Current Ownership & Scope:** This project is currently maintained, developed, and owned solely by Jonkkeyler333.
- **Legacy Contributions:** Previous commits from early experimental stages (for example, initial exploratory scripts) belonged to former collaborators. Those legacy algorithms and functions have been removed or deprecated and are not part of the active codebase.
<!-- 

Este repositorio explora diversas metodologías para el mejoramiento de imágenes capturadas en condiciones de baja iluminación (low-light image enhancement). El proyecto abarca desde métodos y optimizaciones clásicas hasta un enfoque profundo basado en redes neuronales (Deep Learning).



3. **SCI (Self-Calibrated Illumination) - Enfoque Principal**:
   Ubicado en el directorio `sci/`. Este es el módulo más robusto del proyecto, donde se implementa un modelo de aprendizaje profundo utilizando PyTorch.

---

## Resumen (propuesta para portafolio)

Proyecto de mejora de imágenes en condiciones de baja iluminación que combina una arquitectura en capas (API REST con FastAPI) y un motor de inferencia basado en PyTorch. Incluye endpoints para autenticación, gestión de usuarios y registros de inferencia, además de código para entrenamiento e inferencia del modelo SCI (Self-Calibrated Illumination).

El README se organiza en secciones: Tecnologías, Arquitectura, Modelo, Motivación, Objetivos, Instalación, Ejecución, Testing, Variables de entorno y Buenas prácticas.

---

## Tecnologías

- Python 3.12+
- FastAPI (API REST)
- Beanie (ODM para MongoDB, sobre Motor)
- Motor (Async MongoDB driver)
- PyMongo (para compatibilidad y utilidades)
- PyTorch (modelo SCI y entrenamiento)
- Pillow, OpenCV, numpy, scikit-image (procesamiento de imágenes)
- PyJWT (JWT auth)
- pwdlib (hashing seguro de contraseñas)
- pytest / httpx / pytest-asyncio (testing)

Dependencias principales están en `backend/pyproject.toml` y `requirements.txt`.

## Arquitectura (en capas)

La aplicación sigue una arquitectura organizada por responsabilidades:

- `controllers` (API layer): rutas y validaciones (FastAPI routers).
- `services` (business logic): orquestan operaciones, reglas de negocio y llamadas a repositorios.
- `repositories` (data access): encapsulan accesos a la base de datos usando modelos Beanie.
- `models` (domain models): modelos Beanie/Pydantic (`User`, `InfereceLog`).
- `dependencies` (infra): inicialización de base de datos, dependencias de FastAPI.
- `schemas` (DTOs): Pydantic schemas para requests/responses.
- `inference` (ML engine): motor PyTorch para carga de modelos e inferencia (`SciEngine`).

Esta separación facilita pruebas, mantenimiento y permite exponer solo la capa necesaria a la API.

## Modelo

- En `sci/` se implementa el modelo principal tipo SCI (Self-Calibrated Illumination).
- Entrenamiento e inferencia se realizan con PyTorch; checkpoints (`.pth`) se almacenan en `sci/checkpoints/`.
- El repo incluye utilidades para evaluación (PSNR, SSIM) y scripts de inferencia para procesar imágenes de entrada.

## Motivación

Las imágenes capturadas en condiciones de baja iluminación sufren pérdida de detalle, ruido y baja relación señal/ruido. El objetivo de este proyecto es aplicar técnicas de deep learning para restaurar detalle, mejorar la exposición y producir imágenes visualmente útiles y cuantificables mediante métricas (PSNR/SSIM).

## Objetivos

- Crear una API REST que permita subir imágenes, ejecutar la inferencia sobre un modelo entrenado y almacenar logs de uso.
- Proveer endpoints para la gestión de usuarios y autenticación basada en JWT con cookies.
- Mantener una estructura limpia en capas que facilite testing y desarrollo iterativo.
- Incluir pipelines reproducibles para entrenamiento e inferencia y facilitar evaluación con métricas.

## Instalación rápida

1. Clona el repo:

```bash
git clone <repo-url>
cd low_light_enhancement_project/backend
```

2. Crea y activa un entorno virtual (recomendado) e instala dependencias:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r ../requirements.txt
# o usar poetry: poetry install
```

3. Variables de entorno: configura `backend/src/app/.env` o exporta variables necesarias:

- `MONGODB_URI` : URI de producción/ desarrollo (MongoDB Atlas)
- `MONGODB_URI_TEST` : URI para pruebas
- `SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`
- `ENVIRONMENT` : setear a `development` o `test` según corresponda

## Ejecutar la API (desarrollo)

```bash
cd backend
uvicorn app.main:app --reload
```

Para evitar que los tests modifiquen la base de datos de desarrollo:

1. Asegura que `ENVIRONMENT=test` esté configurado antes de importar la app en tus tests (por ejemplo, en `tests/conftest.py`).
2. Inicializa Beanie con una instancia `Database` explícita (usar Motor) para apuntar a la base de tests.

## Testing

Se emplea `pytest` con `pytest-asyncio` y `httpx` para tests de integración. Ejecuta:

```bash
pytest -q
```

Consejo: exporta `ENVIRONMENT=test` en tu entorno de CI o en la sesión antes de ejecutar tests para evitar inicializaciones que afecten la base de desarrollo.

## Variables de entorno (ejemplo)

El archivo `backend/src/app/.env` contiene:

- `APP_NAME`, `IMAGE_SIZE_MAX`, `MODEL_PATH`, `ALLOWED_EXTENSIONS`, `MAX_CONTENT_LENGTH`
- `MONGODB_URI`, `MONGODB_URI_TEST`
- `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `SECRET_KEY`, `ENVIRONMENT`

Evita commitear credenciales reales en el repositorio; usa secret managers o variables de entorno del CI.

## Buenas prácticas y mejoras sugeridas

- Usar una URI de MongoDB separada para tests o un MongoDB in-memory / contenedor aislado.
- Inicializar Beanie con `motor.motor_asyncio.AsyncIOMotorClient` y pasar `client.get_default_database()` o `client['db_test']` a `init_beanie` para evitar ambigüedades.
- Añadir CI que ejecute tests en una base de datos efímera y que no exponga credenciales.
- Añadir documentación de API (OpenAPI/Redoc) y ejemplos de uso en `docs/`.

---

Si quieres, puedo:

 - Generar una versión en inglés del README.
 - Añadir ejemplos de requests curl o un Postman collection.
 - Preparar parches para convertir `conftest.py` y `dependencies/database.py` a usar `motor` y evitar que la BD de desarrollo se borre.

Gracias — dime qué quieres que haga a continuación.