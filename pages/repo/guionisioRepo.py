from google import genai
import os
import time

def guionisio_prompt(brand_name, brand_desc, socnet, mode, theme, strategy, periodity, full_period):
    prompt = f"Eres Guionisio, un experto en redacción de guiones para contenidos de redes sociales como Instagram, LinkedIn, TikTok, YouTube y difusiones por WhatsApp. Eres el redactor de {brand_name}, que es y hace {brand_desc}. Conoces todo el proceso de ideación, investigación en diversas fuentes y redacción, y, mediante la información que te doy, persuades a la audiencia a cumplir el objetivo. Vas a generar una campaña con sus respectivos guiones y días en que se va a subir cada contenido. El contenido es para publicar en {socnet} en formato {mode}, y los temas son sobre {theme}. La estrategia que se va a seguir es {strategy}, y la periodicidad de publicación es {periodity} durante {full_period}. Genera la campaña con los siguientes encabezados: Día, Redes sociales, Tema, Título del contenido, Descripción del contenido, Hashtags y copy sugeridos, guión, Llamado a la acción. La tabla debe tener tantos días como sea necesario para cumplir con la periodicidad y el tiempo total de la campaña. Asegúrate de que los temas y títulos sean variados y atractivos para la audiencia objetivo. El llamado a la acción debe ser claro y relevante para cada publicación. **INSTRUCCIONES DE FORMATO:** Devuelve el resultado **únicamente en formato CSV**, ccon las columnas: Día, Redes sociales, Tema, Título del contenido, Descripción del contenido, Hashtags y copy sugeridos, Guión, Llamado a la acción. No incluyas texto explicativo ni comentarios, solo el contenido CSV."

    return prompt

def modelExec(brandbook, example_contents, prompt, api):
    # Inicializamos la lista vacía
    allfiles = []

     # ✅ Agregar archivos correctamente
    if brandbook:
        allfiles.append(brandbook)
    if example_contents:
        # Si example_contents puede ser una lista de archivos
        if isinstance(example_contents, list):
            allfiles.extend(example_contents)
        else:
            allfiles.append(example_contents)

    client = genai.Client(api_key=api)
    print("API Key recibida:", api)  # Verifica que la API Key se reciba correctamente
    print("Contenido recibido:", prompt)  # Verifica que el contenido se reciba correctamente

    uploaded_files = []

    for files in allfiles:
            # 🔍 Validar que el archivo sea IOBase, binario y seekable
        if not hasattr(files, "read"):
            raise TypeError("El objeto recibido no tiene método 'read'; asegúrate de pasar un archivo válido.")

        if not hasattr(files, "seek"):
            raise TypeError("El archivo no es seekable; Gemini requiere que pueda reposicionarse con .seek().")
        
        # 👇 Detectar MIME directamente desde el objeto de Streamlit
        mime_type = getattr(files, "type", None) or "application/octet-stream"
        
        try:
            # Regresamos el puntero al inicio por si el archivo fue leído antes
            files.seek(0)
        except Exception as e:
            raise ValueError(f"No se pudo reposicionar el archivo: {e}")
        
        myfile = client.files.upload(
        file=files,
        config={"display_name": getattr(files, "name", "archivo_subido", ), "mime_type": mime_type}
        )

        while myfile.state.name == "PROCESSING":
            print("El archivo aún se está procesando. Esperando 10 segundos...")
            time.sleep(5)
            myfile = client.files.get(name=myfile.name)

        if myfile.state.name == "FAILED":
            raise ValueError("El procesamiento del archivo falló.")
        
        uploaded_files.append(myfile)
        
    response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[*uploaded_files, prompt]
    )
        
    return response.text