import re

def limpiar_descripcion(desc):
    desc = desc.lower()
    desc = re.sub(r'\d{9}', '', desc)
    desc = re.sub(r'tlf[:\s]*', '', desc)
    desc = re.sub(r'tfno[:\s]*', '', desc)
    desc = re.sub(r'\baseg\.', '', desc)
    desc = re.sub(r'\s[\/\-\*]\s', ' ', desc)
    desc = re.sub(r'\s+', ' ', desc).strip()
    return desc
pruebas = [
    "INDICA ASEG. QUE LA PUERTA TLF: 660890374",
    "MARIA ANGELES MEDIADORA LLAMA PORQUE EL INQUILINO CARLOS TIENE ATASCO TLF 633440919",
    "LLAMA MARINA INDICA QUE DESDE LAS 3 DE LA MAANA SE LES FUE LA LUZ TFNO 679930233"
]

for p in pruebas:
    print(limpiar_descripcion(p))