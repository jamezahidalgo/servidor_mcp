"""
2 tools
1 resource
1 prompt
"""
from mcp.server.fastmcp import FastMCP

# ================================
# Estado en memoria (Resource)
# ================================
task_list = [
    {"id": 1, "titulo": "Preparar evaluación de Taller de BD", "estado": "pendiente", "prioridad": "media"},
    {"id": 2, "titulo": "Comprar café", "estado": "terminada", "prioridad": "baja"},
    {"id": 3, "titulo": "Calificar evaluaciones", "estado": "pendiente", "prioridad": "alta"},
]

# ================================
# Servidor MCP
# ================================
mcp = FastMCP("Servidor de gestión de tareas personales")

# -------- Resource --------
@mcp.resource(
    uri="tasks://task_list",
    mime_type="application/json",
    name="Lista de tareas",
    description="Tareas actuales con id, título, estado y prioridad."
)
def get_task_list() -> list[dict]:
    return task_list

# -------- Prompt --------
@mcp.prompt()
def resolver_rapido() -> str:
    """
    Obtiene la primera tarea pendiente de alta prioridad
    """    
    respuesta = "Sin pendientes de alta prioridad"
    for tarea in task_list:
        if tarea["estado"] == 'pendiente' and tarea["prioridad"] == 'alta' :
            respuesta = tarea["titulo"]
            break
    return respuesta


# -------- Tools --------
@mcp.tool()
def agrega_tarea(titulo: str, prioridad: str = "media") -> dict:
    """
    Agrega una nueva tarea a la lista de tareas.
    """
    new_id = max([t["id"] for t in task_list]) + 1 if task_list else 1
    task = {"id": new_id, "titulo": titulo, "estado": "pendiente", "prioridad": prioridad}
    task_list.append(task)
    return {"message": f"Tarea agregada con id {new_id}", "task": task}

@mcp.tool()
def actualiza_estado(id: int, estado: str) -> dict:
    """
    Actualiza el estado de una tarea (pendiente o terminada).
    """
    # Verifica el estado
    if estado not in ['pendiente', 'terminada']:
        return {"error": f"{estado} es inválido"}
    for tarea in task_list:
        if tarea["id"] == id:
            if not tarea["estado"] == estado:
                tarea["estado"] = estado
                return {"message": f"Tarea {id} actualizada a {estado}", "task": tarea}
            else:
                return {"error": f"El nuevo estado deber ser distinto al actual: {tarea["estado"]}"}            
    return {"error": f"No se encontró la tarea con id {id}"}

@mcp.tool()
def cambia_prioridad(id: int, prioridad: str) -> dict:
    """
    Cambia la prioridad de una tarea (alta, media o baja).
    """
    # Verifica la prioridad
    if estado not in ['alta', 'media', 'baja']:
        return {"error": f"{prioridad} es un valor inválido"}    

    for tarea in task_list:
        if tarea["id"] == id:            
            tarea["prioridad"] = prioridad
            return {"message": f"Tarea {id} actualizada a prioridad {prioridad}", "task": tarea}
    return {"error": f"No se encontró la tarea con id {id}"}

# ================================
# Main
# ================================
if __name__ == "__main__":
    mcp.run(transport="stdio")
