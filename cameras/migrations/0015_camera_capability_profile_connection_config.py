from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


def seed_rtsp_discovery(apps, schema_editor):
    Profile = apps.get_model("cameras", "CameraCapabilityProfile")
    Profile.objects.get_or_create(
        profile_key="RTSP_DISCOVERY_V1",
        version=1,
        defaults={
            "active": True,
            "adapter_key": "RTSP",
            "allowed_schemes": ["rtsp"],
            "allowed_ports": [554],
            "tls_policy": "NOT_APPLICABLE",
            "auth_method": "RTSP_NEGOTIATE",
            "credential_required": False,
            "endpoint_policy": "TECHNICIAN_OVERRIDE",
            "default_path": "",
            "allowed_override_fields": ["path", "port"],
            "probe_evidence_stage": "B",
            "source_ref": "ADR-021 §§3.5–3.6; CAM-INT-01; CAM-INT-03; CAM-INT-05",
        },
    )


def remove_rtsp_discovery(apps, schema_editor):
    # A reversão remove as tabelas após a configuração; preservar a linha evita
    # falha de PROTECT enquanto as dependências ainda existem.
    return None


class Migration(migrations.Migration):
    dependencies = [
        ("cameras", "0014_camera_authorization_permissions"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CameraCapabilityProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("profile_key", models.CharField(max_length=64)),
                ("version", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("active", models.BooleanField(default=False)),
                ("adapter_key", models.CharField(choices=[("RTSP", "RTSP"), ("HTTP_SNAPSHOT", "HTTP snapshot")], max_length=20)),
                ("allowed_schemes", models.JSONField(default=list)),
                ("allowed_ports", models.JSONField(default=list)),
                ("tls_policy", models.CharField(choices=[("REQUIRED", "Required"), ("NOT_REQUIRED", "Not required"), ("NOT_APPLICABLE", "Not applicable")], max_length=20)),
                ("auth_method", models.CharField(choices=[("NONE", "None"), ("BASIC", "Basic"), ("DIGEST", "Digest"), ("RTSP_NEGOTIATE", "RTSP negotiate")], max_length=20)),
                ("credential_required", models.BooleanField(default=False)),
                ("endpoint_policy", models.CharField(choices=[("PROFILE_FIXED", "Profile fixed"), ("TECHNICIAN_OVERRIDE", "Technician override")], max_length=24)),
                ("default_path", models.CharField(blank=True, default="", max_length=512)),
                ("allowed_override_fields", models.JSONField(default=list)),
                ("probe_evidence_stage", models.CharField(choices=[("A", "Network reachability"), ("B", "Protocol reachability"), ("C", "Media description"), ("D", "Media delivery")], max_length=1)),
                ("source_ref", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="camera_capability_profiles_created", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["profile_key", "-version"]},
        ),
        migrations.CreateModel(
            name="CameraConnectionConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("enabled", models.BooleanField(default=False)),
                ("rtsp_uri", models.CharField(blank=True, default="", max_length=1024)),
                ("http_endpoint_override", models.CharField(blank=True, default="", max_length=512)),
                ("http_port_override", models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65535)])),
                ("transport", models.CharField(choices=[("AUTO", "Automatic"), ("TCP", "TCP"), ("UDP", "UDP")], default="AUTO", max_length=8)),
                ("config_version", models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="camera_connection_configs_updated", to=settings.AUTH_USER_MODEL)),
                ("camera", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="connection_config", to="cameras.camera")),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="camera_configs", to="cameras.cameracapabilityprofile")),
            ],
        ),
        migrations.AddConstraint(
            model_name="cameracapabilityprofile",
            constraint=models.UniqueConstraint(fields=("profile_key", "version"), name="uniq_camera_capability_profile_version"),
        ),
        migrations.AddConstraint(
            model_name="cameracapabilityprofile",
            constraint=models.CheckConstraint(condition=models.Q(("version__gt", 0)), name="camera_capability_profile_version_positive"),
        ),
        migrations.AddIndex(
            model_name="cameracapabilityprofile",
            index=models.Index(fields=["active", "adapter_key"], name="cam_cap_active_adapter_idx"),
        ),
        migrations.AddConstraint(
            model_name="cameraconnectionconfig",
            constraint=models.CheckConstraint(condition=models.Q(("config_version__gt", 0)), name="camera_connection_config_version_positive"),
        ),
        migrations.AddIndex(
            model_name="cameraconnectionconfig",
            index=models.Index(fields=["enabled", "profile"], name="cam_conn_enabled_profile_idx"),
        ),
        migrations.RunPython(seed_rtsp_discovery, remove_rtsp_discovery),
    ]




\n