from django.test import TestCase

from .forms import CameraEdicaoForm
from .models import Camera


class ValidacaoRedeCameraTests(TestCase):
    def criar_form(
        self,
        *,
        ip="",
        mascara_subrede="",
        gateway="",
        mac="",
    ):
        camera = Camera(
            situacao_operacional=(
                Camera.SituacaoOperacional.DESATIVADA
            )
        )

        return CameraEdicaoForm(
            data={
                "nome": "CAM-VALIDACAO-REDE",
                "fabricante": "AXIS",
                "modelo": "P3265",
                "ip": ip,
                "mascara_subrede": mascara_subrede,
                "gateway": gateway,
                "mac": mac,
                "origem_cadastro": (
                    Camera.OrigemCadastro.MANUAL
                ),
            },
            instance=camera,
        )

    def test_ipv4_validos_sao_aceitos(self):
        casos = (
            "10.10.1.50",
            "192.168.0.254",
            "172.16.10.1",
            "203.0.113.10",
        )

        for ip in casos:
            with self.subTest(ip=ip):
                form = self.criar_form(ip=ip)

                self.assertTrue(
                    form.is_valid(),
                    form.errors.as_json(),
                )

                self.assertEqual(
                    form.cleaned_data["ip"],
                    ip,
                )

    def test_ipv4_invalidos_sao_rejeitados(self):
        casos = (
            "10.10.300.1",
            "192.168.1",
            "abc.def.1.2",
            "10.10.10.10.10",
        )

        for ip in casos:
            with self.subTest(ip=ip):
                form = self.criar_form(ip=ip)

                self.assertFalse(
                    form.is_valid()
                )

                self.assertIn(
                    "ip",
                    form.errors,
                )

    def test_mascara_e_validada_apenas_como_ipv4_sintatico(self):
        form = self.criar_form(
            mascara_subrede="255.0.255.0"
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        self.assertEqual(
            form.cleaned_data["mascara_subrede"],
            "255.0.255.0",
        )

    def test_mascara_ipv4_invalida_e_rejeitada(self):
        form = self.criar_form(
            mascara_subrede="255.255.999.0"
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "mascara_subrede",
            form.errors,
        )

    def test_gateway_ipv4_valido_e_aceito(self):
        form = self.criar_form(
            gateway="203.0.113.254"
        )

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        self.assertEqual(
            form.cleaned_data["gateway"],
            "203.0.113.254",
        )

    def test_gateway_ipv4_invalido_e_rejeitado(self):
        form = self.criar_form(
            gateway="10.20.30.999"
        )

        self.assertFalse(
            form.is_valid()
        )

        self.assertIn(
            "gateway",
            form.errors,
        )

    def test_campos_de_rede_vazios_permanecem_opcionais(self):
        form = self.criar_form()

        self.assertTrue(
            form.is_valid(),
            form.errors.as_json(),
        )

        self.assertEqual(
            form.cleaned_data["ip"],
            "",
        )

        self.assertEqual(
            form.cleaned_data["mascara_subrede"],
            "",
        )

        self.assertEqual(
            form.cleaned_data["gateway"],
            "",
        )

        self.assertIsNone(
            form.cleaned_data["mac"]
        )

    def test_mac_aceita_formatos_suportados_e_canonicaliza(self):
        casos = {
            "aa:bb:cc:dd:ee:ff":
                "AA:BB:CC:DD:EE:FF",
            "aa-bb-cc-dd-ee-ff":
                "AA:BB:CC:DD:EE:FF",
            "aabbccddeeff":
                "AA:BB:CC:DD:EE:FF",
            "aabb.ccdd.eeff":
                "AA:BB:CC:DD:EE:FF",
        }

        for entrada, esperado in casos.items():
            with self.subTest(mac=entrada):
                form = self.criar_form(
                    mac=entrada
                )

                self.assertTrue(
                    form.is_valid(),
                    form.errors.as_json(),
                )

                self.assertEqual(
                    form.cleaned_data["mac"],
                    esperado,
                )

    def test_mac_com_sintaxe_invalida_e_rejeitado(self):
        casos = (
            "GG:BB:CC:DD:EE:FF",
            "AA:BB:CC",
            "12345",
            "AA:BB:CC:DD:EE:GG",
        )

        for mac in casos:
            with self.subTest(mac=mac):
                form = self.criar_form(
                    mac=mac
                )

                self.assertFalse(
                    form.is_valid()
                )

                self.assertIn(
                    "mac",
                    form.errors,
                )
