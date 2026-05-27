import ollama
import json
from app.rag import buscar_similares
messages=[{'role': 'system', 'content': """Eres un clasificador de siniestros de hogar para compañías aseguradoras españolas.

Cuando recibas la descripción de un siniestro debes responder ÚNICAMENTE con un JSON con este formato:
{
    "gremio": "el gremio que corresponde",
    "garantia": "la garantía que corresponde"
}

Los gremios posibles son: Electricidad, Bricolaje, Pocería, Fontanería, Albañilería, Pintura, Cerrajería, Toldos, Mantenimiento, Carpintería, Loza Sanitaria, Persianas, Otros, Carpintería Metálica, Marmolista, Tejados, Carpintería de Aluminio, Desatascos, Parquet, Jardinería, Localización de Fugas, Limpiezas, Cerrajería y Carpintería metálica, Escayola, Piscinas, Aislamiento, Urgencias Fontanería, Urgencias Cerrajería, Urgencias Electricidad, Manitas, Bricomanitas, Mamparas, Moquetas.

Las garantías posibles son: DAÑOS ELECTRICOS, BRICOPARTNER, DAÑOS AGUA, SERVICIO ASISTENCIA, LLUVIA, MANTENIMIENTO, ROBO, LOZAS-MARMOLES, PEDRISCO-NIEVE, VIENTO, AVERIA SIN DAÑOS (AGUA), BRICOLAJE, CRISTALES-ESPEJOS, ACTOS VANDALICOS, INCENDIO, DAÑOS ELÉCTRICOS, FENOMENOS METEOROLÓGICOS, RESPONSABILIDAD CIVIL, EXPLOSION, HUMO, ATASCOS, BRICO-MANITAS, LLUVIA VIENTO PEDRISCO NIEVE, INUNDACION, ESCAPES DE AGUA, entre otras.

No añadas explicaciones ni texto adicional, responde solo con el JSON."""}]



def clasificar_siniestro(input):
    busqueda = buscar_similares(input)
    contexto = "\nAquí tienes 2 casos similares para ayudar a clasificar el siniestro:\n"
    rango = 1
    for i in range(len(busqueda)):
        contexto+= f"Caso {rango}: Descripción: {busqueda[i]['descripcion']} → Gremio: {busqueda[i]['gremio']}, Garantía: {busqueda[i]['garantia']}\n"
        rango += 1
    contexto += "\nAhora clasifica este siniestro:\n"
    mensaje= messages + [{'role': 'user', 'content': contexto + input}]
    response_content = ""
    response = ollama.chat("llama3.1:8b",mensaje)
    response_content = response.message.content
    '''print(response_content, end='', flush=True)'''


    
    json_response = json.loads(response_content)
    return json_response, True