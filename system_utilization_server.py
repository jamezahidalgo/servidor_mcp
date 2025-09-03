from mcp.server.fastmcp import FastMCP
import psutil
import socket
import mcp

mcp = FastMCP("Servidor para ver la utilización de recursos de un sistema.")

@mcp.tool()
def get_current_system_utilization() -> dict:
    """
    Obtiene la utilización del sistema.
    """
    utilization = {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
    return utilization

@mcp.prompt()
def current_system_utilization():
    return "¿Cuál es la utilización actual del sistema?"

@mcp.resource(
    uri="sys://machine/hostname",
    mime_type="text/plain",
    name="Hostname",
    description="Nombre de host del servidor (machine hostname)."
)
def machine_hostname() -> str:
    return socket.gethostname()

if __name__ == "__main__":
    mcp.run(transport="stdio")