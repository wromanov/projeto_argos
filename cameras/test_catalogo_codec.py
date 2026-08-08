from django.test import TestCase

from .catalogos import (
    CODEC_CHOICES,
    CODECS_CATALOGO,
    VALOR_PERSONALIZADO,
)
from .forms import CameraEdicaoForm
from .models import Camera


class CatalogoCodecTests(TestCase):
    def criar_camera(self, **kwargs):
        dados = {
            "nome": "CAM-TESTE-CODEC",
            "fabricante": "AXIS",
            "modelo": "P3265",
            "situacao_operacional": (
                Camera.SituacaoOperacional.DESATIVADA
            ),
        }
        dados.update(kwargs)
        return Camera(**dados)

    def dados_formulario(self, **kwargs):
        dados = {
            "nome": "CAM-TESTE-CODEC",
            "fabricante": "AXIS",
            "modelo": "P3265",
            "origem_cadastro": (
                Camera.OrigemCadastro.MANUAL
            ),
            "farm": "STVV",
        }
        dados.update(kwargs)
        return dados

    def test_catalogo_de_codecs_possui_ordem_oficial(self):
        self.assertEqual(
            CODECS_CATALOGO,
            (
                "H.263",
                "H.264",
                "H.265",
                "H.265+",
            ),
        )

    def test_choices_possuem_placeholder_e_personalizado(self):
        self.assertEqual(
            CODEC_CHOICES[0],
            ("", "---------"),
        )

        self.assertEqual(
            CODEC_CHOICES[-1],
            (
                VALOR_PERSONALIZADO,
                "PERSONALIZADO",
            ),
        )

    def test_codec_catalogado_e_normalizado_antes_da_validacao(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                codec="  h.264  ",
            ),
            instance=self.criar_camera(),
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        self.assertEqual(
            form.cleaned_data["codec"],
            "H.264",
        )

    def test_codec_personalizado_e_normalizado(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                codec=VALOR_PERSONALIZADO,
                codec_personalizado=" mjpeg ",
            ),
            instance=self.criar_camera(),
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        self.assertEqual(
            form.cleaned_data["codec"],
            "MJPEG",
        )

    def test_sentinela_personalizado_nao_e_valor_persistivel(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                codec=VALOR_PERSONALIZADO,
                codec_personalizado="personalizado",
            ),
            instance=self.criar_camera(),
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "codec_personalizado",
            form.errors,
        )

    def test_personalizado_exige_valor(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                codec=VALOR_PERSONALIZADO,
                codec_personalizado="   ",
            ),
            instance=self.criar_camera(),
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "codec_personalizado",
            form.errors,
        )

        self.assertIn(
            "Informe o codec personalizado.",
            form.errors["codec_personalizado"],
        )

    def test_codec_legado_e_carregado_como_personalizado(self):
        form = CameraEdicaoForm(
            instance=self.criar_camera(
                codec="H265",
            )
        )

        self.assertEqual(
            form.initial["codec"],
            VALOR_PERSONALIZADO,
        )

        self.assertEqual(
            form.initial["codec_personalizado"],
            "H265",
        )

    def test_codec_catalogado_e_carregado_diretamente(self):
        form = CameraEdicaoForm(
            instance=self.criar_camera(
                codec="H.265",
            )
        )

        self.assertEqual(
            form.initial["codec"],
            "H.265",
        )

        self.assertEqual(
            form.initial["codec_personalizado"],
            "",
        )

    def test_formulario_invalido_preserva_selecao_personalizada(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                codec=VALOR_PERSONALIZADO,
                codec_personalizado="",
            ),
            instance=self.criar_camera(),
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertEqual(
            form["codec"].value(),
            VALOR_PERSONALIZADO,
        )

        self.assertEqual(
            form["codec_personalizado"].value(),
            "",
        )

    def test_save_commit_false_recebe_valor_efetivo_do_codec(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                codec=VALOR_PERSONALIZADO,
                codec_personalizado=" mjpeg ",
            ),
            instance=self.criar_camera(),
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        camera = form.save(
            commit=False
        )

        self.assertEqual(
            camera.codec,
            "MJPEG",
        )

        self.assertNotEqual(
            camera.codec,
            VALOR_PERSONALIZADO,
        )
