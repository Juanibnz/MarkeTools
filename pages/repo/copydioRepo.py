from google import genai
import time

def copydioPromptCreation(redesSociales, intencionComunica, nombreEmpresa, descEmpresa):

    promptCopydio = f"Eres Copydio, un experto en redacción de copys, captions y hashtags para posts de redes sociales como Instagram, LinkedIn, TikTok, emails y difusiones por WhatsApp. Eres el redactor de {nombreEmpresa}, una empresa que se define como: {descEmpresa}. Conoces todo el proceso de ideación, investigación en diversas fuentes y redacción, y, mediante la información que te doy, persuades a la audiencia a cumplir el objetivo. Vas a generar 3 posibles opciones de caption y, si son para distintas redes sociales, indicar para cuales. Usa este video como base para escribir el copy de cada red social. Este copy es especificamente para compartir en {redesSociales}. El objetivo de este copy es comunicar {intencionComunica}. No olvides incluir emojis y hashtags relevantes. Máximo 5 hashtags, siempre en minúsculas. Usa un formato de texto sin estilos: Es decir, no uses asteriscos, guiones o elementos de markdown dentro de los copys. Tu respuesta completa debe estar en formato markdown. No incluyas cabeceras ni saludos, solo el contenido generado."

    return promptCopydio


def modelExec(content, redesSociales, intencionComunica, nombreEmpresa, descEmpresa, api):
    client = genai.Client(api_key=api)
    prompt = copydioPromptCreation(redesSociales, intencionComunica, nombreEmpresa, descEmpresa)
    print("API Key recibida:", api)  # Verifica que la API Key se reciba correctamente
    print("Contenido recibido:", content)  # Verifica que el contenido se reciba correctamente

     # 🔍 Validar que el archivo sea IOBase, binario y seekable
    if not hasattr(content, "read"):
        raise TypeError("El objeto recibido no tiene método 'read'; asegúrate de pasar un archivo válido.")

    if not hasattr(content, "seek"):
        raise TypeError("El archivo no es seekable; Gemini requiere que pueda reposicionarse con .seek().")
    
    # 👇 Detectar MIME directamente desde el objeto de Streamlit
    mime_type = getattr(content, "type", None) or "application/octet-stream"
    
    try:
        # Regresamos el puntero al inicio por si el archivo fue leído antes
        content.seek(0)
    except Exception as e:
        raise ValueError(f"No se pudo reposicionar el archivo: {e}")

    myfile = client.files.upload(
        file=content,
        config={"display_name": getattr(content, "name", "archivo_subido", ), "mime_type": mime_type}
        )

    while myfile.state.name == "PROCESSING":
        print("El archivo aún se está procesando. Esperando 10 segundos...")
        time.sleep(5)
        myfile = client.files.get(name=myfile.name)

    if myfile.state.name == "FAILED":
        raise ValueError("El procesamiento del archivo falló.")
    
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[myfile, prompt]
    )

    return response.text