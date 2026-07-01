import os
import glob
import argparse
from typing import Dict, Optional, List

# Importamos las herramientas de Nellie
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
    Ejecuta toda la pipeline de Nellie sobre un `FileInfo` dado.
    (Esta función no cambia, sirve igual para MIPs o Z-Stacks)
    """
    im_info = ImInfo(file_info)

    # Evitar reprocesar si ya existe salida
    try:
        out_path = im_info.pipeline_paths.get('im_skel_relabelled')
    except Exception:
        out_path = None

    if skip_existing and out_path and os.path.exists(out_path):
        print(f"⚠ Ya existe salida, se salta: {file_info.path}")
        return im_info

    print("→ Ejecutando preprocesado (Filter)...")
    preprocessing = Filter(im_info, remove_edges=remove_edges)
    preprocessing.run()

    print("→ Ejecutando segmentación (Label)...")
    segmenting = Label(im_info, otsu_thresh_intensity=otsu_thresh_intensity, threshold=threshold)
    segmenting.run()

    print("→ Ejecutando networking (Network)...")
    networking = Network(im_info)
    networking.run()

    print("→ Ejecutando mocap marking (Markers)...")
    mocap_marking = Markers(im_info)
    mocap_marking.run()

    print("→ Ejecutando tracking (HuMomentTracking)...")
    hu_tracking = HuMomentTracking(im_info)
    hu_tracking.run()

    print("→ Ejecutando reasignación de vóxeles (VoxelReassigner)...")
    vox_reassign = VoxelReassigner(im_info)
    vox_reassign.run()

    print("→ Ejecutando extracción jerárquica (Hierarchy)...")
    hierarchy = Hierarchy(im_info, skip_nodes=False)
    hierarchy.run()
    
    print("✔ Procesamiento completado para este archivo.")
    return im_info


def find_z_stack_files(root_folder: str) -> List[str]:
    """
    Busca recursivamente archivos que terminen en:
    - _Z0_stack.tif
    - _Z1_stack.tif
    - _Z2_stack.tif
    """
    # Definimos los sufijos que queremos encontrar
    sufijos = ['*_Z0_stack.tif', '*_Z1_stack.tif', '*_Z2_stack.tif']
    
    archivos_encontrados = []
    
    for sufijo in sufijos:
        # Buscamos recursivamente (**) cada patrón
        pattern = os.path.join(root_folder, '**', sufijo)
        encontrados = glob.glob(pattern, recursive=True)
        archivos_encontrados.extend(encontrados)
    
    return archivos_encontrados


def parse_dim_res(s: Optional[str]) -> Dict[str, float]:
    """Parsea una cadena como `T=1,Z=0.5,Y=0.2,X=0.2` a dict."""
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
    """Resuelve la ruta relativa al workspace o absoluta."""
    # ⚠️ RECUERDA CAMBIAR ESTO SEGÚN EL ORDENADOR DONDE ESTÉS
    workspace_root = r'D:/CIC/Videos_Mitocondrias' 
    
    if os.path.isabs(root_folder):
        return root_folder
    if os.path.exists(root_folder):
        return root_folder
    
    resolved = os.path.join(workspace_root, root_folder)
    if os.path.exists(resolved):
        return resolved
        
    return root_folder


def process_z_stack_root(root_folder: str,
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
    Procesa todos los archivos Z-Stack encontrados bajo `root_folder`.
    """
    # Resolver ruta
    root_folder = resolve_root_path(root_folder)
    
    # 1. BUSCAR LOS ARCHIVOS
    target_files = find_z_stack_files(root_folder)
    
    if not target_files:
        print(f"❌ No se encontraron archivos Z0/Z1/Z2 stack en: {root_folder}")
        return

    print(f"📂 Se encontraron {len(target_files)} archivos Z-Stack para procesar.")
    
    if dry_run:
        print("\n📋 MODO DRY-RUN: Lista de archivos a procesar:")
        for f in sorted(target_files):
            print(f"   - {os.path.basename(f)}")
        print("\nOpciones configuradas:")
        print(f"   Axes: {axes}")
        print(f"   Dim-res: {dim_res}")
        return

    # 2. PROCESAR UNO A UNO
    for idx, file_path in enumerate(sorted(target_files), 1):
        print('\n' + '=' * 80)
        print(f"[{idx}/{len(target_files)}] Iniciando: {os.path.basename(file_path)}")
        print(f"Ruta completa: {file_path}")
        print('=' * 80)

        try:
            file_info = FileInfo(file_path)
            file_info.find_metadata()
            file_info.load_metadata()

            # --- CONFIGURACIÓN DE METADATOS ---
            if axes:
                file_info.change_axes(axes)
                print(f"→ Ejes forzados a: {axes}")

            if dim_res:
                for axis, val in dim_res.items():
                    file_info.change_dim_res(axis, val)
                print(f"→ Resoluciones aplicadas: {dim_res}")

            if ch is not None:
                file_info.change_selected_channel(ch)
                print(f"→ Canal seleccionado: {ch}")

            if t_start is not None or t_end is not None:
                s = t_start if t_start is not None else 0
                e = t_end if t_end is not None else None
                if e is None:
                    file_info.select_temporal_range(s, s)
                else:
                    file_info.select_temporal_range(s, e)
                print(f"→ Rango temporal: {s} - {e}")

            # --- EJECUCIÓN ---
            run_pipeline(file_info,
                         remove_edges=remove_edges,
                         otsu_thresh_intensity=otsu_thresh_intensity,
                         threshold=threshold,
                         skip_existing=skip_existing)
                         
        except Exception as exc:
            print(f"❌ ERROR CRÍTICO procesando {os.path.basename(file_path)}: {exc}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Procesar Z-Stacks (Z0, Z1, Z2) con Nellie')
    parser.add_argument('--root', default=r'Project001', help='Carpeta raíz donde buscar')
    
    # Opciones
    parser.add_argument('--axes', default='TYX', help="Ejes, p.ej. 'TYX' o 'TZYX'")
    parser.add_argument('--dim-res', default='T=1,Y=0.05,X=0.05', help="Resoluciones (ej: 'T=1,Y=0.05,X=0.05')")
    parser.add_argument('--ch', type=int, default=None, help='Canal')
    parser.add_argument('--t-start', type=int, default=None, help='Frame inicial')
    parser.add_argument('--t-end', type=int, default=None, help='Frame final')
    
    # Flags de procesado
    parser.add_argument('--remove-edges', action='store_true', help='Eliminar bordes')
    parser.add_argument('--otsu', action='store_true', help='Usar Otsu')
    parser.add_argument('--threshold', type=float, default=None, help='Umbral manual')
    parser.add_argument('--no-skip', dest='skip', action='store_false', help='Forzar reprocesado')
    parser.add_argument('--dry-run', action='store_true', help='Solo listar archivos')

    args = parser.parse_args()
    dim_res_dict = parse_dim_res(args.dim_res)

    process_z_stack_root(args.root,
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