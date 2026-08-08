from django.test import TestCase

from .catalogos import VALOR_PERSONALIZADO
from .forms import CameraEdicaoForm
from .models import Camera


class CompatibilidadeCadastralTests(TestCase):
    def criar_camera(self, **kwargs):
        dados = {
            "nome": "CAM-COMPATIBILIDADE",
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
            "nome": "CAM-COMPATIBILIDADE",
            "fabricante": "AXIS",
            "modelo": "P3265",
            "origem_cadastro": (
                Camera.OrigemCadastro.MANUAL
            ),
        }
        dados.update(kwargs)

        return dados

    def test_model_preserva_valores_legados_fora_dos_catalogos(self):
        camera = Camera.objects.create(
            nome="CAM-LEGADA-MODEL",
            fabricante="AXIS",
            modelo="P3265",
            farm="FARM-LEGADA-01",
            codec="H265",
            retencao_esperada_dias=365,
            situacao_operacional=(
                Camera.SituacaoOperacional.DESATIVADA
            ),
        )

        camera.refresh_from_db()

        self.assertEqual(
            camera.farm,
            "FARM-LEGADA-01",
        )

        self.assertEqual(
            camera.codec,
            "H265",
        )

        self.assertEqual(
            camera.retencao_esperada_dias,
            365,
        )

    def test_formulario_mapeia_tres_valores_legados_para_personalizado(
        self,
    ):
        form = CameraEdicaoForm(
            instance=self.criar_camera(
                farm="FARM-TPS2-02",
                codec="H265",
                retencao_esperada_dias=365,
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

        self.assertEqual(
            form.initial["codec"],
            VALOR_PERSONALIZADO,
        )

        self.assertEqual(
            form.initial["codec_personalizado"],
            "H265",
        )

        self.assertEqual(
            form.initial["retencao_esperada_dias"],
            VALOR_PERSONALIZADO,
        )

        self.assertEqual(
            form.initial["retencao_personalizada_dias"],
            365,
        )

    def test_formulario_preserva_valores_legados_ao_salvar(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                farm=VALOR_PERSONALIZADO,
                farm_personalizado="FARM-TPS2-02",
                codec=VALOR_PERSONALIZADO,
                codec_personalizado="H265",
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
            camera.farm,
            "FARM-TPS2-02",
        )

        self.assertEqual(
            camera.codec,
            "H265",
        )

        self.assertEqual(
            camera.retencao_esperada_dias,
            365,
        )

        self.assertNotEqual(
            camera.farm,
            VALOR_PERSONALIZADO,
        )

        self.assertNotEqual(
            camera.codec,
            VALOR_PERSONALIZADO,
        )

    def test_valores_catalogados_permanecem_catalogados(self):
        form = CameraEdicaoForm(
            instance=self.criar_camera(
                farm="STVV",
                codec="H.265",
                retencao_esperada_dias=30,
            )
        )

        self.assertEqual(
            form.initial["farm"],
            "STVV",
        )

        self.assertEqual(
            form.initial["codec"],
            "H.265",
        )

        self.assertEqual(
            form.initial["retencao_esperada_dias"],
            "30",
        )

        self.assertEqual(
            form.initial["farm_personalizado"],
            "",
        )

        self.assertEqual(
            form.initial["codec_personalizado"],
            "",
        )

        self.assertEqual(
            form.initial["retencao_personalizada_dias"],
            "",
        )

    def test_campos_de_gravacao_vazios_permanecem_opcionais(self):
        form = CameraEdicaoForm(
            data=self.dados_formulario(
                farm="",
                codec="",
                retencao_esperada_dias="",
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
            "",
        )

        self.assertEqual(
            camera.codec,
            "",
        )

        self.assertIsNone(
            camera.retencao_esperada_dias,
        )
