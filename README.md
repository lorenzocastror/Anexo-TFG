# Pipeline Automatizado para el Análisis de la Morfología y Dinámica Mitocondrial
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-ee4c2c.svg)
![Napari](https://img.shields.io/badge/Napari-Bioimaging-green.svg)
![Nellie](https://img.shields.io/badge/Nellie-Mithocondrial%20Segmentation-8a2be2.svg)
![Trackastra](https://img.shields.io/badge/Trackastra-Tracking-ff8c00.svg)
## Introducción
El presente repositorio contiene el conjunto de herramientas computacionales, scripts de procesamiento de imágenes y algoritmos de análisis estadístico desarrollados para la realización del TFG titulado **Modelos Lineales Mixtos para el Análisis de la Dinámica Mitocondrial en Cáncer**. 

---

```mermaid
graph LR
    %% Nodos de la secuencia
    A([Microscopía confocal]) --> B[Segmentación con Nellie]
    B --> C[Fusión lógica de máscaras]
    C --> D[Tracking con Trackastra + Unión de trayectorias]
    D --> E[(Extracción de métricas)]
    E --> F[Visualización]
    F --> G{{Modelos Lineales Mixtos GLMM}}

    %% Estilos de color para jerarquizar visualmente el flujo
    style A fill:#2c3e50,stroke:#fff,stroke-width:2px,color:#fff
    style B fill:#8a2be2,stroke:#fff,stroke-width:2px,color:#fff
    style D fill:#ff8c00,stroke:#fff,stroke-width:2px,color:#fff
    style F fill:#27ae60,stroke:#fff,stroke-width:2px,color:#fff
    style G fill:#c0392b,stroke:#fff,stroke-width:2px,color:#fff
```
---

## Índice del pipeline

1. Configuración del entorno
2. Segmentación mitocondrial (Nellie)
3. Unión lógica de máscaras
4. Tracking mitocondrial (Trackastra)
5. Unificación de resultados
6. Obtención de métricas
7. Obtención de métricas (>10 frames)
8. Generación de figuras para la memoria
9. Boxplots descriptivos
10. SuperPlots
11. Curvas MSD
12. Histogramas de desplazamientos
13. Ratio de movimiento
14. Distancia al centro celular
15. Análisis Estadístico
Flujo de datos
Requisitos y estructura
Software utilizado 

---

## Pipeline
### 1. Configuración del Entorno Virtual (Environment)
Para garantizar la ejecución del pipeline se requiere la preparación de un entorno. La instalación de los paquetes necesarios se realiza mediante `pip` ejecutando el siguiente comando:

```bash
pip install numpy pandas scipy matplotlib seaborn tifffile scikit-image opencv-python openpyxl tqdm napari torch trackastra nellie
```

---

### 2. Segmentación Mitocondrial
Este script automatiza la ejecución de la pipeline de Nellie sobre las secuencias temporales obtenidas mediante el microscopio confocal de fluorescencia correspondientes a los planos focales individuales (Z0, Z1 y Z2). Localiza de forma recursiva los archivos y ejecuta las etapas de preprocesado, segmentación, reconstrucción de la red mitocondrial, tracking, reasignación de vóxeles y extracción jerárquica de características correspondientes a Nellie. 

`Nellie\nellie\Segmentación Mitocondrial Nellie.py`

---

### 3. Unión Lógica de las Máscaras Mitocondriales
Este script consolida la fusión y el procesamiento de las máscaras mitocondriales generadas por Nellie en tres planos focales (Z0, Z1 y Z2). Para cada fotograma, combina las segmentaciones de los tres planos, identifica componentes conectados y aplica un algoritmo de unión morfológica que fusiona estructuras mitocondriales próximas, preservando los objetos principales y eliminando pequeñas detecciones aisladas consideradas ruido. El procesamiento genera una secuencia TIFF etiquetada (2D + tiempo) para cada vídeo.

`Extracción de datos\Unión Lógica de Máscaras`

---

### 4. Tracking Mitocondrial mediante Trackastra + Unión de Trayectorias
Este script realiza el tracking de las máscaras mitocondriales fusionadas previamente. Para cada secuencia, aplica el modelo de aprendizaje profundo Trackastra para enlazar los orgánulos a lo largo del tiempo, calcula sus propiedades morfológicas y dinámicas en cada fotograma, y ejecuta un algoritmo de fusión de trayectorias que las reconecta basándose en la distancia espacial y la persistencia temporal. Este genera para cada secuencia un archivo Excel, una secuencia TIFF etiquetada con los identificadores y un script para la visualización de los resultados en Napari.

`Extracción de datos\Tracking Mitocondrial con Trackastra`

---

### 5. Unificación de las bases de datos de todos los vídeos
Este script consolida automáticamente las tablas generadas para cada vídeo en una única base de datos maestra, incorpora los identificadores experimentales y realiza controles básicos de calidad antes de exportar la matriz final para el análisis estadístico.

`Extracción de datos\Unificación Resultados`

---

### 6. Obtención de la base de datos con las Métricas Iniciales
Este script efectúa la extracción detallada de las métricas dinámicas y espaciales a partir de los datos de seguimiento mitocondrial previamente unificados. Para cada trayectoria, el algoritmo cuantifica parámetros físicos como la velocidad, el desplazamiento neto, el índice de direccionalidad y el área media, integrando simultáneamente las coordenadas del centroide celular para evaluar la dinámica radial y el radial bias de los orgánulos. Adicionalmente, calcula el Desplazamiento Cuadrático Medio poblacional (MSD). El código xporta todas las variables generadas a un nuevo archivo Excel estructurado en diferentes hojas de datos correspondientes a las métricas individuales por trayectoria y las curvas MSD.

`Extracción de datos\Obtención Métricas`

---

### 7. Obtención de la base de datos con las Métricas Iniciales para las mitocondrias con trayectorias >10 frames
Este script constituye una variante del cálculo de métricas descrito anteriormente, restringiendo el análisis exclusivamente a trayectorias con una duración superior a 10 fotogramas.

`Extracción de datos\Obtención Métricas más de 10 frames`

---

### 8. Generación de Secuencias Visuales para la memoria
Este script genera una figura representativa de la dinámica mitocondrial a partir de secuencias de microscopía y los resultados del seguimiento obtenido con Trackastra. Para varios instantes temporales seleccionados, superpone la imagen de fluorescencia original, las máscaras de las mitocondrias segmentadas y las trayectorias acumuladas de los orgánulos, restringiendo el análisis a las mitocondrias contenidas dentro de la célula mediante la máscara celular.

`Visualización de datos\Secuencia de Trayectorias para la memoria`

---

### 9. Generación de los Boxplots de las Métricas Iniciales
Este script automatiza la generación y exportación de gráficos estadísticos descriptivos mediante boxplots para la evaluación visual de las variables morfológicas y dinámicas mitocondriales. 

`Visualización de datos\Boxplots Descriptivos`

---

### 10. Generación de los Gráficos del MSD
Este script genera figuras de las curvas de Desplazamiento Cuadrático Medio (MSD, Mean Squared Displacement) para evaluar la dinámica mitocondrial en los distintos grupos experimentales. A partir de las curvas promedio obtenidas para cada condición, calcula el exponente de difusión (α) mediante una regresión lineal en escala logarítmica sobre los primeros retardos temporales. Además, estima una aproximación del ruido de localización a partir del intercepto de la regresión y exporta estos valores a un archivo Excel. El script genera tanto gráficos individuales para cada grupo experimental como una figura comparativa con todas las curvas MSD.

`Visualización de datos\Gráficos MSD`

---

### 11. Generación de los Histogramas de Desplazamientos mitocondriales
Este script cuantifica los desplazamientos instantáneos de las trayectorias mitocondriales obtenidas durante el seguimiento temporal. Para cada trayectoria se calcula la distancia recorrida entre fotogramas consecutivos, construyendo posteriormente histogramas individuales, por vídeo y por grupo experimental. Además, se genera un Excel que recoge la frecuencia de desplazamientos en intervalos espaciales definidos.

`Visualización de datos\Histogramas Desplazamiento Mitocondrial`

---

### 12. Obtención de la base de datos del Ratio de Movimiento
Este script calcula el ratio de movimiento mitocondrial para cada vídeo a partir de las distribuciones de desplazamiento previamente obtenidas, utilizando un umbral espacial definido (0.2 micras).

`Extracción de datos\Obtención Ratios de movimiento`

---

### 13. Obtención de la base de datos de la Distancia al Centro
Este script exporta un Excel con la distancia media de cada mitocondria al centro de masa celular a lo largo de su trayectoria, utilizando simultáneamente la información de las trayectorias mitocondriales y de la segmentación celular. Además de la distancia absoluta (µm), el algoritmo calcula una distancia normalizada respecto al tamaño celular.

`Extracción de datos\Obtención Distancia al Centro`

---

### 14. Generación de Superplots
Este script genera automáticamente SuperPlots para las principales variables del análisis mitocondrial, produciendo tanto comparaciones globales entre condiciones experimentales como análisis independientes de los grupos control. Para cada variable se generan dos figuras: una comparando el grupo control global con los grupos silenciados y otra evaluando exclusivamente la variabilidad entre los distintos controles temporales.


`Visualización de datos\Superplots`

---

### 15. Análisis Estadístico
Finalmente, se realizó un análisis estadístico de los datos obtenidos anteriormente en este Pipeline mediante SPSS.\    

---

### Flujo de Datos
| Etapa del Pipeline | Archivo de Entrada | Archivo de Salida | Descripción |
| :--- | :--- | :--- | :--- |
| **1. Microscopía Confocal** | N/A | `.tif` | Vídeos RAW originales extraídos del microscopio (planos focales Z0, Z1, Z2). |
| **2. Segmentación (Nellie)** | `.tif` (RAW) | Máscaras `.tif` | Segmentación y reconstrucción de la red mitocondrial independiente por plano focal. |
| **3. Unión Lógica de Máscaras** | Máscaras `.tif` (Z0, Z1, Z2) | `.tif` (Máscara 2D+t) | Fusión morfológica de los planos focales, conexión de componentes y filtrado de ruido. |
| **4. Tracking (Trackastra)** | `.tif` (Máscara unificada) | Múltiples `.xlsx`, `.tif`, script `.py` | Trayectorias de las mitocondrias, reconexión espacial/temporal y visualización para Napari. |
| **5. Unificación de BDs** | Múltiples `.xlsx` (Tracking) | `Master_Analisis.xlsx` | Base de datos con los identificadores experimentales de todos los vídeos. |
| **6. Métricas Iniciales** | `Master_Analisis.xlsx` | `Metricas_Detalladas.xlsx` | Extracción de variables cinemáticas, dinámica radial y curvas base del Desplazamiento Cuadrático Medio (MSD). |
| **7. Métricas >10 frames** | `Master_Analisis.xlsx` | Excel de Métricas (>10 frames) | Filtrado para evaluar exclusivamente las trayectorias mitocondriales estables en >10 frames. |
| **8. Secuencias Visuales** | RAW `.tif`, Máscaras `.tif`, Trayectorias `.xlsx` | Imágenes `.png` | Imágenes representativas de las trayectorias. |
| **9. Boxplots Descriptivos** | `Metricas_Detalladas.xlsx` | Gráficos `.png`| Diagramas de caja para las variables morfológicas y cinemáticas. |
| **10. Gráficos MSD** | `Metricas_Detalladas.xlsx` | Gráficos `.png`, Data `.xlsx` | Curvas de difusión, exponente α y extracción del intercepto (ruido de localización). |
| **11. Histogramas** | `Master_Analisis.xlsx` | Gráficos `.png`, Frecuencias `.xlsx` | Densidades de probabilidad de los desplazamientos entre fotogramas. |
| **12. Ratio de Movimiento** | `.xlsx` (Frecuencias/Desplazamientos)| Ratio de Movimiento `.xlsx` | Base de datos con los ratios de movimiento por mitocondria. |
| **13. Distancia al Centro** | Trayectorias `.xlsx`, Segmentación celular | Distancia al Centro `.xlsx` | Cálculo matricial de distancias absolutas (µm) y normalizadas al centro de masa celular. |
| **14. SuperPlots** | `Metricas_Detalladas.xlsx`, Distancia al Centro `.xlsx`, Ratio de Movimiento `.xlsx` | Gráficos `.png`| Superplots para comparaciones globales inter-grupo y entre los controles. |
| **15. Inferencia (SPSS)** | Matrices `.xlsx` finales | Contrastes de Hipótesis | Análisis estadístico inferencial |

---

### Requisitos y Estructura

- Python 3.11
- CUDA (opcional para Trackastra)
- Sistema operativo Windows (rutas configuradas para Windows)

Para la correcta ejecución del pipeline, el directorio de trabajo debe mantener la siguiente arquitectura de archivos:

```text
Videos_Mitocondrias/
├── Project001/                               # Vídeos originales en formato TIFF (RAW)
├── Project001 Máscaras 3 Capas lng_adaptive/ # Salidas iniciales de segmentación de Nellie
├── Resultados Analisis_TFG/                  # Matrices consolidadas y salidas finales
│   ├── Boxplots_Individuales/
│   ├── Histogramas desplazamientos Control/
│   └── SuperPlots/
└── Python/                                   # Scripts de procesamiento (.py)
```
⚠️ Los módulos de preprocesamiento e integración automática contienen variables ruta asociadas al entorno de almacenamiento local del autor. Antes de ejecutar el pipeline en una nueva estación de trabajo, verifique las rutas declaradas en las cabeceras de configuración de cada script.

---

## Software utilizado

Este pipeline hace uso de herramientas desarrolladas por terceros:

- **Nellie** (Austin E. Y. T. Lefebvre), utilizado para la segmentación y extracción inicial de las características mitocondriales.
  Licencia: CC BY 4.0.
  https://github.com/aelefebv/nellie

- **Trackastra**, utilizado para el seguimiento de trayectorias mitocondriales.
  https://github.com/weigertlab/trackastra

---  
