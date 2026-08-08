from django.test import TestCase

from .catalogos import (
    FARM_CHOICES,
    FARMS_CATALOGO,
    VALOR_PERSONALIZADO,
)
from .forms import CameraEdicaoForm
from .models import Camera


class CatalogoFarmTests(TestCase):
    def criar_camera(self, **kwargs):
        dados = {
            "nome": "CAM-TESTE-FARM",
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
            "nome": "CAM-TESTE-FARM",
            "fabricante": "AXIS",
            "modelo": "P3265",
            "origem_cadastro": (
                Camera.OrigemCadastro.MANUAL
            ),
        }
        dados.update(kwargs)
        return dados

    def test_catalogo_de_farms_possui_ordem_oficial(self):
        self.assertEqual(
            FARMS_CATALOGO,
            (
                "ESTACIONAMENTO",
                "STVV",
                "ALFANDEGAMENTO",
                "BOLS\u00c3O DE TAXI",
                "TDNA",
                "COANA",
                "FACE X",
                "POC",
            ),
        )

    def test_choices_possuem_placeholder_e_personalizado(self):
        self.assertEqual(
            FARM_CHOICES[0],
            ("", "---------"),
        )

        self.assertEqual(
            FARM_CHOICES[-1],
            (
                VALOR_PERSONALIZADO,
                "PERSONALIZADO",
            ),
        )

    def test_farm_catalogada_e_aceita(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                farm="STVV",
                farm_personalizado="",
            ),
            instance=self.criar_camera(),
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        self.assertEqual(
            form.cleaned_data["farm"],
            "STVV",
        )

    def test_farm_personalizada_e_normalizada(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                farm=VALOR_PERSONALIZADO,
                farm_personalizado=" farm-tps2-02 ",
            ),
            instance=self.criar_camera(),
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        self.assertEqual(
            form.cleaned_data["farm"],
            "FARM-TPS2-02",
        )

    def test_sentinela_personalizado_nao_e_valor_persistivel(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                farm=VALOR_PERSONALIZADO,
                farm_personalizado="personalizado",
            ),
            instance=self.criar_camera(),
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "farm_personalizado",
            form.errors,
        )

    def test_personalizado_exige_valor(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                farm=VALOR_PERSONALIZADO,
                farm_personalizado="   ",
            ),
            instance=self.criar_camera(),
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "farm_personalizado",
            form.errors,
        )

        self.assertIn(
            "Informe a farm personalizada.",
            form.errors["farm_personalizado"],
        )

    def test_farm_legada_e_carregada_como_personalizada(self):
        form = CameraEdicaoForm(
            instance=self.criar_camera(
                farm="FARM-TPS2-02",
            )
        )

        self.assertEqual(
            form.initial["farm"],
            VALOR_PERSONALIZADO,
        )

        self.assertEqual(
            form.initial["farm_personalizado"],
            "FARM-TPS2-02",
        )

    def test_farm_catalogada_e_carregada_diretamente(self):
        form = CameraEdicaoForm(
            instance=self.criar_camera(
                farm="STVV",
            )
        )

        self.assertEqual(
            form.initial["farm"],
            "STVV",
        )

        self.assertEqual(
            form.initial["farm_personalizado"],
            "",
        )

    def test_formulario_invalido_preserva_selecao_personalizada(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                farm=VALOR_PERSONALIZADO,
                farm_personalizado="",
            ),
            instance=self.criar_camera(),
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertEqual(
            form["farm"].value(),
            VALOR_PERSONALIZADO,
        )

        self.assertEqual(
            form["farm_personalizado"].value(),
            "",
        )

    def test_save_commit_false_recebe_valor_efetivo_da_farm(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                farm=VALOR_PERSONALIZADO,
                farm_personalizado=" farm-legado-01 ",
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
            camera.farm,
            "FARM-LEGADO-01",
        )

        self.assertNotEqual(
            camera.farm,
            VALOR_PERSONALIZADO,
        )
