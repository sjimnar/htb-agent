# Reglas para el Agente HTB

Este directorio contendrá las reglas y heurísticas que el agente de IA utilizará para tomar decisiones durante la resolución de máquinas CTF.

## Estructura Propuesta

- `enumeration_rules.py`: Reglas para determinar cómo proceder con la fase de enumeración según los puertos y servicios encontrados.
- `vulnerability_detection_rules.py`: Reglas para identificar posibles vulnerabilidades basadas en la información obtenida.
- `exploitation_rules.py`: Reglas para seleccionar y ejecutar exploits apropiados.
- `post_exploitation_rules.py`: Reglas para la fase post-explotación y la escalada de privilegios.

## Implementación Futura

Las reglas utilizarán los resultados de los diferentes workflows para determinar los siguientes pasos en el proceso de resolución de la máquina. Por ejemplo, si el escaneo Nmap detecta un servidor web en el puerto 80, las reglas indicarán que se debe proceder con un escaneo de directorios web con Gobuster o Dirb.
