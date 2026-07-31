from io import StringIO

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .admin import PerfilUsuarioAdmin
from .forms import DadosPessoaisForm, PerfilProprioForm
from .models import PerfilUsuario
from .templatetags.usuarios_extras import iniciais_usuario


class PerfilUsuarioTests(TestCase):
    def setUp(self):
        self.user=get_user_model().objects.create_user(username="walace",password="Senha-forte-123",first_name="Walace",last_name="Castro",email="WALACE@EXAMPLE.COM")
        self.perfil=self.user.perfil
        self.client.force_login(self.user)
    def dados(self,**extra):
        dados={"first_name":"Novo","last_name":"Nome","email":"NOVO@EXAMPLE.COM","telefone":" 11999990000 ","ramal":" 123 "}; dados.update(extra); return dados
    def test_criacao_perfil_valida(self): self.assertEqual(self.perfil.usuario,self.user)
    def test_str_do_perfil(self): self.assertEqual(str(self.perfil),"Walace Castro")
    def test_relacionamento_um_para_um(self): self.assertEqual(self.user.perfil.pk,self.perfil.pk)
    def test_campos_opcionais_iniciam_vazios(self): self.assertEqual((self.perfil.telefone,self.perfil.ramal,self.perfil.cargo,self.perfil.setor),("","","",""))
    def test_timestamps_do_perfil(self): self.assertTrue(self.perfil.criado_em and self.perfil.atualizado_em)
    def test_novo_usuario_recebe_perfil(self): self.assertTrue(get_user_model().objects.create_user(username="novo").perfil)
    def test_salvar_usuario_nao_duplica_perfil(self): self.user.save(); self.assertEqual(PerfilUsuario.objects.filter(usuario=self.user).count(),1)
    def test_excluir_usuario_exclui_perfil(self): pk=self.perfil.pk; self.user.delete(); self.assertFalse(PerfilUsuario.objects.filter(pk=pk).exists())
    def test_form_dados_pessoais_possui_campos_corretos(self): self.assertEqual(list(DadosPessoaisForm().fields),["first_name","last_name","email"])
    def test_form_dados_pessoais_nao_expoe_campos_privilegiados(self): self.assertFalse({"username","password","is_staff","is_superuser","groups","user_permissions"}&set(DadosPessoaisForm().fields))
    def test_nome_e_sobrenome_sao_obrigatorios(self): self.assertFalse(DadosPessoaisForm({"first_name":" ","last_name":" ","email":"a@b.com"}).is_valid())
    def test_email_e_obrigatorio_e_valido(self): self.assertFalse(DadosPessoaisForm({"first_name":"A","last_name":"B","email":"invalido"}).is_valid())
    def test_form_dados_pessoais_normaliza_textos(self):
        f=DadosPessoaisForm({"first_name":" A ","last_name":" B ","email":" A@B.COM "}); self.assertTrue(f.is_valid()); self.assertEqual((f.cleaned_data["first_name"],f.cleaned_data["last_name"],f.cleaned_data["email"]),("A","B","a@b.com"))
    def test_form_perfil_possui_telefone_e_ramal(self): self.assertEqual(list(PerfilProprioForm().fields),["telefone","ramal"])
    def test_form_perfil_nao_expoe_cargo_e_setor(self): self.assertFalse({"cargo","setor"}&set(PerfilProprioForm().fields))
    def test_form_perfil_remove_espacos_externos(self): f=PerfilProprioForm({"telefone":" 11 ","ramal":" 22 "}); self.assertTrue(f.is_valid()); self.assertEqual((f.cleaned_data["telefone"],f.cleaned_data["ramal"]),("11","22"))
    def test_perfil_anonimo_redireciona_para_login(self): self.client.logout(); self.assertRedirects(self.client.get(reverse("usuarios:perfil")),"/login/?next=/perfil/",fetch_redirect_response=False)
    def test_perfil_autenticado_retorna_200(self): self.assertEqual(self.client.get(reverse("usuarios:perfil")).status_code,200)
    def test_perfil_usa_template_correto(self): self.assertTemplateUsed(self.client.get(reverse("usuarios:perfil")),"usuarios/perfil.html")
    def test_perfil_exibe_dados_pessoais(self): self.assertContains(self.client.get(reverse("usuarios:perfil")),"Walace Castro")
    def test_perfil_exibe_dados_organizacionais(self): self.perfil.cargo="Analista"; self.perfil.save(); self.assertContains(self.client.get(reverse("usuarios:perfil")),"Analista")
    def test_perfil_exibe_grupos(self): g=Group.objects.create(name="Grupo teste"); self.user.groups.add(g); self.assertContains(self.client.get(reverse("usuarios:perfil")),"Grupo teste")
    def test_perfil_exibe_permissoes(self): p=Permission.objects.get(codename="view_camera"); self.user.user_permissions.add(p); self.assertContains(self.client.get(reverse("usuarios:perfil")),p.name)
    def test_perfil_nao_exibe_upload_de_foto(self): self.assertNotContains(self.client.get(reverse("usuarios:perfil")),'type="file"')
    def test_editar_perfil_anonimo_redireciona(self): self.client.logout(); self.assertEqual(self.client.get(reverse("usuarios:editar_perfil")).status_code,302)
    def test_pagina_edicao_retorna_200(self): self.assertEqual(self.client.get(reverse("usuarios:editar_perfil")).status_code,200)
    def test_edicao_atualiza_dados_do_proprio_usuario(self): self.client.post(reverse("usuarios:editar_perfil"),self.dados()); self.user.refresh_from_db(); self.assertEqual((self.user.first_name,self.user.last_name,self.user.email),("Novo","Nome","novo@example.com"))
    def test_edicao_atualiza_telefone_e_ramal(self): self.client.post(reverse("usuarios:editar_perfil"),self.dados()); self.perfil.refresh_from_db(); self.assertEqual((self.perfil.telefone,self.perfil.ramal),("11999990000","123"))
    def test_edicao_nao_altera_username(self): d=self.dados(username="invasor"); self.client.post(reverse("usuarios:editar_perfil"),d); self.user.refresh_from_db(); self.assertEqual(self.user.username,"walace")
    def test_edicao_nao_altera_cargo_e_setor(self): self.perfil.cargo="Cargo"; self.perfil.setor="Setor"; self.perfil.save(); self.client.post(reverse("usuarios:editar_perfil"),self.dados(cargo="Outro",setor="Outro")); self.perfil.refresh_from_db(); self.assertEqual((self.perfil.cargo,self.perfil.setor),("Cargo","Setor"))
    def test_formulario_invalido_nao_salva_parcialmente(self): self.client.post(reverse("usuarios:editar_perfil"),self.dados(email="invalido")); self.perfil.refresh_from_db(); self.assertEqual(self.perfil.telefone,"")
    def test_edicao_valida_redireciona_para_perfil(self): self.assertRedirects(self.client.post(reverse("usuarios:editar_perfil"),self.dados()),reverse("usuarios:perfil"))
    def test_alterar_senha_anonimo_redireciona(self): self.client.logout(); self.assertEqual(self.client.get(reverse("usuarios:alterar_senha")).status_code,302)
    def test_pagina_alterar_senha_retorna_200(self): self.assertEqual(self.client.get(reverse("usuarios:alterar_senha")).status_code,200)
    def test_alteracao_valida_muda_senha_e_mantem_sessao(self):
        self.client.post(reverse("usuarios:alterar_senha"),{"old_password":"Senha-forte-123","new_password1":"Nova-senha-forte-456","new_password2":"Nova-senha-forte-456"}); self.user.refresh_from_db(); self.assertTrue(self.user.check_password("Nova-senha-forte-456")); self.assertIn("_auth_user_id",self.client.session)
    def test_senha_atual_incorreta_nao_altera_senha(self): self.client.post(reverse("usuarios:alterar_senha"),{"old_password":"errada","new_password1":"Nova-senha-forte-456","new_password2":"Nova-senha-forte-456"}); self.user.refresh_from_db(); self.assertTrue(self.user.check_password("Senha-forte-123"))
    def test_novas_senhas_diferentes_nao_alteram_senha(self): self.client.post(reverse("usuarios:alterar_senha"),{"old_password":"Senha-forte-123","new_password1":"Nova-senha-forte-456","new_password2":"Outra-senha-forte-789"}); self.user.refresh_from_db(); self.assertTrue(self.user.check_password("Senha-forte-123"))
    def test_template_de_senha_nao_reexibe_valores(self): response=self.client.post(reverse("usuarios:alterar_senha"),{"old_password":"SEGREDO-ATUAL","new_password1":"SEGREDO-NOVO","new_password2":"DIFERENTE"}); self.assertNotContains(response,"SEGREDO-ATUAL"); self.assertNotContains(response,"SEGREDO-NOVO")
    def test_cabecalho_exibe_menu_de_perfil(self): response=self.client.get(reverse("usuarios:perfil")); self.assertContains(response,"<details"); self.assertContains(response,"Meu perfil")
    def test_inicio_exibe_cartao_meu_perfil(self): self.assertContains(self.client.get(reverse("core:inicio")),"Meu Perfil")
    def test_iniciais_usuario_com_nome_completo(self): self.assertEqual(iniciais_usuario(self.user),"WC")
    def test_iniciais_usuario_com_fallback_para_username(self): self.user.first_name=self.user.last_name=""; self.assertEqual(iniciais_usuario(self.user),"WA")
    def test_admin_perfil_nao_permite_adicionar(self): self.assertFalse(PerfilUsuarioAdmin(PerfilUsuario,admin.site).has_add_permission(None))
    def test_admin_perfil_nao_permite_excluir(self): self.assertFalse(PerfilUsuarioAdmin(PerfilUsuario,admin.site).has_delete_permission(None,self.perfil))
