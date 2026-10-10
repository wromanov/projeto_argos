import asyncio
import signal

from django.core.management.base import BaseCommand, CommandError

from cameras.monitoramento.runtime import RuntimePreflightError, build_runtime


class Command(BaseCommand):
    help = "Executa o worker dedicado de monitoramento MON."

    def add_arguments(self, parser):
        parser.add_argument("--once", action="store_true", help="Executa um ciclo local e encerra (uso de validação).")

    def handle(self, *args, **options):
        try:
            runtime = build_runtime()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                for signum in (signal.SIGINT, signal.SIGTERM):
                    try:
                        signal.signal(signum, lambda _sig, _frame: loop.call_soon_threadsafe(runtime._stop.set))
                    except (ValueError, OSError):
                        continue
                graceful = loop.run_until_complete(runtime.run(once=options["once"]))
            finally:
                loop.close()
        except RuntimePreflightError as exc:
            raise CommandError(f"Preflight MON falhou ({exc.code}).") from None
        except Exception as exc:
            raise CommandError(f"Worker MON encerrou por falha operacional ({type(exc).__name__}).") from None
        if not graceful:
            raise CommandError("Worker MON encerrou com shutdown incompleto; ownership permanece cercado.")
