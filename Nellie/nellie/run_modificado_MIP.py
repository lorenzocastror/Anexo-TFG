import os
import glob
import argparse
from typing import Dict, Optional

from nellie.feature_extraction.hierarchical import Hierarchy
from nellie.im_info.verifier import FileInfo, ImInfo
from nellie.segmentation.filtering import Filter
from nellie.segmentation.labelling import Label
from nellie.segmentation.mocap_marking import Markers
from nellie.segmentation.networking import Network
from nellie.tracking.hu_tracking import HuMomentTracking
from nellie.tracking.voxel_reassignment import VoxelReassigner


def run_pipeline(file_info: FileInfo,
                 remove_edges: bool = False,
                 otsu_thresh_intensity: bool = False,
                 threshold: Optional[float] = None,
                 skip_existing: bool = True):
    """
    Lanza el pipeline completo de Nellie en el orden correcto.
    
    Se mantiene 'skip_existing' por defecto para evitar la pérdida de tiempo 
    reprocesando datos en caso de interrupción (el script comprueba 
    automáticamente si existe el archivo 'im_skel_relabelled').
    """
    im_info = ImInfo(file_info)

    # Comprobación rápida para verificar si el output ya fue generado previamente
    try:
        out_path = im_info.pipeline_paths.get('im_skel_relabelled')
    except Exception:
        out_path = None

    if skip_existing and out_path and os.path.exists(out_path):
        print(f"⚠ Ya existe salida ({out_path}), se salta: {file_info.path}")
        return im_info

    print("→ Ejecutando preprocesado (Filter)...")
    preprocessing = Filter(im_info, remove_edges=remove_edges)
    preprocessing.run()
    print("✔ Preprocesado completado")

    print("→ Ejecutando segmentación (Label)...")
    segmenting = Label(im_info, otsu_thresh_intensity=otsu_thresh_intensity, threshold=threshold)
    segmenting.run()
    print("✔ Segmentación completada")

    print("→ Ejecutando networking (Network)...")
    networking = Network(im_info)
    networking.run()
    print("✔ Networking completado")

    print("→ Ejecutando mocap marking (Markers)...")
    mocap_marking = Markers(im_info)
    mocap_marking.run()
    print("✔ Mocap marking completado")

    print("→ Ejecutando tracking (HuMomentTracking)...")
    hu_tracking = HuMomentTracking(im_info)
    hu_tracking.run()
    print("✔ Tracking completado")

    print("→ Ejecutando reasignación de vóxeles (VoxelReassigner)...")
    vox_reassign = VoxelReassigner(im_info)
    vox_reassign.run()
    print("✔ Voxel reassignment completado")

    print("→ Ejecutando extracción jerárquica (Hierarchy)...")
    hierarchy = Hierarchy(im_info, skip_nodes=False)
    hierarchy.run()
    print("✔ Hierarchy completado")

    return im_info


def find_mip_files(root_folder: str):
    """
    Extrae todos los archivos *_MIP.tif de la carpeta y subcarpetas.
    La búsqueda recursiva con glob previene fallos en la ruta en caso de que 
    la macro de ImageJ ("Video fusion MIP") modifique la estructura de directorios.
    """
    pattern = os.path.join(root_folder, '**', '*_MIP.tif')
    return glob.glob(pattern, recursive=True)


def parse_dim_res(s: Optional[str]) -> Dict[str, float]:
    """
    Convierte la cadena de texto introducida por consola (tipo T=1,Y=0.05...) 
    en un diccionario estándar interpretable por el script.
    """
    if not s:
        return {}
    out: Dict[str, float] = {}
    parts = [p.strip() for p in s.split(',') if p.strip()]
    for p in parts:
        if '=' in p:
            k, v = p.split('=', 1)
            try:
                out[k.strip()] = float(v)
            except ValueError:
                print(f"⚠ No se pudo parsear valor para {k}: {v}")
    return out


def resolve_root_path(root_folder: str) -> str:
    """
    Función auxiliar para la resolución de rutas. 
    Si recibe un nombre de carpeta aislado (ej. 'Project001'), asume su 
    ubicación dentro del workspace del disco D. Si recibe una ruta absoluta 
    de Windows, la mantiene intacta.
    """
    workspace_root = r'D:/CIC/Videos_Mitocondrias'
    
    if os.path.isabs(root_folder):
        return root_folder
    
    if os.path.exists(root_folder):
        return root_folder
        
    resolved = os.path.join(workspace_root, root_folder)
    if os.path.exists(resolved):
        return resolved
        
    return root_folder


def process_mip_root(root_folder: str,
                     remove_edges: bool = False,
                     otsu_thresh_intensity: bool = False,
                     threshold: Optional[float] = None,
                     axes: Optional[str] = None,
                     dim_res: Optional[Dict[str, float]] = None,
                     ch: Optional[int] = None,
                     t_start: Optional[int] = None,
                     t_end: Optional[int] = None,
                     skip_existing: bool = True,
                     dry_run: bool = False):
    """
    Bucle principal que localiza los MIPs y aplica las configuraciones antes 
    de ejecutar Nellie. Incorpora un modo dry_run para listar las operaciones 
    pendientes sin consumir recursos de procesamiento.
    """
    # Ajuste previo de la ruta
    root_folder = resolve_root_path(root_folder)
    
    mip_files = find_mip_files(root_folder)
    if not mip_files:
        print(f"No se encontraron archivos MIP en: {root_folder}")
        return

    print(f"Se encontraron {len(mip_files)} archivos MIP.")
    if dry_run:
        print("\n📋 MODO DRY-RUN: Se listan los archivos y opciones sin ejecutar la pipeline.\n")
    else:
        print("Procesando...")
        
    for idx, mip_path in enumerate(sorted(mip_files), 1):
        print('\n' + '=' * 64)
        print(f"[{idx}/{len(mip_files)}] Procesando: {mip_path}")
        print('=' * 64)

        file_info = FileInfo(mip_path)
        file_info.find_metadata()
        file_info.load_metadata()

        # Sobrescritura de metadatos si se han proporcionado argumentos por consola
        if axes:
            try:
                file_info.change_axes(axes)
                print(f"→ Ejes cambiados a: {axes}")
            except Exception as e:
                print(f"⚠ No se pudo cambiar ejes: {e}")

        if dim_res:
            for axis, val in dim_res.items():
                try:
                    file_info.change_dim_res(axis, val)
                    print(f"→ Resolución {axis} establecida en {val}")
                except Exception as e:
                    print(f"⚠ No se pudo cambiar resolución {axis}: {e}")

        if ch is not None:
            try:
                file_info.change_selected_channel(ch)
                print(f"→ Canal seleccionado: {ch}")
            except Exception as e:
                print(f"⚠ No se pudo seleccionar canal {ch}: {e}")

        if t_start is not None or t_end is not None:
            try:
                # Control de seguridad ante la posible ausencia de un límite temporal
                s = t_start if t_start is not None else 0
                e = t_end if t_end is not None else None
                if e is None:
                    file_info.select_temporal_range(s, s)
                else:
                    file_info.select_temporal_range(s, e)
                print(f"→ Rango temporal seleccionado: {t_start} - {t_end}")
            except Exception as ex:
                print(f"⚠ No se pudo seleccionar rango temporal: {ex}")

        # Finalización temprana si el modo dry-run está activo
        if dry_run:
            print(f"  Axes: {axes if axes else '(no especificado)'}")
            print(f"  Dim-res: {dim_res if dim_res else '(no especificado)'}")
            print(f"  Canal: {ch if ch is not None else '(no especificado)'}")
            print(f"  T-range: {t_start}-{t_end if t_end is not None else '(no especificado)'}")
            continue

        # Ejecución principal
        try:
            run_pipeline(file_info,
                         remove_edges=remove_edges,
                         otsu_thresh_intensity=otsu_thresh_intensity,
                         threshold=threshold,
                         skip_existing=skip_existing)
        except Exception as exc:
            print(f"❌ Error procesando {mip_path}: {exc}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Procesar TIFF MIP con la pipeline Nellie')
    parser.add_argument('--root', default=r'Project001', help='Carpeta raíz donde buscar MIP')
    parser.add_argument('--axes', default='TYX', help="Cambiar orden de ejes, p.ej. 'TZYX' (por defecto 'TYX')")
    parser.add_argument('--dim-res', default='T=1,Y=0.05,X=0.05', help="Resoluciones como 'T=1,Z=0.5,Y=0.2,X=0.2' (por defecto 'T=1,Y=0.05,X=0.05')")
    parser.add_argument('--ch', type=int, default=None, help='Canal a seleccionar (si aplica)')
    parser.add_argument('--t-start', type=int, default=None, help='Inicio temporal (int)')
    parser.add_argument('--t-end', type=int, default=None, help='Fin temporal (int)')
    parser.add_argument('--remove-edges', action='store_true', help='Activar removal de bordes en preprocesado')
    parser.add_argument('--otsu', action='store_true', help='Usar Otsu para threshold de intensidad')
    parser.add_argument('--threshold', type=float, default=None, help='Umbral fijo de intensidad')
    parser.add_argument('--no-skip', dest='skip', action='store_false', help='No saltar ficheros ya procesados')
    parser.add_argument('--dry-run', action='store_true', help='Solo listar archivos MIP y opciones sin ejecutar la pipeline')

    args = parser.parse_args()

    dim_res_dict = parse_dim_res(args.dim_res)

    # Ejemplo de ejecución desde terminal:
    # python run_modificado.py --root Project001 --axes TZYX --dim-res T=1,Z=0.5,Y=0.2,X=0.2 --ch 0 --remove-edges --otsu
    
    # Prueba de ejecución en modo seguro (dry-run):
    # python run_modificado.py --root Project001 --dry-run
    process_mip_root(args.root,
                     remove_edges=args.remove_edges,
                     otsu_thresh_intensity=args.otsu,
                     threshold=args.threshold,
                     axes=args.axes,
                     dim_res=dim_res_dict,
                     ch=args.ch,
                     t_start=args.t_start,
                     t_end=args.t_end,
                     skip_existing=args.skip,
                     dry_run=args.dry_run)