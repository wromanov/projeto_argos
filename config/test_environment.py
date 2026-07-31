import os
from unittest import TestCase
from unittest.mock import patch
from django.core.exceptions import ImproperlyConfigured
from .environment import get_env_bool, get_env_int, get_env_list, get_required_env, get_required_secret


class EnvironmentTests(TestCase):
    def test_env_bool_true(self):
        with patch.dict(os.environ,{"X":"true"}): self.assertTrue(get_env_bool("X",False))
    def test_env_bool_false(self):
        with patch.dict(os.environ,{"X":"false"}): self.assertFalse(get_env_bool("X",True))
    def test_env_bool_aceita_sim(self):
        with patch.dict(os.environ,{"X":"sim"}): self.assertTrue(get_env_bool("X",False))
    def test_env_bool_aceita_nao(self):
        with patch.dict(os.environ,{"X":"não"}): self.assertFalse(get_env_bool("X",True))
    def test_env_bool_rejeita_valor_invalido(self):
        with patch.dict(os.environ,{"X":"talvez"}), self.assertRaises(ImproperlyConfigured): get_env_bool("X",False)
    def test_env_int_valido(self):
        with patch.dict(os.environ,{"X":"10"}): self.assertEqual(get_env_int("X",1),10)
    def test_env_int_rejeita_texto(self):
        with patch.dict(os.environ,{"X":"texto"}), self.assertRaises(ImproperlyConfigured): get_env_int("X",1)
    def test_env_int_respeita_minimo(self):
        with patch.dict(os.environ,{"X":"1"}), self.assertRaises(ImproperlyConfigured): get_env_int("X",5,minimum=2)
    def test_env_list_separa_e_remove_espacos(self):
        with patch.dict(os.environ,{"X":" a, b ,,c "}): self.assertEqual(get_env_list("X"),["a","b","c"])
    def test_required_env_rejeita_ausente(self):
        with patch.dict(os.environ,{},clear=True), self.assertRaises(ImproperlyConfigured): get_required_env("X")
    def test_required_secret_rejeita_valor_curto(self):
        with patch.dict(os.environ,{"X":"curto"}), self.assertRaises(ImproperlyConfigured): get_required_secret("X")
    def test_required_secret_nao_expoe_valor_no_erro(self):
        segredo="segredo-curto"
        with patch.dict(os.environ,{"X":segredo}):
            try: get_required_secret("X")
            except ImproperlyConfigured as exc: self.assertNotIn(segredo,str(exc))
