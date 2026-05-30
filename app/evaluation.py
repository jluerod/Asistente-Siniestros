from conversation import clasificar_siniestro
import pandas as pd
df = pd.read_excel('SINIESTROS_FILTERED.xlsx')
df = df.drop_duplicates(subset=["DESCRIPCION_SINIESTRO"])
df = df.fillna("DESCONOCIDO")
df =df.sample(100)
acierto_base = 0
fallo_base = 0
acierto_train = 0
fallo_train = 0
for index, i in df.iterrows():
    print(f"Clasificando {index}...")
    resultado_base,x= clasificar_siniestro(i["DESCRIPCION_SINIESTRO"], False)
    resultado_train,x = clasificar_siniestro(i["DESCRIPCION_SINIESTRO"], True)
    if i["GREMIO"] == resultado_base['gremio']:
        acierto_base += 1
    if i["GREMIO"] == resultado_train['gremio']:
        acierto_train += 1
    
acc_base = acierto_base / len(df) * 100
acc_train = acierto_train / len(df) * 100
print(f"Accuracy sin RAG: {acc_base}%")
print(f"Accuracy con RAG: {acc_train}%")