from django.core.management.base import BaseCommand, CommandError

from cameras.imagens.lifecycle_service import MAX_LIFECYCLE_BATCH, expire_due_images


class Command(BaseCommand):
    help = "Retira logicamente um lote bounded de imagens cuja retenção venceu."

    def add_arguments(self, parser):
        parser.add_argument("--batch-size", type=int, default=100)
        parser.add_argument("--camera-id", type=int)

    def handle(self, *args, **options):
        batch_size = options["batch_size"]
        if not 1 <= batch_size <= MAX_LIFECYCLE_BATCH:
            raise CommandError(f"--batch-size deve estar entre 1 e {MAX_LIFECYCLE_BATCH}.")
        count = expire_due_images(batch_size=batch_size, camera_id=options["camera_id"])
        self.stdout.write(self.style.SUCCESS(f"{count} imagem(ns) retirada(s) logicamente."))
