# curate.py
################################################################################
from imagen import Imagen                                                       # unsere class
import asyncio                                                                  # für parallele IO prozesse
from openai import AsyncOpenAI                                                  # für openai im async modus
from dotenv import load_dotenv                                                  # für secrets in .env
from os import getenv, rename                                                   # secrets lesen, dateien verschieben
from utils import read_file, read_buff                                          # aus unseren utils
################################################################################
models = {
    "meta":   "gpt-4o-mini",                                                    # model für prompt
    "image":  "gpt-image-1-mini",                                               # dall-e-2 | dall-e-3 | gpt-image-1-mini
    "vision": "gpt-4o-mini",                                                    # model für visioning
    "curate": "gpt-4o-mini"                                                     # model für curation
}
#-------------------------------------------------------------------------------
amount = 3                                                                      # anzahl der images
#-------------------------------------------------------------------------------
config = {                                                                      # user einstellung für image
    "chars":                800,                                                # dall-e-2: 1000 | dall-e-3: 4000 | gpt-image-1-mini: 32000
    "background":           "opaque",                                           # only gpt-image-1: opaque | transparent | auto
    "moderation":           "auto",                                             # only gpt-image-1: auto | low
    "n":                    1,                                                  # 1-10; dall-e-3: only 1
    "output_compression":   100,                                                # only gpt-image-1: 0-100
    "output_format":        "png",                                              # only gpt-image-1: png | jpeg | webp
    "partial_images":       None,                                               # only for data stream (deactivated in props)
    "quality":              "medium",                                           # only gpt-image-1: low | medium | high |auto
    "response_format":      "url",                                              # only dall-e: url | b64_json
    "size":                 "1024x1024",                                        # different options per model
    "stream":               None,                                               # only for data stream (deactivated in props)
    "style":                "vivid",                                            # only gpt-image-1: vivid | natural
    "user":                 None,                                               # deactivated in props
}

#-------------------------------------------------------------------------------

async def get_winner(objs: list[Imagen], client: AsyncOpenAI):                  # lässt openai bestes bild auswählen
    msg = [];  ids = []                                                         # inputs initialisieren
    objs = [o for o in objs if o and o.id]                                      # nur mverwenden was vorhanden ist
    for obj in objs:                                                            # durch image objekt instanzen loopen
        buff = obj.buff or read_buff(f"images/{obj.id}.png")                    # aus obj cache ist schneller -> fallback:aus file
        src = f"data:image/png;base64,{buff}"                                   # aber cache aus dem objekt lesen ist schneller
        msg.append({"type":"input_image", "image_url": src})                    # den inputs das aktuelle image hinzufügen
        ids.append(obj.id)                                                      # aktuelle uuid zur uuids liste hinzufügen
    if not ids: raise ValueError("no image ids found")                          # wenn kein score > 0.9, dann keine curation
    prompt = read_file("prompts/curate.md") + str(ids)                          # prompt plus ids für zuordnung per reihenfolge
    msg.insert(0, {"type":"input_text", "text":prompt})                         # nach dem loop: die prompt noch hinzufügen
    res = await client.responses.create(                                        # responses api von openai für das visioning
        model = models["curate"],                                               # gewähltes model angeben
        input = [{"role": "user", "content": msg}],                             # strikt den vorgegeben input übergeben
    ); return res.output_text.strip()                                           # nur returnen was wir brauchen: blanke uuid

#-------------------------------------------------------------------------------
async def run_task(client, config):                                             # führt alles in unserer klasse aus
    try:                                                                        # muss sonst könnten alle tasks failen ($)
        img = Imagen(client, models, config)                                    # objekt zu unserer klasse instanziieren
        result = await img.execute()                                            # alle methods des objektes ausführen
        return img if result else None                                          # objekt returnen, sofern score ok
    except Exception as e: print(e)                                             # falls error: printen
#-------------------------------------------------------------------------------

async def main():                                                               # calls alle funktionen im aktuellen skript
    load_dotenv()                                                               # der runtime zugriff auf .env geben
    client = AsyncOpenAI(api_key=getenv("OPENAI_API_KEY"))                      # async client der openai sdk mit api key
    tasks = [run_task(client, config) for _ in range(amount)]                   # liste aus coroutine funktions objekten
    print(f"generating {amount} images ...")                                    # status info
    candidates = await asyncio.gather(*tasks, return_exceptions=False)          # coroutinen parallel ausführen
    print("curating winner ...")                                                # status info
    winner = await get_winner(candidates, client)                               # gewinner ermitteln
    src_path = f"images/{winner}.png"                                           # pfad wo gewinner gerade liegt
    dst_path = f"winners/{winner}.png"                                          # pfad wo wir gewinner hinschieben wollen
    rename(src_path, dst_path)                                                  # gewinner in winner ordner verschieben
    print(f"winner saved at: {dst_path}")                                       # gewinner pfad printen

#-------------------------------------------------------------------------------

if __name__ == "__main__":                                                      # execution guard
    try: asyncio.run(main())                                                    # try: hauptfunktion asynchron aufrufen
    except Exception as e: print(e)                                             # errors abfangen und printen





