from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("cameras", "0020_cameracapturejob"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="cameracapturejob",
            constraint=models.UniqueConstraint(
                fields=("camera",),
                condition=models.Q(status__in=("QUEUED", "RUNNING")),
                name="cam_capture_active_camera_uniq",
            ),
        ),
    ]
