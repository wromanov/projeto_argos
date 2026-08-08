(() => {
    "use strict";

    const VALOR_PERSONALIZADO = "__PERSONALIZADO__";

    const CAMPOS_PERSONALIZADOS = [
        {
            select: "[data-farm-select]",
            container: "[data-farm-personalizado]",
        },
        {
            select: "[data-codec-select]",
            container: "[data-codec-personalizado]",
        },
    ];

    function inicializarCampoPersonalizado({
        select: seletorSelect,
        container: seletorContainer,
    }) {
        const select = document.querySelector(
            seletorSelect
        );

        const container = document.querySelector(
            seletorContainer
        );

        if (!select || !container) {
            return;
        }

        const input = container.querySelector(
            "input"
        );

        function atualizarInterface({
            focar = false,
        } = {}) {
            const personalizado = (
                select.value === VALOR_PERSONALIZADO
            );

            container.hidden = !personalizado;

            select.setAttribute(
                "aria-expanded",
                String(personalizado)
            );

            if (input) {
                input.disabled = !personalizado;

                if (
                    personalizado
                    && focar
                ) {
                    input.focus();
                }
            }
        }

        select.addEventListener(
            "change",
            () => {
                atualizarInterface({
                    focar: true,
                });
            }
        );

        atualizarInterface();
    }

    function inicializarFormularioCamera() {
        CAMPOS_PERSONALIZADOS.forEach(
            inicializarCampoPersonalizado
        );
    }

    if (
        document.readyState === "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            inicializarFormularioCamera
        );
    } else {
        inicializarFormularioCamera();
    }
})();
