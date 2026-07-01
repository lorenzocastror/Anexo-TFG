# Pipeline Automatizado para el Análisis de la Morfología y Dinámica Mitocondrial

## Introducción
El presente repositorio contiene el conjunto de herramientas computacionales, scripts de procesamiento de imágenes y algoritmos de análisis estadístico desarrollados para la realización del TFG titulado MODELOS LINEALES MIXTOS PARA EL ANÁLISIS DE LA DINÁMICA MITOCONDRIAL EN CÁNCER. 

---

## Estructura del Pipeline y Documentación del Código

### 1. Configuración del Entorno Virtual (Environment)
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

```bash
pip install os glob argparse typing tifffile openpyxl cv2 warnings nellie torch trackastra napari openpyxl numpy pandas scikit-image scipy tqdm matplotlib opencv seaborn
```

---

### 2. Segmentación Mitocondrial
Este script automatiza la ejecución de la pipeline de Nellie sobre secuencias temporales correspondientes a planos focales individuales (Z0, Z1 y Z2). Localiza de forma recursiva los archivos TIFF, configura automáticamente los metadatos necesarios (ejes, resolución espacial y temporal, canal y rango temporal) y ejecuta las etapas de preprocesado, segmentación, reconstrucción de la red mitocondrial, tracking, reasignación de vóxeles y extracción jerárquica de características. Además, permite procesar grandes conjuntos de datos de forma masiva, evitar el reprocesamiento de archivos ya analizados y comprobar previamente los archivos a procesar mediante un modo dry-run.

Nellie\nellie\Segmentación Mitocondrial 

---

### 3. Unión Lógica de las Máscaras Mitocondriales
Este script automatiza la fusión y el procesamiento de las máscaras mitocondriales generadas por Nellie en tres planos focales (Z0, Z1 y Z2). Para cada fotograma, combina las segmentaciones de los tres planos, identifica componentes conectados y aplica un algoritmo de clustering morfológico que fusiona estructuras mitocondriales próximas, preservando los objetos principales y eliminando pequeñas detecciones aisladas consideradas ruido. El procesamiento se realiza de forma masiva sobre todos los vídeos del proyecto, generando una secuencia TIFF etiquetada (2D + tiempo) para cada vídeo.
Extracción de datos\Unión Lógica de Máscaras

---

### 4. Tracking Mitocondrial mediante Trackastra + Unión de Trayectorias
Este script automatiza el seguimiento espaciotemporal y la extracción de métricas de las máscaras mitocondriales fusionadas previamente. Para cada secuencia, aplica el modelo de aprendizaje profundo Trackastra para enlazar los orgánulos a lo largo del tiempo, calcula sus propiedades morfológicas y dinámicas en cada fotograma, y ejecuta un algoritmo de fusión de trayectorias que reconecta fragmentos fragmentados basándose en la distancia espacial y la persistencia temporal. El procesamiento se realiza de forma masiva sobre todos los vídeos del proyecto, generando para cada uno de ellos un archivo de datos tabulares en Excel, una secuencia TIFF etiquetada con los identificadores unificados y un script autoejecutable para la visualización inmediata de los resultados en Napari.

---

### 5. Unificación de las bases de datos de todos los vídeos
Este script automatiza la búsqueda, extracción y consolidación de los datos tabulares contenidos en los múltiples archivos Excel generados a lo largo del proyecto. Recorre de forma recursiva la estructura de directorios aplicando filtros de exclusión precisos para descartar archivos temporales, copias de seguridad y carpetas de versiones anteriores. A partir de los archivos validados, extrae las hojas específicas de trayectorias de interés y datos celulares, asignando a cada registro el identificador de su vídeo correspondiente. Tras concatenar toda la información, el módulo ejecuta un control de calidad sistemático para eliminar posibles filas duplicadas y exporta una única matriz maestra en formato Excel que centraliza la totalidad de las observaciones poblacionales listas para el análisis estadístico global.

---

### 6. Obtención de la base de datos con las Métricas Iniciales
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno virtualizado. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

---

### 7. Obtención de la base de datos con las Métricas Iniciales para las mitocondrias con trayectorias <10 frames
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno virtualizado. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

---

### 8. Generación de Secuencias Visuales para la memoria
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno virtualizado. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

---

### 9. Generación de los Boxplots de las Métricas Iniciales
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno virtualizado. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

---

### 10. Generación de Superplots para los grupos Control
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno virtualizado. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

---

### 11. Generación de los Histogramas de Desplazamientos mitocondriales
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno virtualizado. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

---

### 12. Obtención de la base de datos del Ratio de Movimiento
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno virtualizado. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

---

### 13. Obtención de la base de datos de la Distancia al Centro
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno virtualizado. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

---

### 14. Generación de Superplots
Para garantizar la reproducibilidad del pipeline y la correcta ejecución de todas las dependencias matemáticas, de visión computacional y aprendizaje profundo, se requiere la preparación de un entorno virtualizado. La instalación de los paquetes necesarios se realiza mediante el gestor de paquetes `pip` ejecutando el siguiente comando:

---
