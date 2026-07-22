# props.py
#-------------------------------------------------------------------------------
# Beschreibt die möglichen Parameter für jedes Image Modell
# Herangehensweise: Standardisierung
# Später im Code soll bei Feldern mit Listen als Values
# der Wert bei Index -1 als Default und Fallback dienen
# Deshalb drehen wir hier z.B. manche Listen hier um
# Wo wir nur None als Value setzen, kennt das Model den Parameter nicht
# 'stream' und 'user' lassen wir absichtlich unberücksichtigt
#-------------------------------------------------------------------------------

props = {

    "dall-e-2":     {
        "chars": list(range(200,1001)),
        "background": None,
        "moderation": None,
        "n": list(range(1,11))[::-1],
        "output_compression": None,
        "output_format": None,
        "partial_images": None,
        "quality": None,
        "response_format": ["url", "b64_json"],
        "size": ["256x256", "512x512", "1024x1024"],
        "stream": None,
        "style": None,
        "user": None,
    },

#-------------------------------------------------------------------------------

    "dall-e-3":     {
        "chars": list(range(200,4001)),
        "background": None,
        "moderation": None,
        "n": [1],
        "output_compression": None,
        "output_format": None,
        "partial_images": None,
        "quality": ["standard", "hd"],
        "response_format": ["url", "b64_json"],
        "size": ["1792x1024", "1024x1792", "1024x1024"],
        "stream": None,
        "style": ["vivid","natural"],
        "user": None,
    },

#-------------------------------------------------------------------------------

    "gpt-image-1-mini":  {
        "chars": list(range(200,32000)),
        "background": ["transparent", "opaque", "auto"],
        "moderation": ["low", "auto"],
        "n": list(range(1,11))[::-1],
        "output_compression": list(range(0,101))[::-1],
        "output_format": ["png", "jpeg", "webp"],
        "partial_images": None,
        "quality": ["low", "medium", "high", "auto"],
        "response_format": None,
        "size": ["auto", "1536x1024", "1024x1536", "1024x1024"],
        "stream": None,
        "style": None,
        "user": None,
    },

#-------------------------------------------------------------------------------

}

props["gpt-image-1"] = props["gpt-image-1-mini"]                            # hinzufügen: key für "gpt-image-1" mit selben props wie "gpt-image-1"-mini



