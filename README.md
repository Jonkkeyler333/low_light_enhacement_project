# Low Light Image Enhancement Project

## 📌 Project Note / Disclaimer

* **Current Ownership & Scope:** This project is currently maintained, developed, and owned solely by **Jonkkeyler333**.
* **Legacy Contributions:** Previous commits from early experimental stages (e.g., initial exploratory scripts from May) belonged to former collaborators. Those legacy algorithms and functions have been fully removed/deprecated from the current codebase and are not part of the active production or architecture.
<!-- 

Este repositorio explora diversas metodologías para el mejoramiento de imágenes capturadas en condiciones de baja iluminación (low-light image enhancement). El proyecto abarca desde métodos y optimizaciones clásicas hasta un enfoque profundo basado en redes neuronales (Deep Learning).

## Estructura del Proyecto

El repositorio está dividido principalmente en tres enfoques:

1. **LIME (Low-light Image Enhancement via Illumination Map Estimation)**: 
   Ubicado en la carpeta `LIME/`, este enfoque tradicional se basa en la estimación de mapas de iluminación mediante un proceso de optimización. Incluye Jupyter Notebooks interactivos (`LIME_LOLdatabase.ipynb` y `LIME_Optimization (2).ipynb`) diseñados para experimentar con la teoría detrás de LIME. Solo es necesario ejecutarlos.

2. **MSR (Multi-Scale Retinex)**:
   Ubicado en la carpeta `Multi-Scale Retinex (MSR)/`, contiene el notebook `LowLight_MSR.ipynb`. Este espacio está dedicado al clásico algoritmo de mejora inspirado en el modelo retiniano humano (Retinex), aplicado en múltiples escalas, para corregir el color e iluminar zonas oscuras de las imágenes.

3. **SCI (Self-Calibrated Illumination) - Enfoque Principal**:
   Ubicado en el directorio `sci/`. Este es el módulo más robusto del proyecto, donde se implementa un modelo de aprendizaje profundo utilizando PyTorch.

---

## SCI (Self-Calibrated Illumination)

Este módulo está preparado para ejecutar ciclos de entrenamiento (train) e inferencia guiados con métricas (PSNR y SSIM).

### Configuración del Entorno de Python

Primero, se instalan las dependencias requeridas. Se recomienda usar un entorno virtual. Ejecuta:

```bash
pip install -r requirements.txt
```

### Conjunto de Datos (LOLDataset)

El modelo está diseñado para entrenarse a partir del conjunto de datos **LOLDataset**. Si se quiere probar, debes descargarlo y descomprimirlo en la carpeta correspondiente.

Puedes descargar los datos (usando `gdown` por ejemplo) y extraerlos en una carpeta `sci/data/` (o bien, reescribir la ruta en `sci/src/config.yaml`). El directorio debería tener una estructura como esta tras la extracción:
- `data/our485/` (entrenamiento)
- `data/eval15/` (validación / pruebas)

*Nota:* Para descargar los datos de manera automatizada de Google Drive, puedes consultar el script provisto en `sci/src/run.ipynb`, que contiene el URL de descarga a utilizar.

### Notas sobre el Colab Notebook (`run.ipynb`)

El archivo [sci/src/run.ipynb](sci/src/run.ipynb) contiene instrucciones empaquetadas **específicamente orientadas para ejecutarse en kernels de Google Colab**. Este notebook provee todos los pasos: desde montar Google Drive y descargar el dataset remotamente, hasta clonar el repo y lanzar el script de entrenamiento, facilitando el uso de las GPUs libres de Colab. No debe utilizarse para correr los scripts interactivamente en tu máquina local.

### Ejecución de Código Local

Para correr los scripts de manera local, asegúrate de estar siempre dentro de la ruta `sci/` y de tener la carpeta `data/` en su lugar o listada de acorde a tu path en el archivo [sci/src/config.yaml](sci/src/config.yaml).

#### Entrenamiento

Para ejecutar el entrenamiento con los hiperparámetros de `src/config.yaml`, ejecuta:

```bash
cd sci
python -m src.train
```

Los checkpoints (`.pth`) del modelo se almacenarán dentro de la carpeta `checkpoints/` junto al registro de logs y métricas.

#### Inferencia

Para evaluar el sistema o realizar predicciones con un modelo previamente entrenado, utiliza el script [sci/src/inference.py](sci/src/inference.py). 

Dentro del código, notarás que hay variables de ruta para la entrada (`input_folder`) y la salida (`output_folder`). Existen dos configuraciones allí (una de ellas comentada):
- **Imágenes del dataset:** Las rutas predeterminadas (ej. `data/eval15/low`) analizan el conjunto de datos de validación, por lo que requieren una carpeta de referencia (`reference_folder`) para calcular las métricas de rendimiento.
- **Imágenes propias:** Las rutas comentadas (ej. `inference/`) están listas para descomentarse en caso de que desees colocar tus propias imágenes oscuras y ver el antes/después del modelo. *(Nota: si evalúas imágenes propias sin un target o ground truth, podrías necesitar comentar la parte del código que calcula PSNR y SSIM con la referencia).*

Asegúrate de apuntar a tu modelo deseado en `model_path` (archivo `.pth`) y luego ejecuta:

Luego ejecuta:

```bash
cd sci
python -m src.inference
```

El script guardará las imágenes mejoradas, junto con gráficos adicionales del error en formato SSIM Map, en la carpeta designada por el output, y arrojará un resumen promediado del **PSNR** y el **SSIM**. -->