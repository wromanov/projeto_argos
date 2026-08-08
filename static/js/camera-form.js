(() => {
    "use strict";

    const VALOR_PERSONALIZADO = "__PERSONALIZADO__";

    function inicializarFarmPersonalizada() {
        const select = document.querySelector(
            "[data-farm-select]"
        );

        const container = document.querySelector(
            "[data-farm-personalizado]"
        );

        if (!select || !container) {
            return;
        }

        const input = container.querySelector(
            "input"
        );

        function atualizarInterface({ focar = false } = {}) {
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

    if (
        document.readyState === "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            inicializarFarmPersonalizada
        );
    } else {
        inicializarFarmPersonalizada();
    }
})();
