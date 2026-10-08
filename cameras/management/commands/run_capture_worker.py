"""Run the isolated IMG-CAP worker; it never applies database migrations."""

import time

from django.core.management.base import BaseCommand, CommandError

from cameras.imagens.capture_service import run_next_capture


class Command(BaseCommand):
    help = "Consome jobs pendentes de captura de imagem de câmeras."

    def add_arguments(self, parser):
        parser.add_argument("--once", action="store_true", help="Processa no máximo um job e encerra.")
        parser.add_argument("--max-jobs", type=int, default=0, help="Limite de jobs; zero mantém o worker ativo.")
        parser.add_argument("--poll-seconds", type=float, default=1.0, help="Intervalo de polling quando a fila estiver vazia.")

    def handle(self, *args, **options):
        max_jobs = options["max_jobs"]
        poll_seconds = options["poll_seconds"]
        if max_jobs < 0 or poll_seconds < 0.1:
            raise CommandError("Limite de jobs ou intervalo inválido.")
        limit = 1 if options["once"] else max_jobs
        processed = 0
        while limit == 0 or processed < limit:
            job = run_next_capture()
            if job is None:
                if options["once"] or (limit and processed >= limit):
                    break
                time.sleep(poll_seconds)
                continue
            processed += 1
            self.stdout.write(f"{job.pk} {job.status} {job.error_code or '-'}")
        return f"Processed {processed} capture job(s)."
