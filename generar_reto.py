import json
import os
import urllib.request

# Cargar variables secretas
gemini_key = os.environ.get("GEMINI_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL").rstrip("/")
supabase_key = os.environ.get("SUPABASE_KEY")

# 1. Preguntar a Gemini
prompt = (
    "Genera un reto de aprendizaje diario fascinante para investigar en 1 hora. "
    "Responde UNICAMENTE en formato JSON valido con este formato exacto:\n"
    "{\n"
    '  "titulo": "Titulo conciso del tema",\n'
    '  "descripcion": "Breve explicacion de lo que se va a investigar",\n'
    '  "pregunta_clave": "Pregunta principal a resolver en esa hora",\n'
    '  "categoria": "Tecnologia / Historia / Ciencia / Negocios / Arte"\n'
    "}"
)

gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
headers = {"Content-Type": "application/json"}
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"response_mime_type": "application/json"},
}

req = urllib.request.Request(
    gemini_url, data=json.dumps(payload).encode("utf-8"), headers=headers
)
with urllib.request.urlopen(req) as response:
    res_data = json.loads(response.read().decode("utf-8"))

# Extraer JSON de la respuesta de Gemini
raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
data_json = json.loads(raw_text)

# 2. Guardar en Supabase
supabase_endpoint = f"{supabase_url}/rest/v1/retos"
supa_headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal",
}

supa_req = urllib.request.Request(
    supabase_endpoint,
    data=json.dumps(data_json).encode("utf-8"),
    headers=supa_headers,
    method="POST",
)
with urllib.request.urlopen(supa_req) as response:
    print("¡Reto del dia generado e insertado con exito en Supabase!")
