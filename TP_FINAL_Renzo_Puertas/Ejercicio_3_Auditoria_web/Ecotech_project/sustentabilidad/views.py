from django.shortcuts import render

from .services import obtener_metricas_consumo

def vista_panel_sustentabilidad(request): 

    registro_historicos = [
        {"planta": "Planta Norte", "consumo_kwh": 1400.0},
        {"planta": "Planta Sur", "consumo_kwh": 3600.40},
        {"planta": "Planta Este", "consumo_kwh": 750.4},
        {"planta": "Planta Oeste", "consumo_kwh": 2400.0},
        {"planta": "Planta Norte", "consumo_kwh": 300.0},
    ]

    metricas = obtener_metricas_consumo(registro_historicos)

    contexto = {
    "total_emisiones": metricas["total_global_emisiones"],
    "planta_mayor_consumo": metricas["planta_mayor_consumo"],
    "detalle_emisiones": metricas["emisiones_por_planta"]
     }

    return render(request, 'sustentabilidad/panel.html', contexto)


