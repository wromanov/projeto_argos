# Generated from the reconciled CAM-INT-04 capture-job model.
import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cameras", "0019_alter_camera_options_cameraimportpreview"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CameraCaptureJob",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("idempotency_key", models.CharField(max_length=128)),
                ("source", models.CharField(choices=[("HTTP_SNAPSHOT", "HTTP snapshot"), ("RTSP_FRAME", "RTSP frame")], max_length=20)),
                ("profile_key", models.CharField(max_length=64)),
                ("profile_version", models.PositiveIntegerField()),
                ("config_version", models.PositiveIntegerField()),
                ("status", models.CharField(choices=[("QUEUED", "Queued"), ("RUNNING", "Running"), ("SUCCEEDED", "Succeeded"), ("FAILED", "Failed"), ("CANCELLED", "Cancelled")], default="QUEUED", max_length=12)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("error_code", models.CharField(blank=True, default="", max_length=32)),
                ("camera", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="capture_jobs", to="cameras.camera")),
                ("image_record", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="capture_job", to="cameras.cameraimagerecord")),
                ("requestor", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="camera_capture_jobs", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(model_name="cameracapturejob", constraint=models.UniqueConstraint(fields=("camera", "requestor", "idempotency_key"), name="cam_capture_idempotency_uniq")),
        migrations.AddConstraint(model_name="cameracapturejob", constraint=models.CheckConstraint(condition=models.Q(source__in=["HTTP_SNAPSHOT", "RTSP_FRAME"]), name="cam_capture_source_valid")),
        migrations.AddConstraint(model_name="cameracapturejob", constraint=models.CheckConstraint(condition=models.Q(status__in=["QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "CANCELLED"]), name="cam_capture_status_valid")),
        migrations.AddConstraint(model_name="cameracapturejob", constraint=models.CheckConstraint(condition=models.Q(profile_version__gt=0), name="cam_capture_profile_version_positive")),
        migrations.AddConstraint(model_name="cameracapturejob", constraint=models.CheckConstraint(condition=models.Q(config_version__gt=0), name="cam_capture_config_version_positive")),
        migrations.AddConstraint(model_name="cameracapturejob", constraint=models.CheckConstraint(condition=models.Q(models.Q(("error_code", ""), ("image_record__isnull", False), ("status", "SUCCEEDED")), models.Q(("error_code", ""), ("image_record__isnull", True), ("status__in", ["QUEUED", "RUNNING"])), models.Q(("error_code__gt", ""), ("image_record__isnull", True), ("status__in", ["FAILED", "CANCELLED"])), _connector="OR"), name="cam_capture_result_coherent")),
        migrations.AddIndex(model_name="cameracapturejob", index=models.Index(fields=["status", "created_at"], name="cam_capture_status_created_idx")),
        migrations.AddIndex(model_name="cameracapturejob", index=models.Index(fields=["camera", "created_at"], name="cam_capture_camera_created_idx")),
    ]
