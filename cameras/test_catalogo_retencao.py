from django.test import TestCase

from .catalogos import (
    RETENCAO_CHOICES,
    RETENCOES_CATALOGO,
    VALOR_PERSONALIZADO,
)
from .forms import CameraEdicaoForm
from .models import Camera


class CatalogoRetencaoTests(TestCase):
    def criar_camera(self, **kwargs):
        dados = {
            "nome": "CAM-TESTE-RETENCAO",
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
            "nome": "CAM-TESTE-RETENCAO",
            "fabricante": "AXIS",
            "modelo": "P3265",
            "origem_cadastro": (
                Camera.OrigemCadastro.MANUAL
            ),
            "farm": "STVV",
            "codec": "H.264",
        }
        dados.update(kwargs)
        return dados

    def test_catalogo_de_retencoes_possui_ordem_oficial(self):
        self.assertEqual(
            RETENCOES_CATALOGO,
            (
                15,
                30,
                90,
                180,
                360,
                540,
            ),
        )

    def test_choices_possuem_placeholder_e_personalizado(self):
        self.assertEqual(
            RETENCAO_CHOICES[0],
            ("", "---------"),
        )

        self.assertEqual(
            RETENCAO_CHOICES[-1],
            (
                VALOR_PERSONALIZADO,
                "PERSONALIZADO",
            ),
        )

    def test_retencao_catalogada_e_convertida_para_inteiro(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                retencao_esperada_dias="30",
            ),
            instance=self.criar_camera(),
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        self.assertEqual(
            form.cleaned_data["retencao_esperada_dias"],
            30,
        )

        self.assertIsInstance(
            form.cleaned_data["retencao_esperada_dias"],
            int,
        )

    def test_retencao_personalizada_positiva_e_aceita(self):
        for valor in (365, 1000):
            with self.subTest(valor=valor):
                form = CameraEdicaoForm(
                    data=self.dados_formulario(
                        retencao_esperada_dias=(
                            VALOR_PERSONALIZADO
                        ),
                        retencao_personalizada_dias=str(
                            valor
                        ),
                    ),
                    instance=self.criar_camera(),
                )

                self.assertTrue(
                    form.is_valid(),
                    form.errors.as_json(),
                )

                self.assertEqual(
                    form.cleaned_data[
                        "retencao_esperada_dias"
                    ],
                    valor,
                )

    def test_retencao_personalizada_exige_valor(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                retencao_esperada_dias=(
                    VALOR_PERSONALIZADO
                ),
                retencao_personalizada_dias="",
            ),
            instance=self.criar_camera(),
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "retencao_personalizada_dias",
            form.errors,
        )

        self.assertIn(
            (
                "Informe a reten\u00e7\u00e3o "
                "personalizada em dias."
            ),
            form.errors[
                "retencao_personalizada_dias"
            ],
        )

    def test_retencao_personalizada_rejeita_valor_nao_positivo(self):
        for valor in ("0", "-10"):
            with self.subTest(valor=valor):
                form = CameraEdicaoForm(
                    data=self.dados_formulario(
                        retencao_esperada_dias=(
                            VALOR_PERSONALIZADO
                        ),
                        retencao_personalizada_dias=valor,
                    ),
                    instance=self.criar_camera(),
                )

                self.assertFalse(
                    form.is_valid()
                )

                self.assertIn(
                    "retencao_personalizada_dias",
                    form.errors,
                )

    def test_retencao_catalogada_e_carregada_diretamente(self):
        form = CameraEdicaoForm(
            instance=self.criar_camera(
                retencao_esperada_dias=30,
            )
        )

        self.assertEqual(
            form.initial["retencao_esperada_dias"],
            "30",
        )

        self.assertEqual(
            form.initial["retencao_personalizada_dias"],
            "",
        )

    def test_retencao_fora_do_catalogo_e_carregada_como_personalizada(self):
        form = CameraEdicaoForm(
            instance=self.criar_camera(
                retencao_esperada_dias=365,
            )
        )

        self.assertEqual(
            form.initial["retencao_esperada_dias"],
            VALOR_PERSONALIZADO,
        )

        self.assertEqual(
            form.initial["retencao_personalizada_dias"],
            365,
        )

    def test_formulario_invalido_preserva_selecao_personalizada(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                retencao_esperada_dias=(
                    VALOR_PERSONALIZADO
                ),
                retencao_personalizada_dias="",
            ),
            instance=self.criar_camera(),
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertEqual(
            form["retencao_esperada_dias"].value(),
            VALOR_PERSONALIZADO,
        )

        self.assertEqual(
            form["retencao_personalizada_dias"].value(),
            "",
        )

    def test_save_commit_false_recebe_retencao_efetiva(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                retencao_esperada_dias=(
                    VALOR_PERSONALIZADO
                ),
                retencao_personalizada_dias="365",
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
            camera.retencao_esperada_dias,
            365,
        )

        self.assertIsInstance(
            camera.retencao_esperada_dias,
            int,
        )
