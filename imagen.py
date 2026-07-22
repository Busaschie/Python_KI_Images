# imagen.py
################################################################################
from uuid import uuid4  # erzeugt eindeutige IDs
from copy import deepcopy  # erstellt kopien von objekten
from props import props  # lädt mdell-parameter
from utils import read_file, write_buff  # datei-hlfsfunktionen
from openai import AsyncOpenAI  # openAI client
from openai.types import ImagesResponse as ImgResp  # typ für bildantworten
################################################################################

class Imagen:

    # --------------------------------------------------------------------------
    def __init__(self, client, models, config):
        self.id = str(uuid4())  # generiert eindeutige bild-ID
        self.client: AsyncOpenAI = client  # speichert openai client
        self.mod = deepcopy(models)  # kopiert modellkonfiguration
        self.cfg = deepcopy(config)  # kopiert config
        self.prop = props[models["image"]]  # lädt modell-spezifische props
        self.prompt = ""  # initialisiert prompt
        self.buff = None  # initialisiert bilddaten

    # --------------------------------------------------------------------------
    async def set_prompt(self, path, chars):
        meta = read_file(path).replace("__imod__", self.mod["meta"])  # lädt prompt-template
        res = await self.client.responses.create(  # sendet anfrage an openai
            model=self.mod["meta"],  # nutzt modell für metaprompt
            input=meta.replace("__chars__", str(chars))  # dynamisch platzhalter in prompt ersetzen
        );
        self.prompt = res.output_text[:chars]  # speichert gekürzten prompt

    # --------------------------------------------------------------------------
    async def set_config(self):
        c = {"model": self.mod["image"], "prompt": self.prompt}  # basis-konfiguration
        for k, v in self.prop.items():  # iteriert über erlaubte parameter
            if v is None or k == "chars":
                continue  # überspringt ungültige keys
            elif self.cfg.get(k) not in v:
                c[k] = v[-1]  # setzt default wenn ungültig
            else:
                c[k] = self.cfg[k]  # übernimmt gültigen wert
        self.cfg = c  # speichert finale config

    # --------------------------------------------------------------------------
    async def get_image(self):
        res: ImgResp = await self.client.images.generate(**self.cfg)  # generiert bild
        self.buff = write_buff(f"images/{self.id}.png", res.data[0].b64_json)  # speichert bild als datei
        print(f"new image saved at: images/{self.id}.png")  # ausgabe

    # --------------------------------------------------------------------------
    async def get_score(self):
        txt = read_file("prompts/vision.md").replace("__ref__", self.prompt)  # lädt bewertungs-prompt
        src = f"data:image/png;base64,{self.buff}"  # kodiert bild
        c1 = {"type": "input_text", "text": txt}  # visioning prompt message
        c2 = {"type": "input_image", "image_url": src}  # bildinput
        res = await self.client.responses.create(  # sendet an vision-modell
            model=self.mod["vision"],  # modell für visioning zuweisen
            input=[{"role": "user", "content": [c1, c2]}]  # inputs übergeben
        )
        try:
            return 0.9 <= float(res.output_text) <= 1  # prüft score >= 0.9
        except:
            return False  # fehler => ungültig

    # --------------------------------------------------------------------------

    async def execute(self):
        await self.set_prompt("prompts/meta.md", self.cfg["chars"])  # erstellt prompt
        await self.set_config()  # setzt config
        await self.get_image()  # generiert bild
        return await self.get_score()  # bewertet bild




