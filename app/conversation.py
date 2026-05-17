import ollama
import json

messages=[{'role': 'system', 'content': """Eres un clasificador de siniestros de hogar para compañías aseguradoras españolas.

Cuando recibas la descripción de un siniestro debes responder ÚNICAMENTE con un JSON con este formato:
{
    "gremio": "el gremio que corresponde",
    "garantia": "la garantía que corresponde"
}

Los gremios posibles son: Electricidad, Bricolaje, Pocería, Fontanería, Albañilería, Pintura, Cerrajería, Toldos, Mantenimiento, Carpintería, Loza Sanitaria, Persianas, Otros, Carpintería Metálica, Marmolista, Tejados, Carpintería de Aluminio, Desatascos, Parquet, Jardinería, Localización de Fugas, Limpiezas, Cerrajería y Carpintería metálica, Escayola, Piscinas, Aislamiento, Urgencias Fontanería, Urgencias Cerrajería, Urgencias Electricidad, Manitas, Bricomanitas, Mamparas, Moquetas.

Las garantías posibles son: DAÑOS ELECTRICOS, BRICOPARTNER, DAÑOS AGUA, SERVICIO ASISTENCIA, LLUVIA, MANTENIMIENTO, ROBO, LOZAS-MARMOLES, PEDRISCO-NIEVE, VIENTO, AVERIA SIN DAÑOS (AGUA), BRICOLAJE, CRISTALES-ESPEJOS, ACTOS VANDALICOS, INCENDIO, DAÑOS ELÉCTRICOS, FENOMENOS METEOROLÓGICOS, RESPONSABILIDAD CIVIL, EXPLOSION, HUMO, ATASCOS, BRICO-MANITAS, LLUVIA VIENTO PEDRISCO NIEVE, INUNDACION, ESCAPES DE AGUA, entre otras.

No añadas explicaciones ni texto adicional, responde solo con el JSON."""}]

user_input = input()
messages= messages + [{'role': 'user', 'content': user_input}]
response_content = ""
response = ollama.chat("llama3.1:8b",messages)
response_content = response.message.content
print(response_content, end='', flush=True)


print('\n')
json_response = json.loads(response_content)
print(json_response)
