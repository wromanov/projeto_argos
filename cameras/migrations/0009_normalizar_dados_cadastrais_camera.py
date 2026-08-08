from django.db import migrations


CAMPOS_CAIXA_ALTA = (
    "patrimonio",
    "nome",
    "fabricante",
    "modelo",
    "serial",
    "terminal",
    "pavimento",
    "setor",
    "ambiente",
    "ponto_referencia",
    "farm",
    "codec",
)


def normalizar_texto(valor):
    if valor is None:
        return None

    return str(valor).strip().upper()


def verificar_conflitos(cameras):
    patrimonios = {}
    seriais = {}
    nomes_ativos = {}

    for camera in cameras:
        patrimonio = normalizar_texto(
            camera.patrimonio
        )

        serial = normalizar_texto(
            camera.serial
        )

        nome = normalizar_texto(
            camera.nome
        )

        if patrimonio:
            chave = patrimonio.casefold()

            if chave in patrimonios:
                raise RuntimeError(
                    "Conflito de patrimonio apos "
                    "normalizacao entre cameras "
                    f"{patrimonios[chave]} e "
                    f"{camera.pk}."
                )

            patrimonios[chave] = camera.pk

        if serial:
            chave = serial.casefold()

            if chave in seriais:
                raise RuntimeError(
                    "Conflito de numero de serie apos "
                    "normalizacao entre cameras "
                    f"{seriais[chave]} e "
                    f"{camera.pk}."
                )

            seriais[chave] = camera.pk

        if (
            camera.situacao_operacional
            != "DESATIVADA"
        ):
            chave = nome.casefold()

            if chave in nomes_ativos:
                raise RuntimeError(
                    "Conflito de nome ativo apos "
                    "normalizacao entre cameras "
                    f"{nomes_ativos[chave]} e "
                    f"{camera.pk}."
                )

            nomes_ativos[chave] = camera.pk


def normalizar_dados_cadastrais(
    apps,
    schema_editor,
):
    Camera = apps.get_model(
        "cameras",
        "Camera",
    )

    db_alias = schema_editor.connection.alias

    cameras = list(
        Camera.objects
        .using(db_alias)
        .all()
        .order_by("pk")
    )

    # Antes de qualquer escrita, valida se a
    # normalizacao causaria colisao em campos
    # sujeitos a unicidade.
    verificar_conflitos(cameras)

    for camera in cameras:
        atualizacoes = {}

        for campo in CAMPOS_CAIXA_ALTA:
            atual = getattr(
                camera,
                campo,
                None,
            )

            normalizado = normalizar_texto(
                atual
            )

            if (
                campo in ("patrimonio", "serial")
                and normalizado == ""
            ):
                normalizado = None

            if atual != normalizado:
                atualizacoes[campo] = normalizado

        if atualizacoes:
            (
                Camera.objects
                .using(db_alias)
                .filter(pk=camera.pk)
                .update(**atualizacoes)
            )


class Migration(migrations.Migration):

    dependencies = [
        (
            "cameras",
            "0008_substituicaocamera",
        ),
    ]

    operations = [
        migrations.RunPython(
            normalizar_dados_cadastrais,
            migrations.RunPython.noop,
        ),
    ]
