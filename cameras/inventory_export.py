"""Safe, on-demand exports for the camera inventory."""

import csv
import io
import re
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from django.db.models import Sum
from django.db.models.functions import Length
from django.utils import timezone

from .forms import CAMPOS_CAMERA
from .models import Camera


# This is deliberately a fixed contract derived from the existing cadastral
# form allowlist. Model introspection must never expand the export surface.
_ROTULOS = {
    "patrimonio": "Patrimônio",
    "nome": "Nome",
    "fabricante": "Fabricante",
    "modelo": "Modelo",
    "serial": "Número de série",
    "mac": "Endereço MAC",
    "tipo": "Tipo de câmera",
    "terminal": "Terminal",
    "pavimento": "Pavimento",
    "setor": "Setor",
    "ambiente": "Ambiente",
    "descricao_detalhada": "Descrição detalhada",
    "ponto_referencia": "Ponto de referência",
    "ip": "Endereço IP",
    "mascara_subrede": "Máscara de sub-rede",
    "gateway": "Gateway",
    "vlan": "VLAN",
    "farm": "Farm",
    "retencao_esperada_dias": "Retenção esperada (dias)",
    "codec": "Codec",
    "origem_cadastro": "Origem do cadastro",
    "observacoes": "Observações",
    "situacao_operacional": "Situação operacional",
}

EXPORT_FIELDS = tuple(
    {"key": key, "label": _ROTULOS[key]} for key in (*CAMPOS_CAMERA, "situacao_operacional")
)
EXPORT_FIELD_BY_KEY = {field["key"]: field for field in EXPORT_FIELDS}
_FORMULA_PREFIX = re.compile(r"^\s*[=+\-@]")
_CHUNK_SIZE = 500
_PDF_CHUNK_SIZE = 25
PDF_MAX_RECORDS = 2300
PDF_MAX_FREE_TEXT_CHARS = 1_000_000
_PDF_FREE_TEXT_FIELDS = {"descricao_detalhada", "observacoes"}


class InvalidExportSelection(ValueError):
    """The request contains an unknown, duplicate, or empty field selection."""


class PdfExportLimitExceeded(ValueError):
    """The PDF report exceeds its bounded row or free-text budget."""


def selected_fields(raw_fields):
    fields = list(raw_fields)
    if not fields or len(fields) > len(EXPORT_FIELDS):
        raise InvalidExportSelection
    if len(set(fields)) != len(fields):
        raise InvalidExportSelection
    if any(field not in EXPORT_FIELD_BY_KEY for field in fields):
        raise InvalidExportSelection
    return tuple(EXPORT_FIELD_BY_KEY[field] for field in fields)


def validate_pdf_limits(queryset, fields, record_count):
    if record_count > PDF_MAX_RECORDS:
        raise PdfExportLimitExceeded

    text_fields = [
        field["key"] for field in fields
        if field["key"] in _PDF_FREE_TEXT_FIELDS
    ]
    if not text_fields:
        return

    totals = queryset.aggregate(
        **{
            f"chars_{field}": Sum(Length(field))
            for field in text_fields
        }
    )
    if sum(value or 0 for value in totals.values()) > PDF_MAX_FREE_TEXT_CHARS:
        raise PdfExportLimitExceeded


def pdf_export_available():
    try:
        from reportlab import __file__ as reportlab_package_file
        from reportlab.pdfgen import canvas  # noqa: F401
        font_path = Path(reportlab_package_file).parent / "fonts" / "Vera.ttf"
    except (ImportError, OSError):
        return False
    return font_path.is_file()


def _display_value(field, value):
    if value is None:
        return ""
    model_field = Camera._meta.get_field(field)
    if model_field.choices:
        value = dict(model_field.flatchoices).get(value, value)
    if isinstance(value, datetime):
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        return value.isoformat(sep=" ", timespec="seconds")
    if isinstance(value, (date, Decimal)):
        return str(value)
    return str(value)


def _safe_csv_cell(value):
    text = "" if value is None else str(value)
    if _FORMULA_PREFIX.match(text):
        return "'" + text
    return text


def csv_stream(queryset, fields):
    keys = [field["key"] for field in fields]
    labels = [field["label"] for field in fields]

    def generate():
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer, lineterminator="\r\n")
        yield "\ufeff"
        writer.writerow(labels)
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)
        for row in queryset.values(*keys).iterator(chunk_size=_CHUNK_SIZE):
            writer.writerow([_safe_csv_cell(_display_value(key, row[key])) for key in keys])
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)

    return generate()


def _wrap_text(text, font_name, font_size, max_width, pdfmetrics):
    """Wrap one cell in linear time without losing non-whitespace characters."""
    words = str(text).split()
    if not words:
        return [""]

    lines = []
    current_chars = []
    current_width = 0
    space_width = pdfmetrics.stringWidth(" ", font_name, font_size)

    for word in words:
        word_width = pdfmetrics.stringWidth(word, font_name, font_size)
        if word_width <= max_width:
            if current_chars and current_width + space_width + word_width > max_width:
                lines.append("".join(current_chars))
                current_chars = []
                current_width = 0
            if current_chars:
                current_chars.append(" ")
                current_width += space_width
            current_chars.extend(word)
            current_width += word_width
        else:
            if current_chars:
                lines.append("".join(current_chars))
                current_chars = []
                current_width = 0
            for character in word:
                character_width = pdfmetrics.stringWidth(
                    character, font_name, font_size
                )
                if current_chars and current_width + character_width > max_width:
                    lines.append("".join(current_chars))
                    current_chars = []
                    current_width = 0
                current_chars.append(character)
                current_width += character_width

    if current_chars or not lines:
        lines.append("".join(current_chars))
    return lines


def write_pdf(file_obj, queryset, fields, filters, record_count):
    """Render a row-streamed PDF; selected columns may make a wide page."""
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen import canvas

    from reportlab import __file__ as reportlab_package_file

    font_path = Path(reportlab_package_file).parent / "fonts" / "Vera.ttf"
    if not font_path.is_file():
        raise RuntimeError("Unicode font unavailable")
    font_name = "ArgosVera"
    if font_name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(font_name, str(font_path)))

    margin = 28
    column_width = 110
    page_width = max(842, margin * 2 + column_width * len(fields))
    page_height = 595
    row_font_size = 7.5
    leading = 9
    available_width = column_width - 8
    page = canvas.Canvas(file_obj, pagesize=(page_width, page_height), pageCompression=1)
    page.setTitle("Inventário de câmeras")
    page.setAuthor("ARGOS")
    page.setSubject("Exportação do inventário de câmeras")

    title = "Inventário de câmeras"
    timestamp = timezone.localtime(timezone.now()).strftime("%d/%m/%Y %H:%M:%S %Z")
    filter_text = "; ".join(filters) if filters else "nenhum filtro adicional"
    fields_text = ", ".join(field["label"] for field in fields)
    y = page_height - margin
    page.setFont(font_name, 13)
    page.drawString(margin, y, title)
    y -= 18
    page.setFont(font_name, 8)
    page.drawString(margin, y, f"Gerado em {timestamp} · {record_count} registro(s)")
    y -= 13
    for metadata_label, metadata_value in (("Filtros", filter_text), ("Campos", fields_text)):
        wrapped = _wrap_text(f"{metadata_label}: {metadata_value}", font_name, 7.5, page_width - 2 * margin, pdfmetrics)
        for line in wrapped:
            page.drawString(margin, y, line)
            y -= leading

    def draw_footer(page_number):
        page.setStrokeColor(HexColor("#d8dee8"))
        page.line(margin, 24, page_width - margin, 24)
        page.setFillColor(HexColor("#495466"))
        page.setFont(font_name, 7)
        page.drawRightString(page_width - margin, 12, f"ARGOS · Página {page_number}")
        page.setFillColor(HexColor("#111827"))

    page_number = 1
    keys = [field["key"] for field in fields]

    def draw_header(top):
        x = margin
        page.setFillColor(HexColor("#e9eef5"))
        page.rect(margin, top - 19, column_width * len(fields), 19, fill=1, stroke=0)
        page.setFillColor(HexColor("#111827"))
        page.setFont(font_name, 7.5)
        for field in fields:
            for line_index, line in enumerate(_wrap_text(field["label"], font_name, 7.5, available_width, pdfmetrics)[:2]):
                page.drawString(x + 4, top - 10 - line_index * leading, line)
            x += column_width
        page.setStrokeColor(HexColor("#aeb8c6"))
        for index in range(len(fields) + 1):
            x = margin + index * column_width
            page.line(x, top - 19, x, 24)
        return top - 19

    y = draw_header(y - 4)
    page.setFont(font_name, row_font_size)
    page.setStrokeColor(HexColor("#d8dee8"))
    for row in queryset.values(*keys).iterator(chunk_size=_PDF_CHUNK_SIZE):
        cell_lines = [
            _wrap_text(_display_value(key, row[key]), font_name, row_font_size, available_width, pdfmetrics)
            for key in keys
        ]
        offsets = [0] * len(cell_lines)
        while any(offset < len(lines) for offset, lines in zip(offsets, cell_lines)):
            room_for_lines = max(0, int((y - 30 - 6) // leading))
            if room_for_lines == 0:
                draw_footer(page_number)
                page.showPage()
                page_number += 1
                y = page_height - margin
                page.setFont(font_name, 13)
                page.drawString(margin, y, title)
                y = draw_header(y - 7)
                page.setFont(font_name, row_font_size)
                room_for_lines = max(1, int((y - 30 - 6) // leading))

            fragment_size = min(
                room_for_lines,
                max(len(lines) - offset for offset, lines in zip(offsets, cell_lines)),
            )
            row_height = max(17, fragment_size * leading + 6)
            for index, lines in enumerate(cell_lines):
                x = margin + index * column_width + 4
                fragment = lines[offsets[index]:offsets[index] + fragment_size]
                for line_index, line in enumerate(fragment):
                    page.drawString(x, y - 11 - line_index * leading, line)
                offsets[index] += len(fragment)
            page.line(margin, y - row_height, page_width - margin, y - row_height)
            y -= row_height

    draw_footer(page_number)
    page.save()
