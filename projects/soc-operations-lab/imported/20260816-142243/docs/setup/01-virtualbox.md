# 01 — VirtualBox

## Componentes

El laboratorio utiliza tres máquinas virtuales: Kali Linux, Ubuntu con Wazuh Manager y un endpoint Windows 11. VirtualBox proporciona tres adaptadores lógicos por rol cuando aplica: MANAGEMENT, ATTACK/LAB y NAT/INTERNET.

## Criterio reproducible

1. Crear las tres VMs.
2. Asignar los adaptadores a las tres redes documentadas en [networking](06-networking.md).
3. Confirmar direcciones IP antes de probar detecciones.
4. Ejecutar escenarios solo desde ATTACK/LAB contra activos del laboratorio.

La exportación de máquinas, sus tamaños, versiones exactas de ISO y snapshots no forma parte todavía del material público. Deben registrarse en una futura reconstrucción limpia antes de declararse un procedimiento paso a paso completo.
