import json
import os
from typing import List

# PUNTO A: Dominio del Catálogo y Excepciones

class StockInvalidoError(Exception):
    # Excepción personalizada para controlar inventarios negativos.
    def __init__(self, mensaje: str = "El stock no puede ser un valor negativo."):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class DispositivoEcologico:
    # Clase base para la jerarquía de productos sustentables de EcoTech.
    def __init__(self, id_producto: str, nombre: str, precio: float, stock: int):
        self.id_producto: str = id_producto
        self.nombre: str = nombre
        self.precio: float = precio
        self._stock: int = 0
        self.stock = stock

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, nuevo_stock: int):
        if nuevo_stock < 0:
            raise StockInvalidoError(
                f"Error en producto '{self.nombre}' (ID: {self.id_producto}): "
                f"Intento de asignar stock negativo ({nuevo_stock})."
            )
        self._stock = nuevo_stock

    def generar_ficha_tecnica(self):
        return (
            f"--- Ficha Técnica ECOTECH ---\n"
            f"ID: {self.id_producto}\n"
            f"Producto: {self.nombre}\n"
            f"Precio: ${self.precio:,.2f}\n"
            f"Disponibilidad: {self._stock} unidades"
        )

    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock
        }


class PanelSolar(DispositivoEcologico):
    def __init__(self, id_producto: str, nombre: str, precio: float, stock: int, 
                 potencia_w: int, eficiencia_porcentaje: float):
        # Se invoca al constructor de la clase padre.
        super().__init__(id_producto, nombre, precio, stock)
        self.potencia_w: int = potencia_w
        self.eficiencia_porcentaje: float = eficiencia_porcentaje

    def generar_ficha_tecnica(self):
       #Polimorfismo
        ficha_base = super().generar_ficha_tecnica()
        datos_especificos = (
            f"\nEspecificaciones Técnicas Solares:\n"
            f"  - Potencia Nominal: {self.potencia_w}W\n"
            f"  - Eficiencia de Conversión: {self.eficiencia_porcentaje}%\n"
            f"------------------------------"
        )
        return f"{ficha_base}{datos_especificos}"

    def to_dict(self):
        datos = super().to_dict()
        datos.update({
            "potencia_w": self.potencia_w,
            "eficiencia_porcentaje": self.eficiencia_porcentaje
        })
        return datos


# PUNTO B: Persistencia y Gestión del Catálogo

class GestorInventario:
    # Módulo encargado de la persistencia de datos del catálogo.
    
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos: List[DispositivoEcologico], ruta_archivo: str):
        # Serializa y almacena una lista de dispositivos en un archivo JSON.
        
            # Se transforman las instancias a diccionarios usando compresión de listas.
            catalogo_serializado = [disp.to_dict() for disp in lista_dispositivos]
            
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(catalogo_serializado, archivo, indent=4, ensure_ascii=False)

         
# Bloque de prueba de datos crudos.

if __name__ == "__main__":

    print("\n" + "="*45)
    print("      PRUEBAS DE CATÁLOGO DE ECOTECH SOLUTIONS      ")
    print("="*45)
    
    catalogo = [
        {
            "id_producto": "ECO-SOL-350",
            "nombre": "Panel Solar EcoPremium",
            "precio": 125000.00,
            "stock": 15,                
            "eficiencia": "21.5%",
            "potencia": 350
        },
        {
            "id_producto": "ECO-SOL-250",
            "nombre": "Panel Solar EcoStandard",
            "precio": 85000.00,
            "stock": 40,                
            "eficiencia": "18.2%",
            "potencia": 250
        },

        #Pruebas con productos invalidos.
        {
            "id_producto": "ECO-SOL-ERR",
            "nombre": "Panel EcoFallido",
            "precio": 50000.50,          
            "stock": -5,                  
            "eficiencia": "19.0%",
            "potencia": 300
        } ,
        {
            "id_producto": "ECO-SOL-ER2",
            "nombre": "Panel EcoFallido2",
            "precio": 70000.50,           
            "stock": -10,                  #
            "eficiencia": "22.0%",
            "potencia": 350
        }
    ]

    lista_productos_validos = []

    for datos in catalogo:
        print(f"\nRegistrando datos: {datos['nombre']}")
        try:
            panel = PanelSolar(
                id_producto=datos["id_producto"], 
                nombre=datos["nombre"], 
                precio=datos["precio"], 
                stock=datos["stock"], 
                eficiencia_porcentaje=datos["eficiencia"], 
                potencia_w=datos["potencia"]
            )
            ficha = panel.generar_ficha_tecnica()
            lista_productos_validos.append(panel)
            print(f" Éxito: {ficha}")
        except StockInvalidoError as e:
            print(f" Error de Stock: {e}")
        except ValueError as e:
            print(f" Error de Formato (ValueError): {e}")
        except Exception as e:
            print(f" Error inesperado: {e}")

    print("\n" + "="*45)

    os.makedirs("Ejercicio_2_Productos", exist_ok=True)
    ruta_archivo = "Ejercicio_2_Productos/catalogo_ecotech.json"
    
    try:
        GestorInventario.guardar_catalogo_json(lista_productos_validos, ruta_archivo)
        print(f"Archivo guardado correctamente en: '{ruta_archivo}'")
    except Exception as e:
        print(f" Error al escribir el archivo: {e}")

    print("="*45)    