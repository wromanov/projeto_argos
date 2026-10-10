# CAM-INT-05 derived automatic diagnostic snapshot.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cameras", "0017_camera_firmware_version_cameracapabilityevidence"),
    ]

    operations = [
        migrations.CreateModel(
            name="CameraHealthSnapshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("observed_at", models.DateTimeField()),
                ("config_generation", models.PositiveIntegerField()),
                ("stage_a_state", models.CharField(choices=[("PASS", "Pass"), ("FAIL", "Fail"), ("NOT_RUN", "Not run")], max_length=7)),
                ("stage_a_observed_at", models.DateTimeField()),
                ("stage_a_duration_seconds", models.FloatField()),
                ("stage_a_error_code", models.CharField(blank=True, default="", max_length=64)),
                ("stage_b_state", models.CharField(choices=[("PASS", "Pass"), ("FAIL", "Fail"), ("NOT_RUN", "Not run")], max_length=7)),
                ("stage_b_observed_at", models.DateTimeField()),
                ("stage_b_duration_seconds", models.FloatField()),
                ("stage_b_error_code", models.CharField(blank=True, default="", max_length=64)),
                ("stage_c_state", models.CharField(choices=[("PASS", "Pass"), ("FAIL", "Fail"), ("NOT_RUN", "Not run")], max_length=7)),
                ("stage_c_observed_at", models.DateTimeField()),
                ("stage_c_duration_seconds", models.FloatField()),
                ("stage_c_error_code", models.CharField(blank=True, default="", max_length=64)),
                ("stage_d_state", models.CharField(choices=[("PASS", "Pass"), ("FAIL", "Fail"), ("NOT_RUN", "Not run")], max_length=7)),
                ("stage_d_observed_at", models.DateTimeField()),
                ("stage_d_duration_seconds", models.FloatField()),
                ("stage_d_error_code", models.CharField(blank=True, default="", max_length=64)),
                ("reached_stage", models.CharField(blank=True, default="", max_length=1)),
                ("correlation_id", models.UUIDField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("camera", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="health_snapshot", to="cameras.camera")),
            ],
            options={
                "indexes": [models.Index(fields=["observed_at"], name="cam_health_observed_idx")],
                "constraints": [
                    models.CheckConstraint(condition=models.Q(("config_generation__gt", 0)), name="cam_health_generation_positive"),
                    *[
                        models.CheckConstraint(condition=models.Q((f"stage_{stage}_state__in", ["PASS", "FAIL", "NOT_RUN"])), name=f"cam_health_stage_{stage}_state_valid")
                        for stage in "abcd"
                    ],
                    *[
                        models.CheckConstraint(condition=models.Q((f"stage_{stage}_duration_seconds__gte", 0)), name=f"cam_health_stage_{stage}_duration_nonnegative")
                        for stage in "abcd"
                    ],
                    models.CheckConstraint(condition=models.Q(("reached_stage__in", ["", "A", "B", "C", "D"])), name="cam_health_reached_stage_valid"),
                    models.CheckConstraint(condition=models.Q(("stage_a_state", "PASS")) | models.Q(("stage_b_state", "NOT_RUN")), name="cam_health_stage_b_requires_a"),
                    models.CheckConstraint(condition=models.Q(("stage_b_state", "PASS")) | models.Q(("stage_c_state", "NOT_RUN")), name="cam_health_stage_c_requires_b"),
                    models.CheckConstraint(condition=models.Q(("stage_c_state", "PASS")) | models.Q(("stage_d_state", "NOT_RUN")), name="cam_health_stage_d_requires_c"),
                    models.CheckConstraint(
                        condition=models.Q(("stage_a_state", "PASS"), ("stage_b_state", "PASS"), ("stage_c_state", "PASS"), ("stage_d_state", "PASS")) | ~models.Q(("stage_d_state", "PASS")),
                        name="cam_health_d_pass_requires_abc",
                    ),
                ],
            },
        ),
    ]
