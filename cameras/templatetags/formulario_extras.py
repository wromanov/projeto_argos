from django import template


register = template.Library()


@register.filter
def campo_com_attrs(bound_field):
    """
    Renderiza um BoundField adicionando atributos ARIA
    exclusivamente relacionados a ajuda e erros de validacao.
    """
    attrs = {}
    described_by = []

    field_id = bound_field.id_for_label

    if field_id and bound_field.help_text:
        described_by.append(
            f"{field_id}_help"
        )

    if bound_field.errors:
        attrs["aria-invalid"] = "true"

        if field_id:
            error_id = f"{field_id}_errors"

            described_by.append(
                error_id
            )

            attrs["aria-errormessage"] = (
                error_id
            )

    if described_by:
        attrs["aria-describedby"] = (
            " ".join(described_by)
        )

    return bound_field.as_widget(
        attrs=attrs
    )
