import json
import os
import urllib.request
from urllib.error import HTTPError

# Cargar variables secretas (limpiando espacios en blanco por si acaso)
gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
supabase_url = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
supabase_key = os.environ.get("SUPABASE_KEY", "").strip()

print("Iniciando generacion de reto...")

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

# Actualizado al modelo "latest"
gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={gemini_key}"
headers = {"Content-Type": "application/json"}
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"response_mime_type": "application/json"},
}

req = urllib.request.Request(
    gemini_url, data=json.dumps(payload).encode("utf-8"), headers=headers
)

try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
        data_json = json.loads(raw_text)
        print("¡Gemini respondio correctamente!")
except HTTPError as e:
    print(f"ERROR EN GEMINI (Codigo {e.code}):")
    print(e.read().decode("utf-8"))
    exit(1)

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

try:
    with urllib.request.urlopen(supa_req) as response:
        print("¡Reto del dia generado e insertado con exito en Supabase!")
except HTTPError as e:
    print(f"ERROR EN SUPABASE (Codigo {e.code}):")
    print(e.read().decode("utf-8"))
    exit(1)
