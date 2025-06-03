# Workflows para la Resolución de Máquinas HTB

Este documento describe en lenguaje natural los workflows (flujos de trabajo) que yo, como agente de `cline.bot`, debo seguir para resolver máquinas de Hack The Box. En lugar de implementar estos workflows como scripts Python, uso mis capacidades nativas para interactuar directamente con el servidor MCP de Kali.

## 1. Conexión a la VPN de HTB

**Descripción:** Este workflow establece la conexión VPN a la red de Hack The Box.

**Requisitos:**
- Archivo de configuración OpenVPN en la máquina Kali (típicamente en `/home/kali/htb.ovpn`)
- Contraseña de la máquina Kali para ejecutar comandos sudo

**Pasos:**
1. Verificar si hay una conexión OpenVPN activa
2. Si existe, detenerla con `sudo pkill openvpn`
3. Iniciar una nueva conexión con `sudo nohup openvpn /home/kali/htb.ovpn &`

**Implementación con `use_mcp_tool`:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="execute_command",
    arguments={
        "command": "echo 'kali' | sudo -S pkill openvpn && echo 'kali' | sudo -S nohup openvpn /home/kali/htb.ovpn &"
    }
)
```

## 2. Configuración del Archivo Hosts

**Descripción:** Este workflow añade el hostname y la IP de la máquina objetivo al archivo `/etc/hosts` de la máquina Kali.

**Requisitos:**
- IP de la máquina objetivo
- Hostname de la máquina objetivo
- Contraseña de la máquina Kali para ejecutar comandos sudo

**Pasos:**
1. Añadir la entrada al archivo `/etc/hosts` con el formato `IP hostname`

**Implementación con `use_mcp_tool`:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="execute_command",
    arguments={
        "command": f"echo 'kali' | sudo -S sh -c \"echo '{target_ip} {hostname}' >> /etc/hosts\""
    }
)
```

## 3. Escaneo Inicial con Nmap

**Descripción:** Este workflow realiza un escaneo Nmap inicial para identificar puertos abiertos y servicios en la máquina objetivo.

**Requisitos:**
- IP de la máquina objetivo

**Parámetros:**
- `target`: IP de la máquina objetivo
- `scan_type`: Tipo de escaneo (por defecto "-sV" para detección de versiones)
- `ports`: Rango de puertos a escanear (por defecto "1-1024")
- `additional_args`: Argumentos adicionales (por defecto "-Pn" para evitar el ping)

**Implementación con `use_mcp_tool`:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="nmap_scan",
    arguments={
        "target": target_ip,
        "scan_type": "-sV",
        "ports": "1-1024",
        "additional_args": "-Pn"
    }
)
```

## 4. Enumeración Web con Gobuster

**Descripción:** Este workflow realiza un escaneo de directorios web utilizando Gobuster.

**Requisitos:**
- URL del servidor web objetivo

**Parámetros:**
- `url`: URL del objetivo (ej. "http://titanic.htb")
- `mode`: Modo de escaneo (por defecto "dir" para directorios)
- `wordlist`: Ruta a la lista de palabras (por defecto "/usr/share/wordlists/dirb/common.txt")
- `additional_args`: Argumentos adicionales (opcional)

**Implementación con `use_mcp_tool`:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="gobuster_scan",
    arguments={
        "url": target_url,
        "mode": "dir",
        "wordlist": "/usr/share/wordlists/dirb/common.txt",
        "additional_args": ""
    }
)
```

## 5. Análisis Web con Nikto

**Descripción:** Este workflow realiza un análisis de vulnerabilidades web utilizando Nikto.

**Requisitos:**
- URL o IP del servidor web objetivo

**Parámetros:**
- `target`: URL o IP del objetivo
- `additional_args`: Argumentos adicionales (opcional)

**Implementación con `use_mcp_tool`:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="nikto_scan",
    arguments={
        "target": target_url,
        "additional_args": ""
    }
)
```

## 6. Búsqueda de Vulnerabilidades SQL con SQLMap

**Descripción:** Este workflow busca vulnerabilidades de inyección SQL utilizando SQLMap.

**Requisitos:**
- URL del objetivo con parámetros potencialmente vulnerables

**Parámetros:**
- `url`: URL del objetivo
- `data`: Datos POST (opcional)
- `additional_args`: Argumentos adicionales (opcional)

**Implementación con `use_mcp_tool`:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="sqlmap_scan",
    arguments={
        "url": target_url,
        "data": post_data,
        "additional_args": "--batch --dbs"
    }
)
```

## 7. Ataque de Fuerza Bruta con Hydra

**Descripción:** Este workflow realiza ataques de fuerza bruta contra servicios de autenticación.

**Requisitos:**
- IP del objetivo
- Servicio objetivo (ssh, ftp, http-post-form, etc.)
- Lista de usuarios o contraseñas

**Parámetros:**
- `target`: IP del objetivo
- `service`: Servicio a atacar
- `username`/`username_file`: Usuario o archivo de usuarios
- `password`/`password_file`: Contraseña o archivo de contraseñas
- `additional_args`: Argumentos adicionales (opcional)

**Implementación con `use_mcp_tool`:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="hydra_attack",
    arguments={
        "target": target_ip,
        "service": "ssh",
        "username_file": "/path/to/users.txt",
        "password_file": "/usr/share/wordlists/rockyou.txt",
        "additional_args": ""
    }
)
```

---

## 8. Ejecución Asincrónica de Herramientas

**Descripción:** Este workflow ejecuta herramientas de escaneo en segundo plano y guarda los resultados en archivos para revisarlos posteriormente, sin bloquear la ejecución del agente.

**Requisitos:**
- Herramienta de escaneo a ejecutar
- Ubicación para almacenar los resultados

**Pasos:**
1. Crear directorios para almacenar resultados si no existen
2. Ejecutar la herramienta en segundo plano con nohup y redirigir salida a archivo
3. Continuar con otras tareas mientras la herramienta se ejecuta
4. Verificar el estado de la herramienta cuando sea necesario
5. Recuperar y analizar los resultados cuando estén disponibles

**Implementación con `use_mcp_tool` para Gobuster:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="execute_command",
    arguments={
        "command": "mkdir -p /home/kali/scan_results/titanic && nohup gobuster dir -u http://titanic.htb -w /usr/share/wordlists/dirb/common.txt -o /home/kali/scan_results/titanic/gobuster_dirs.txt > /dev/null 2>&1 &"
    }
)
```

**Implementación con `use_mcp_tool` para Nikto:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="execute_command",
    arguments={
        "command": "mkdir -p /home/kali/scan_results/titanic && nohup nikto -h http://titanic.htb -output /home/kali/scan_results/titanic/nikto_scan.txt > /dev/null 2>&1 &"
    }
)
```

**Verificación del estado:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="execute_command",
    arguments={
        "command": "ps aux | grep -E 'gobuster|nikto' | grep -v grep"
    }
)
```

**Recuperación de resultados:**
```
use_mcp_tool(
    server_name="kali-mcp",
    tool_name="execute_command",
    arguments={
        "command": "cat /home/kali/scan_results/titanic/gobuster_dirs.txt"
    }
)
```

Al utilizar este documento como guía, yo (como agente) puedo ejecutar directamente las herramientas del servidor MCP de Kali según el contexto específico de cada máquina, sin necesidad de capas adicionales de abstracción en código Python. Esta aproximación es más flexible y permite adaptarme mejor a las necesidades específicas de cada máquina HTB.
