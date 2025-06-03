#!/usr/bin/env python3
"""
Demostración del ejecutor del agente HTB.

Este script simula la forma en que el agente de cline.bot orquestaría
la ejecución del HTBAgent para una máquina específica.

En la implementación real, el agente de cline.bot no ejecutaría este script directamente,
sino que utilizaría el conocimiento del flujo de trabajo definido en htb-agent/agent_scripts/main_agent.py
y las implementaciones de workflows descritas en htb-agent/workflows/workflows.md para ejecutar
directamente las herramientas MCP de Kali.

Uso:
    python3 demo_executor.py [nombre_maquina]

    Si no se proporciona un nombre de máquina, se utilizará 'machine_name_example'.
"""

import sys
import os
from agent_scripts.main_agent import HTBAgent

def main():
    # Determinar qué máquina procesar
    if len(sys.argv) > 1:
        target_machine = sys.argv[1]
    else:
        print("No se proporcionó un nombre de máquina. Usando 'machine_name_example' por defecto.")
        target_machine = "machine_name_example"
    
    # Construir la ruta al info.json
    ctf_info_path = f"ctf_docs/{target_machine}/info.json"
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ctf_info_path)
    
    # Verificar que el archivo info.json existe
    if not os.path.exists(full_path):
        print(f"Error: No se encontró el archivo info.json para la máquina '{target_machine}'.")
        print(f"Se esperaba en: {full_path}")
        print("Asegúrate de crear la carpeta y el archivo info.json con la información básica de la máquina.")
        sys.exit(1)
    
    print(f"=== Iniciando Demostración del Agente HTB para '{target_machine}' ===")
    print(f"Utilizando info.json de: {full_path}")
    print()
    
    try:
        # Crear el agente y ejecutar su workflow
        # NOTA: En un entorno real, el agente de cline.bot interpretaría este flujo
        # y usaría directamente sus capacidades nativas con use_mcp_tool en lugar
        # de ejecutar este script.
        agent = HTBAgent(full_path)
        agent.run_workflow()
        print("\n=== Demostración completada ===")
        print("\nRECUERDA: Esta es solo una SIMULACIÓN del flujo de trabajo.")
        print("En un entorno real, el agente cline.bot ejecutaría")
        print("directamente las herramientas MCP de Kali.")
        
    except Exception as e:
        print(f"\nError durante la ejecución del agente: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
