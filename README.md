# Proyecto HTB Agent

Este proyecto tiene como objetivo desarrollar un agente de IA para `cline.bot` que asista en la resolución de máquinas de Hack The Box (HTB) y CTFs de seguridad, utilizando un servidor MCP de Kali Linux.

## Filosofía del Proyecto

Este proyecto adopta un enfoque basado en **documentación en lenguaje natural** en lugar de código Python para definir los workflows. Esto aprovecha las capacidades nativas de `cline.bot` para interactuar directamente con el servidor MCP de Kali, sin necesidad de capas adicionales de abstracción.

El agente de IA interpreta:
- La estructura general del flujo de trabajo definida en `main_agent.py`
- Las implementaciones detalladas de cada workflow en `workflows.md`
- La información específica de cada máquina en su archivo `info.json`

## Estructura del Proyecto

- `htb-agent/`: Contiene la lógica principal del agente y sus configuraciones.
    - `workflows/`: Define los flujos de trabajo para interactuar con las herramientas.
        - `workflows.md`: Documentación detallada de cada workflow en lenguaje natural.
    - `rules/`: Contendrá las reglas y heurísticas para la toma de decisiones de la IA.
    - `ctf_docs/`: Almacena la documentación y la información de entrada/salida para cada máquina CTF.
        - `[nombre_maquina]/`: Carpeta para una máquina específica (ej. `titanic.htb/`).
            - `info.json`: Archivo con la información de la máquina y los resultados del agente.
    - `mcp_configs/`: Configuraciones para el servidor MCP de Kali.
    - `agent_scripts/`: Scripts principales que implementan la estructura del agente.
        - `main_agent.py`: Define la estructura general del flujo de trabajo.
    - `demo_executor.py`: Script de demostración para simular la ejecución del agente.

## Cómo Usar el Agente

Para que el agente de `cline.bot` comience a trabajar en una máquina HTB:

1.  **Prepara la Carpeta de la Máquina:**
    *   Crea una nueva carpeta dentro de `htb-agent/ctf_docs/` con el nombre de la máquina (ej. `htb-agent/ctf_docs/titanic.htb/`).
    *   Dentro de esta carpeta, crea un archivo `info.json` con la información mínima requerida.

2.  **Información Mínima Requerida en `info.json`:**
    El archivo `info.json` debe contener al menos los siguientes campos:
    ```json
    {
      "target_ip": "DIRECCION_IP_DE_LA_MAQUINA",
      "hostname": "NOMBRE_DE_HOST_DE_LA_MAQUINA",
      "os": "SISTEMA_OPERATIVO_DE_LA_MAQUINA",
      "initial_scan_results": [],
      "known_vulnerabilities": [],
      "credentials": {},
      "notes": ""
    }
    ```
    *   `target_ip`: La dirección IP de la máquina objetivo (ej. "10.10.11.55").
    *   `hostname`: El nombre de host de la máquina (ej. "titanic.htb").
    *   `os`: El sistema operativo de la máquina (ej. "Linux", "Windows").
    *   Los demás campos (`initial_scan_results`, `known_vulnerabilities`, `credentials`, `notes`) serán actualizados por el agente a medida que avanza.

3.  **Invoca al Agente:**
    Una vez que el `info.json` esté preparado, puedes invocar al agente dándome una instrucción como:
    ```
    Cline, inicia el agente para la máquina '[nombre_maquina]'
    ```
    (ej. "Cline, inicia el agente para la máquina 'titanic.htb'")

    Yo (el agente) leeré el `info.json`, interpretaré la estructura del flujo de trabajo definida en `main_agent.py`, y consultaré las implementaciones detalladas en `workflows.md` para ejecutar directamente las herramientas necesarias a través de mi capacidad nativa `use_mcp_tool`.

## Servidor MCP de Kali

Este proyecto requiere un servidor MCP de Kali Linux configurado y accesible. Las configuraciones de conexión se encuentran en `htb-agent/mcp_configs/kali_mcp_config.py`.

**Configuración Actual del Servidor Kali MCP:**
- **Nombre del Servidor:** `kali-mcp`
- **URL:** `http://10.196.1.68:5000`

Asegúrate de que tu máquina virtual Kali esté encendida, el servidor MCP esté ejecutándose y sea accesible, y que esté habilitado en la configuración de tus servidores MCP en VSCode.

## Workflows Implementados

Los workflows implementados se describen detalladamente en `htb-agent/workflows/workflows.md` e incluyen:

1. **Conexión a la VPN de HTB**
2. **Configuración del Archivo Hosts**
3. **Escaneo Inicial con Nmap**
4. **Enumeración Web con Gobuster**
5. **Análisis Web con Nikto**
6. **Búsqueda de Vulnerabilidades SQL con SQLMap**
7. **Ataque de Fuerza Bruta con Hydra**
8. **Ejecución Asincrónica de Herramientas**

El workflow #8 (Ejecución Asincrónica de Herramientas) es especialmente útil para herramientas que requieren tiempos de ejecución prolongados como Gobuster o Nikto. Este patrón permite ejecutar herramientas en segundo plano y recuperar los resultados posteriormente, evitando timeouts y mejorando la eficiencia del flujo de trabajo.

### Ejemplo de Ejecución Asincrónica

```bash
# 1. Ejecutar herramientas en segundo plano
mkdir -p /home/kali/scan_results/machine_name && nohup gobuster dir -u http://machine_name.htb -w /usr/share/wordlists/dirb/common.txt -o /home/kali/scan_results/machine_name/gobuster_dirs.txt > /dev/null 2>&1 &

# 2. Verificar estado de herramientas
ps aux | grep -E 'gobuster|nikto' | grep -v grep

# 3. Recuperar resultados cuando estén disponibles
cat /home/kali/scan_results/machine_name/gobuster_dirs.txt
```

Para más detalles sobre la implementación de cada workflow, consulta `workflows.md`.

## Fases del Proceso de Resolución

El agente sigue un proceso estructurado para resolver máquinas HTB:

1. **Preparación del Entorno**: Conexión VPN, configuración de hosts
2. **Reconocimiento Inicial**: Escaneo Nmap para descubrir servicios
3. **Enumeración de Servicios**: Análisis detallado de cada servicio descubierto
4. **Explotación Inicial**: Aprovechamiento de vulnerabilidades para acceso inicial
5. **Post-Explotación y Escalada de Privilegios**: Afianzamiento y elevación de privilegios

Estas fases se definen en `htb-agent/agent_scripts/main_agent.py`, aunque el agente puede adaptarlas según las características específicas de cada máquina.
