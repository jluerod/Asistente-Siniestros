import chromadb
import pandas as pd


"""df = pd.read_excel('SINIESTROS_FILTERED.xlsx')
df = df.drop_duplicates(subset=["DESCRIPCION_SINIESTRO"])
df = df.fillna("DESCONOCIDO")"""
chroma_client = chromadb.PersistentClient(path="./data/chroma")
siniestros = chroma_client.get_or_create_collection(name="siniestros")
"""batch_size = 1000
for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    siniestros.add(
        documents=batch["DESCRIPCION_SINIESTRO"].tolist(),
        metadatas=batch[["GREMIO", "GARANTIA"]].to_dict(orient="records"),
        ids=batch.index.astype(str).tolist()
    )
    print(f"Cargados {min(i+batch_size, len(df))}/{len(df)}")
print(f"Total documentos en ChromaDB: {siniestros.count()}")"""
def buscar_similares (descripción):
    results = siniestros.query(query_texts = [descripción], n_results=3)
    casos = []
    for desc, datos in zip(results['documents'][0], results['metadatas'][0]):
        casos.append({"descripcion": desc, "gremio": datos["GREMIO"], "garantia": datos["GARANTIA"]})

    return casos
