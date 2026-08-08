from django.test import TestCase

from .forms import CameraEdicaoForm
from .models import Camera
from .validadores import normalizar_texto_cadastral


class NormalizacaoTextoCadastralTests(TestCase):
    def test_none_permanece_none(self):
        self.assertIsNone(
            normalizar_texto_cadastral(None)
        )

    def test_remove_espacos_e_converte_para_caixa_alta(self):
        self.assertEqual(
            normalizar_texto_cadastral(
                "  Axis Communications  "
            ),
            "AXIS COMMUNICATIONS",
        )

    def test_preserva_acentos_ao_converter_para_caixa_alta(self):
        self.assertEqual(
            normalizar_texto_cadastral(
                "Bols?o de Taxi"
            ),
            "BOLS?O DE TAXI",
        )


class NormalizacaoCameraModeloTests(TestCase):
    def test_save_normaliza_campos_estruturados(self):
        camera = Camera.objects.create(
            patrimonio=" pat-001 ",
            nome=" cam-tps2-01 ",
            fabricante=" Axis ",
            modelo=" p3265-lve ",
            serial=" ser-001 ",
            terminal=" tps2 ",
            pavimento=" t?rreo ",
            setor=" desembarque ",
            ambiente=" sagu?o ",
            ponto_referencia=" porta a ",
            farm=" stvv ",
            codec=" h.264 ",
        )

        camera.refresh_from_db()

        esperados = {
            "patrimonio": "PAT-001",
            "nome": "CAM-TPS2-01",
            "fabricante": "AXIS",
            "modelo": "P3265-LVE",
            "serial": "SER-001",
            "terminal": "TPS2",
            "pavimento": "T?RREO",
            "setor": "DESEMBARQUE",
            "ambiente": "SAGU?O",
            "ponto_referencia": "PORTA A",
            "farm": "STVV",
            "codec": "H.264",
        }

        for campo, esperado in esperados.items():
            with self.subTest(campo=campo):
                self.assertEqual(
                    getattr(camera, campo),
                    esperado,
                )

    def test_save_preserva_campos_narrativos(self):
        descricao = (
            "C?mera instalada acima da porta principal."
        )
        observacoes = (
            "Validar posicionamento ap?s manuten??o."
        )

        camera = Camera.objects.create(
            nome="cam-narrativa",
            fabricante="axis",
            modelo="p3265",
            descricao_detalhada=descricao,
            observacoes=observacoes,
        )

        camera.refresh_from_db()

        self.assertEqual(
            camera.descricao_detalhada,
            descricao,
        )

        self.assertEqual(
            camera.observacoes,
            observacoes,
        )

    def test_patrimonio_e_serial_vazios_sao_none(self):
        camera = Camera.objects.create(
            nome="cam-vazios",
            fabricante="axis",
            modelo="p3265",
            patrimonio="   ",
            serial="   ",
        )

        camera.refresh_from_db()

        self.assertIsNone(
            camera.patrimonio
        )

        self.assertIsNone(
            camera.serial
        )

    def test_save_com_update_fields_normaliza_apenas_campos_salvos(self):
        camera = Camera.objects.create(
            nome="cam-update-fields",
            fabricante="axis",
            modelo="p3265",
        )

        camera.nome = "  novo nome  "
        camera.fabricante = " fabricante temporario "

        camera.save(
            update_fields=["nome"]
        )

        self.assertEqual(
            camera.nome,
            "NOVO NOME",
        )

        self.assertEqual(
            camera.fabricante,
            " fabricante temporario ",
        )

        camera.refresh_from_db()

        self.assertEqual(
            camera.nome,
            "NOVO NOME",
        )

        self.assertEqual(
            camera.fabricante,
            "AXIS",
        )


class NormalizacaoCameraFormularioTests(TestCase):
    def test_form_normaliza_antes_da_persistencia(self):
        camera = Camera.objects.create(
            nome="CAM-FORM-01",
            fabricante="AXIS",
            modelo="P3265",
            situacao_operacional=(
                Camera.SituacaoOperacional.DESATIVADA
            ),
        )

        descricao = (
            "C?mera instalada acima da porta."
        )

        observacoes = (
            "Validar novamente ap?s manuten??o."
        )

        form = CameraEdicaoForm(
            data={
                "patrimonio": "   ",
                "nome": "  cam-form-01  ",
                "fabricante": "  axis  ",
                "modelo": "  p3265-lve  ",
                "serial": "   ",
                "terminal": "  tps2  ",
                "pavimento": "  t?rreo  ",
                "setor": "  desembarque  ",
                "ambiente": "  sagu?o  ",
                "ponto_referencia": "  porta a  ",
                "farm": "  stvv  ",
                "codec": "  h.264  ",
                "descricao_detalhada": descricao,
                "observacoes": observacoes,
                "origem_cadastro": (
                    Camera.OrigemCadastro.MANUAL
                ),
            },
            instance=camera,
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        esperados = {
            "nome": "CAM-FORM-01",
            "fabricante": "AXIS",
            "modelo": "P3265-LVE",
            "terminal": "TPS2",
            "pavimento": "T?RREO",
            "setor": "DESEMBARQUE",
            "ambiente": "SAGU?O",
            "ponto_referencia": "PORTA A",
            "farm": "STVV",
            "codec": "H.264",
        }

        for campo, esperado in esperados.items():
            with self.subTest(campo=campo):
                self.assertEqual(
                    form.cleaned_data[campo],
                    esperado,
                )

        self.assertIsNone(
            form.cleaned_data["patrimonio"]
        )

        self.assertIsNone(
            form.cleaned_data["serial"]
        )

        self.assertEqual(
            form.cleaned_data[
                "descricao_detalhada"
            ],
            descricao,
        )

        self.assertEqual(
            form.cleaned_data["observacoes"],
            observacoes,
        )

        # A inst?ncia j? precisa estar normalizada
        # antes do save, pois a auditoria compara
        # os valores neste est?gio.
        self.assertEqual(
            camera.nome,
            "CAM-FORM-01",
        )

        self.assertEqual(
            camera.fabricante,
            "AXIS",
        )

        self.assertEqual(
            camera.farm,
            "STVV",
        )
