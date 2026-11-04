import FreeSimpleGUI as sg


def formatar_numero(valor):
    return format(valor, ".15g")


def main():
    sg.theme("LightGrey1")

    layout = [
        [
            sg.Input(
                "0",
                key="-DISPLAY-",
                size=(16, 1),
                font=("Helvetica", 24),
                justification="right",
                readonly=True,
                expand_x=True,
            ),
            sg.Button("←", size=(5, 2), key="-BACKSPACE-"),
        ],
        [
            sg.Button("7", size=(5, 2), key="7"),
            sg.Button("8", size=(5, 2), key="8"),
            sg.Button("9", size=(5, 2), key="9"),
            sg.Button("/", size=(5, 2), key="/"),
        ],
        [
            sg.Button("4", size=(5, 2), key="4"),
            sg.Button("5", size=(5, 2), key="5"),
            sg.Button("6", size=(5, 2), key="6"),
            sg.Button("*", size=(5, 2), key="*"),
        ],
        [
            sg.Button("1", size=(5, 2), key="1"),
            sg.Button("2", size=(5, 2), key="2"),
            sg.Button("3", size=(5, 2), key="3"),
            sg.Button("-", size=(5, 2), key="-"),
        ],
        [
            sg.Button("C", size=(5, 2), key="-CLEAR-"),
            sg.Button("0", size=(5, 2), key="0"),
            sg.Button(".", size=(5, 2), key="."),
            sg.Button("+", size=(5, 2), key="+"),
        ],
        [sg.Button("=", size=(23, 2), key="-EQUALS-", expand_x=True)],
    ]

    window = sg.Window("Calculadora", layout, element_justification="center")
    display = "0"
    valor_guardado = None
    operacao_pendente = None
    iniciar_novo_numero = False

    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "-CLEAR-":
            display = "0"
            valor_guardado = None
            operacao_pendente = None
            iniciar_novo_numero = False
        elif event == "-BACKSPACE-":
            if not iniciar_novo_numero:
                display = display[:-1] or "0"
        elif event in "+-*/":
            if display == "Erro":
                display = "0"
            valor_guardado = float(display)
            operacao_pendente = event
            iniciar_novo_numero = True
        elif event == "-EQUALS-" and operacao_pendente is not None:
            segundo_valor = float(display)
            if operacao_pendente == "+":
                resultado = valor_guardado + segundo_valor
            elif operacao_pendente == "-":
                resultado = valor_guardado - segundo_valor
            elif operacao_pendente == "*":
                resultado = valor_guardado * segundo_valor
            else:
                if segundo_valor == 0:
                    display = "Erro"
                    valor_guardado = None
                    operacao_pendente = None
                    iniciar_novo_numero = True
                    window["-DISPLAY-"].update(display)
                    continue
                resultado = valor_guardado / segundo_valor

            display = formatar_numero(resultado)
            valor_guardado = None
            operacao_pendente = None
            iniciar_novo_numero = True
        elif event == ".":
            if iniciar_novo_numero or display == "Erro":
                display = "0."
            elif "." not in display:
                display += "."
            iniciar_novo_numero = False
        elif isinstance(event, str) and event.isdigit():
            if iniciar_novo_numero or display in ("0", "Erro"):
                display = event
            else:
                display += event
            iniciar_novo_numero = False

        window["-DISPLAY-"].update(display)

    window.close()


if __name__ == "__main__":
    main()
