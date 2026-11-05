# PUNTO A: Normalización de Lecturas

def limpiar_registro_sensor(registro_raw: dict):

    # Copia para no alterar el diccionario original.
    registro_limpio = {}
    
    # Limpiar el ID del sensor.
    raw_id = registro_raw.get("sensor_id", "DESCONOCIDO")
    registro_limpio["sensor_id"] = str(raw_id).strip()
    
    # Limpiar y convertir la temperatura.
    raw_temp = registro_raw.get("temperatura", "0.0")
    # Filtrar solo los caracteres que forman parte del número.
    temp_filtrada = "".join(c for c in str(raw_temp) if c.isdigit() or c in ".-")
    
    try:
        registro_limpio["temperatura"] = float(temp_filtrada)
    except ValueError:
        registro_limpio["temperatura"] = 0.0  # Valor por defecto seguro en caso de error.
        
    # Validar la ubicación con valor por defecto seguro.
    ubicacion = registro_raw.get("ubicacion")
    if ubicacion and str(ubicacion).strip():
        registro_limpio["ubicacion"] = str(ubicacion).strip()
    else:
        registro_limpio["ubicacion"] = "Ubicación Desconocida"
        
    return registro_limpio


# PUNTO B: Monitoreo y Mapeo Estadístico

def generar_resumen_sensores(lista_sensores_limpios: list, umbral_temperatura: float):

    #Se Analizan los registros limpios para identificar sensores que superan el umbral. 
    # Y se calcula el promedio térmico global de la planta.

    if not lista_sensores_limpios:
        return [], 0.0

    sensores_alerta = []
    suma_temperaturas = 0.0

    for sensor in lista_sensores_limpios:
        temp = sensor["temperatura"]
        suma_temperaturas += temp
        
        # Verificar si supera el umbral de alerta.
        if temp > umbral_temperatura:
            sensores_alerta.append(sensor["sensor_id"])

    promedio_temperatura = suma_temperaturas / len(lista_sensores_limpios)
    
    return sensores_alerta, round(promedio_temperatura, 2)


# Bloque de pruebas con datos.
if __name__ == "__main__":
    # Datos crudos recibidos de EcoTech Solutions.
    datos_crudos = [
        {"sensor_id": "  SENSOR-001  ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": "31.2°C", "ubicacion": "   Planta Sur   "},
        {"sensor_id": " SENSOR-003 ", "temperatura": "19.8 C"}, 
        {"sensor_id": "SENSOR-004", "temperatura": "35.0", "ubicacion": ""}, 
        {"sensor_id": " SENSOR-005 ", "temperatura": "28.7C", "ubicacion": "Almacén Central"}
    ]
    
    # Definición del umbral crítico de temperatura.
    Umbral_Critico = 30.0

    print("--- Iniciando el procesamiento de datos ---")
    
    # Sanitización.
    registros_sanitizados = [limpiar_registro_sensor(reg) for reg in datos_crudos]
    
    print("Registros Sanitizados con Éxito:")
    for r in registros_sanitizados:
        print(f"  {r}")

    # Análisis Estadístico.
    alertas, promedio_global = generar_resumen_sensores(registros_sanitizados, Umbral_Critico)

    # Impresión formateada del reporte final.
    print("\n" + "="*45)
    print("      REPORTE CONSOLIDADO - ECOTECH SOLUTIONS      ")
    print("="*45)
    print(f"Temperatura Promedio Global: {promedio_global}°C")
    print(f"Umbral de Alerta Definido:   {Umbral_Critico}°C")
    print("-"*45)
    
    if alertas:
        print(f"DISPOSITIVOS EN ALERTA CRÍTICA ({len(alertas)}):")
        for id_sensor in alertas:
            print(f"  • {id_sensor}")
    else:
        print("No se detectaron sensores superando el umbral térmico.")
    print("="*45)
