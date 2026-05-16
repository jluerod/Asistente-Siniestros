import ollama


messages=[{'role': 'system', 'content': 'Eres un asistente médico inteligente y empático. Tu objetivo es ayudar al usuario a entender mejor su situación de salud y preparar su consulta médica. Cuando el usuario describe síntomas: - Haz preguntas de seguimiento para entender bien la situación: duración, intensidad, localización, factores que lo empeoran o mejoran, medicación actual, enfermedades previas. - Basándote en los síntomas, menciona las causas más comunes y probables de forma informativa. - Da recomendaciones prácticas: si algo requiere atención urgente, si puede esperar, qué tipo de especialista sería más adecuado, qué puede hacer el usuario para aliviar los síntomas mientras tanto. - Al final genera un informe estructurado con los síntomas, posibles causas y preguntas clave para llevar al médicoResponde siempre en español, con un tono cercano y claro. Evita tecnicismos innecesarios pero no simplifiques en exceso la información médica.'}]
        
while True:
    user_input = input()
    if user_input.lower() == 'exit':
        break
    response_content = ""
    for chunk in ollama.chat("llama3.1:8b", messages= messages + [{'role': 'user', 'content': user_input}], stream=True):
        if chunk.message:
            response_chunk = chunk.message.content
            print(response_chunk, end='', flush=True)
            response_content += response_chunk
    messages += [
        {'role': 'user', 'content': user_input},
        {'role': 'assistant', 'content': response_content},
    ]
    print('\n')
