# Workflows del Agente HTB

Este directorio contiene los workflows que el agente utiliza para interactuar con las herramientas de Kali a través del servidor MCP.

## Estructura de un Workflow

Cada workflow es un módulo Python que define una función principal para interactuar con una herramienta específica de Kali. Deben seguir la siguiente estructura:

```python
import sys
import os

# Añadir el directorio padre al path para poder importar de mcp_configs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp_configs.kali_mcp_config import KALI_MCP_SERVER_NAME
from tools import use_mcp_tool  # Esta importación la proporciona cline.bot

def perform_tool_action(param1, param2, mcp_server_name, ...):
    """
    Documentación de la función con descripción, parámetros y valores de retorno.
    """
    try:
        result = use_mcp_tool(
            server_name=mcp_server_name,
            tool_name="herramienta_kali",
            arguments={
                "param1": param1,
                "param2": param2,
                # Otros parámetros según requiera la herramienta
            }
        )
        return result
    except Exception as e:
        print(f"Error en el workflow: {e}")
        return {"status": "error", "message": str(e)}
```

## Workflows Implementados

- `connect_vpn.py`: Workflow para conectar la máquina Kali a la VPN de HTB.
- `nmap_scan_workflow.py`: Workflow para realizar escaneos Nmap a máquinas objetivo.
- `gobuster_scan_workflow.py`: Workflow para realizar escaneos de directorios web con Gobuster.

## Cómo Añadir un Nuevo Workflow

1. Crea un nuevo archivo Python en este directorio con un nombre descriptivo (ej. `nikto_scan_workflow.py`).
2. Sigue la estructura básica descrita anteriormente.
3. Define la función principal del workflow con parámetros claros y documentación.
4. Implementa la lógica para llamar a la herramienta correspondiente del servidor MCP de Kali.
5. Maneja los posibles errores y devuelve un resultado estructurado.
6. Importa el nuevo workflow en `htb-agent/agent_scripts/main_agent.py` si es necesario integrarlo en el flujo principal.

## Integración con el Agente

El agente principal (`HTBAgent` en `main_agent.py`) orquesta la ejecución de estos workflows basándose en la información de la máquina y las reglas definidas. Cada workflow debe ser modular, realizar una única tarea específica, y devolver resultados que puedan ser procesados por el agente.
