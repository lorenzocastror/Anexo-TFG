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

Extracción de datos\Tracking Mitocondrial con Trackastra

---

### 5. Unificación de las bases de datos de todos los vídeos
Este script automatiza la búsqueda, extracción y consolidación de los datos tabulares contenidos en los múltiples archivos Excel generados a lo largo del proyecto. Recorre de forma recursiva la estructura de directorios aplicando filtros de exclusión precisos para descartar archivos temporales, copias de seguridad y carpetas de versiones anteriores. A partir de los archivos validados, extrae las hojas específicas de trayectorias de interés y datos celulares, asignando a cada registro el identificador de su vídeo correspondiente. Tras concatenar toda la información, el módulo ejecuta un control de calidad sistemático para eliminar posibles filas duplicadas y exporta una única matriz maestra en formato Excel que centraliza la totalidad de las observaciones poblacionales listas para el análisis estadístico global.

Extracción de datos\Unificación Resultados

---

### 6. Obtención de la base de datos con las Métricas Iniciales
Este script automatiza el cálculo y la extracción detallada de métricas cinemáticas y espaciales a partir de los datos de seguimiento mitocondrial previamente unificados. Para cada trayectoria, el algoritmo cuantifica parámetros físicos como la velocidad, el desplazamiento neto, el índice de direccionalidad y el área media, integrando simultáneamente las coordenadas del centroide celular para evaluar la dinámica radial y el radial bias de los orgánulos. Adicionalmente, computa el Desplazamiento Cuadrático Medio poblacional (MSD) para caracterizar de forma global el comportamiento difusivo o de transporte activo de la muestra. El procesamiento incluye un riguroso control de calidad estructural para purgar posibles registros temporales duplicados y exporta todas las variables generadas a un nuevo archivo Excel estructurado en diferentes hojas de datos correspondientes a las métricas individuales por trayectoria y las curvas MSD, optimizado para su posterior evaluación estadística.

Extracción de datos\Obtención Métricas

---

### 7. Obtención de la base de datos con las Métricas Iniciales para las mitocondrias con trayectorias >10 frames
Este script automatiza el cálculo y la extracción detallada de métricas cinemáticas y espaciales a partir de los datos de seguimiento mitocondrial previamente unificados para mitocondrias que tienen trayectorias >10 frames. Para cada trayectoria, el algoritmo cuantifica parámetros físicos como la velocidad, el desplazamiento neto, el índice de direccionalidad y el área media, integrando simultáneamente las coordenadas del centroide celular para evaluar la dinámica radial y el radial bias de los orgánulos. Adicionalmente, computa el Desplazamiento Cuadrático Medio poblacional (MSD) para caracterizar de forma global el comportamiento difusivo o de transporte activo de la muestra. El procesamiento incluye un riguroso control de calidad estructural para purgar posibles registros temporales duplicados y exporta todas las variables generadas a un nuevo archivo Excel estructurado en diferentes hojas de datos correspondientes a las métricas individuales por trayectoria y las curvas MSD, optimizado para su posterior evaluación estadística.

Extracción de datos\Obtención Métricas >10 frames

---

### 8. Generación de Secuencias Visuales para la memoria
Este script genera una figura representativa de la dinámica mitocondrial a partir de secuencias de microscopía y los resultados del seguimiento obtenido con Trackastra. Para varios instantes temporales seleccionados, superpone la imagen de fluorescencia original, las máscaras de las mitocondrias segmentadas y las trayectorias acumuladas de los orgánulos, restringiendo el análisis a las mitocondrias contenidas dentro de la célula mediante una máscara celular. Finalmente, crea un panel comparativo con barra de escala y anotaciones temporales, listo para su utilización en publicaciones o presentaciones científicas.

Visualización de datos\Secuencia de Trayectorias para la memoria

---

### 9. Generación de los Boxplots de las Métricas Iniciales
Este script automatiza la generación y exportación de gráficos estadísticos descriptivos mediante boxplots para la evaluación visual de las variables morfológicas y dinámicass de las poblaciones mitocondriales. 

Visualización de datos\Boxplots Descriptivos

---

### 10. Generación de Superplots
Este script genera automáticamente SuperPlots para las principales variables del análisis mitocondrial, produciendo tanto comparaciones globales entre condiciones experimentales como análisis independientes de la estabilidad de los grupos control. Para cada variable se generan dos figuras: una comparando el grupo control con los grupos silenciados y otra evaluando exclusivamente la variabilidad entre los distintos controles temporales.


Visualización de datos\Superplots

---

### 11. Generación de los Gráficos del MSD
Este script genera figuras científicas de las curvas de Desplazamiento Cuadrático Medio (MSD, Mean Squared Displacement) para evaluar la dinámica mitocondrial en los distintos grupos experimentales. A partir de las curvas promedio obtenidas para cada condición, calcula el exponente de difusión (α) mediante una regresión lineal en escala logarítmica sobre los primeros retardos temporales, permitiendo caracterizar el tipo de movimiento de las mitocondrias. Además, estima una aproximación del ruido de localización a partir del intercepto de la regresión y exporta estos valores a un archivo Excel. El script genera tanto gráficos individuales para cada grupo experimental como una figura comparativa con todas las curvas MSD, utilizando un formato optimizado para publicaciones científicas mediante Matplotlib.

Visualización de datos\Gráficos MSD

---

### 12. Generación de los Histogramas de Desplazamientos mitocondriales
Este script cuantifica los desplazamientos instantáneos (steps) de las trayectorias mitocondriales obtenidas durante el seguimiento temporal y genera un análisis estadístico completo de su distribución. Para cada trayectoria se calcula la distancia recorrida entre fotogramas consecutivos, construyendo posteriormente histogramas individuales, por vídeo y por grupo experimental. Además, se genera una matriz resumen en un Excel que recoge la frecuencia de desplazamientos en intervalos espaciales definidos.

Histogramas Desplazamiento Mitocondrial

---

### 13. Obtención de la base de datos del Ratio de Movimiento
Este script calcula ratio de movilidad mitocondrial a partir de las distribuciones de desplazamiento previamente obtenidas. El procedimiento clasifica los desplazamientos registrados en dos categorías (estáticos y móviles) utilizando un umbral espacial definido (0.2 micras) y calcula, para cada vídeo, el cociente entre ambas fracciones.

Extracción de datos\Obtención Ratios de movimiento

---

### 14. Obtención de la base de datos de la Distancia al Centro
Este script calcula la distancia media de cada mitocondria al centro de masa celular a lo largo de su trayectoria, utilizando simultáneamente la información de las trayectorias mitocondriales y de la segmentación celular. Además de la distancia absoluta (µm), el algoritmo calcula una distancia normalizada respecto al tamaño celular, permitiendo comparar células de diferentes dimensiones mediante una métrica adimensional. El resultado es una tabla donde cada fila representa una mitocondria, incluyendo su distancia media al centro celular y la clasificación experimental correspondiente.

Extracción de datos\Obtención Distancia al Centro

---
