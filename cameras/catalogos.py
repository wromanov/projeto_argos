VALOR_PERSONALIZADO = "__PERSONALIZADO__"


FARMS_CATALOGO = (
    "ESTACIONAMENTO",
    "STVV",
    "ALFANDEGAMENTO",
    "BOLSÃO DE TAXI",
    "TDNA",
    "COANA",
    "FACE X",
    "POC",
)


FARM_CHOICES = (
    ("", "---------"),
    *(
        (valor, valor)
        for valor in FARMS_CATALOGO
    ),
    (
        VALOR_PERSONALIZADO,
        "PERSONALIZADO",
    ),
)

CODECS_CATALOGO = (
    "H.263",
    "H.264",
    "H.265",
    "H.265+",
)


CODEC_CHOICES = (
    ("", "---------"),
    *(
        (valor, valor)
        for valor in CODECS_CATALOGO
    ),
    (
        VALOR_PERSONALIZADO,
        "PERSONALIZADO",
    ),
)
