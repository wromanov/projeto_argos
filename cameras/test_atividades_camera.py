from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import AtividadeCameraForm
from .models import AtividadeCamera, Camera


class AtividadesCameraTests(TestCase):
    def setUp(self):
        self.camera = self.criar_camera()
        self.outra_camera = self.criar_camera("B")
        self.user = get_user_model().objects.create_user(username="operador", password="senha")

    def criar_camera(self, sufixo="A"):
        return Camera.objects.create(nome=f"Camera {sufixo}", fabricante="Axis", modelo="M1", ip=f"10.0.0.{1 if sufixo == 'A' else 2}", mascara_subrede="255.255.255.0", vlan=100, patrimonio=f"PAT-{sufixo}")

    def dados(self, **extra):
        data = {"tipo": "AVARIA", "titulo": "Falha de imagem", "descricao": "Câmera sem imagem no monitoramento.", "ocorrida_em": "2026-07-31T10:30", "responsavel": "Equipe técnica"}
        data.update(extra)
        return data

    def atividade(self, camera=None, **extra):
        data = {"camera": camera or self.camera, "tipo": "AVARIA", "titulo": "Atividade", "descricao": "Descrição completa", "ocorrida_em": timezone.now(), "responsavel": "Equipe"}
        data.update(extra)
        return AtividadeCamera.objects.create(**data)

    def test_criacao_atividade_valida(self): self.assertEqual(self.atividade().tipo, "AVARIA")
    def test_str_da_atividade(self): self.assertIn("Avaria identificada", str(self.atividade()))
    def test_relacionamento_com_camera(self): self.assertEqual(self.camera.atividades.count(), 1) if self.atividade() else None
    def test_descricao_do_tipo(self): self.assertEqual(self.atividade().get_tipo_display(), "Avaria identificada")
    def test_ordenacao_mais_recente_primeiro(self):
        antiga = self.atividade(ocorrida_em=timezone.now()-timedelta(days=1)); nova = self.atividade(titulo="Nova", ocorrida_em=timezone.now()); self.assertEqual(AtividadeCamera.objects.first(), nova)
    def test_camera_com_atividade_nao_pode_ser_excluida(self):
        self.atividade()
        with self.assertRaises(ProtectedError):
            self.camera.delete()

    def test_formulario_valido(self): self.assertTrue(AtividadeCameraForm(self.dados()).is_valid())
    def test_descricao_obrigatoria(self): self.assertFalse(AtividadeCameraForm(self.dados(descricao="")).is_valid())
    def test_camera_nao_esta_no_formulario(self): self.assertNotIn("camera", AtividadeCameraForm().fields)
    def test_governanca_nao_esta_no_formulario(self): self.assertFalse({"criado_por","criado_em","atualizado_por","atualizado_em"}.intersection(AtividadeCameraForm().fields))
    def test_datetime_local_valido(self): self.assertTrue(AtividadeCameraForm(self.dados(ocorrida_em="2026-07-31T10:30")).is_valid())

    def test_pagina_criacao_retorna_200(self): self.assertEqual(self.client.get(reverse("cameras:criar_atividade", args=[self.camera.pk])).status_code, 200)
    def test_pagina_criacao_mostra_camera(self): self.assertContains(self.client.get(reverse("cameras:criar_atividade", args=[self.camera.pk])), self.camera.nome)
    def test_criacao_valida(self):
        response = self.client.post(reverse("cameras:criar_atividade", args=[self.camera.pk]), self.dados()); self.assertRedirects(response, reverse("cameras:detalhe", args=[self.camera.pk])); self.assertEqual(self.camera.atividades.count(), 1)
    def test_criacao_vincula_camera_da_url(self):
        self.client.post(reverse("cameras:criar_atividade", args=[self.camera.pk]), self.dados()); self.assertEqual(AtividadeCamera.objects.get().camera, self.camera)
    def test_criacao_camera_inexistente_retorna_404(self): self.assertEqual(self.client.get(reverse("cameras:criar_atividade", args=[99999])).status_code, 404)
    def test_criacao_preenche_governanca(self):
        self.client.force_login(self.user); self.client.post(reverse("cameras:criar_atividade", args=[self.camera.pk]), self.dados()); atividade=AtividadeCamera.objects.get(); self.assertEqual(atividade.criado_por, self.user); self.assertEqual(atividade.atualizado_por, self.user)

    def test_pagina_edicao_retorna_200(self): self.assertEqual(self.client.get(reverse("cameras:editar_atividade", args=[self.atividade().pk])).status_code, 200)
    def test_edicao_atualiza_registro(self):
        atividade=self.atividade(); self.client.post(reverse("cameras:editar_atividade", args=[atividade.pk]), self.dados(titulo="Atualizada")); atividade.refresh_from_db(); self.assertEqual(atividade.titulo,"Atualizada")
    def test_edicao_nao_cria_novo_registro(self):
        atividade=self.atividade(); self.client.post(reverse("cameras:editar_atividade", args=[atividade.pk]), self.dados()); self.assertEqual(AtividadeCamera.objects.count(),1)
    def test_edicao_preserva_camera(self):
        atividade=self.atividade(); self.client.post(reverse("cameras:editar_atividade", args=[atividade.pk]), self.dados()); atividade.refresh_from_db(); self.assertEqual(atividade.camera,self.camera)
    def test_edicao_preserva_criado_por(self):
        atividade=self.atividade(criado_por=self.user); self.client.post(reverse("cameras:editar_atividade", args=[atividade.pk]), self.dados()); atividade.refresh_from_db(); self.assertEqual(atividade.criado_por,self.user)
    def test_edicao_atualiza_atualizado_por(self):
        atividade=self.atividade(); self.client.force_login(self.user); self.client.post(reverse("cameras:editar_atividade", args=[atividade.pk]), self.dados()); atividade.refresh_from_db(); self.assertEqual(atividade.atualizado_por,self.user)
    def test_edicao_inexistente_retorna_404(self): self.assertEqual(self.client.get(reverse("cameras:editar_atividade", args=[99999])).status_code,404)

    def test_detalhe_camera_exibe_atividade(self):
        atividade = self.atividade()
        response = self.client.get(reverse("cameras:detalhe", args=[self.camera.pk]))
        self.assertContains(response, atividade.titulo)

    def test_detalhe_camera_nao_exibe_atividade_de_outra_camera(self): self.atividade(self.outra_camera,titulo="Exclusiva"); self.assertNotContains(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])),"Exclusiva")
    def test_detalhe_camera_limita_dez_atividades(self):
        for i in range(11): self.atividade(titulo=f"Atividade {i}")
        response=self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])); self.assertContains(response,"Atividade 10"); self.assertNotContains(response,"Atividade 0")
    def test_link_registrar_atividade_usa_camera_correta(self): self.assertContains(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])),reverse("cameras:criar_atividade",args=[self.camera.pk]))
    def test_link_historico_usa_camera_correta(self): self.assertContains(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])),reverse("cameras:lista_atividades",args=[self.camera.pk]))
    def test_link_editar_usa_atividade_correta(self):
        atividade=self.atividade(); self.assertContains(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])),reverse("cameras:editar_atividade",args=[atividade.pk]))
    def test_estado_vazio_no_detalhe(self): self.assertContains(self.client.get(reverse("cameras:detalhe",args=[self.camera.pk])),"Nenhuma atividade registrada para esta câmera.")

    def test_historico_retorna_200(self): self.assertEqual(self.client.get(reverse("cameras:lista_atividades",args=[self.camera.pk])).status_code,200)
    def test_historico_lista_atividades_da_camera(self):
        atividade = self.atividade()
        response = self.client.get(reverse("cameras:lista_atividades", args=[self.camera.pk]))
        self.assertContains(response, atividade.titulo)

    def test_historico_nao_lista_atividade_de_outra_camera(self): self.atividade(self.outra_camera,titulo="Outra atividade"); self.assertNotContains(self.client.get(reverse("cameras:lista_atividades",args=[self.camera.pk])),"Outra atividade")
    def test_historico_ordenado_por_data(self):
        self.atividade(titulo="Antiga",ocorrida_em=timezone.now()-timedelta(days=1)); self.atividade(titulo="Nova",ocorrida_em=timezone.now()); response=self.client.get(reverse("cameras:lista_atividades",args=[self.camera.pk])); self.assertLess(response.content.find(b"Nova"),response.content.find(b"Antiga"))
    def test_historico_pagina_acima_de_vinte(self):
        for i in range(21): self.atividade(titulo=f"Registro {i}")
        response=self.client.get(reverse("cameras:lista_atividades",args=[self.camera.pk]),{"page":2}); self.assertEqual(len(response.context["atividades"]),1)
    def test_historico_pagina_invalida_nao_falha(self): self.assertEqual(self.client.get(reverse("cameras:lista_atividades",args=[self.camera.pk]),{"page":"invalida"}).status_code,200)
    def test_historico_camera_inexistente_retorna_404(self): self.assertEqual(self.client.get(reverse("cameras:lista_atividades",args=[99999])).status_code,404)
    def test_historico_exibe_total(self): self.atividade(); self.assertContains(self.client.get(reverse("cameras:lista_atividades",args=[self.camera.pk])),"1 registro")