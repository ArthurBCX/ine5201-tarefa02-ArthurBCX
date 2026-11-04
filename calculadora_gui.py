import math

import FreeSimpleGUI as sg


def formatar_numero(valor):
    return format(valor, ".15g")


def calcular(primeiro_valor, segundo_valor, operacao):
    if operacao == "+":
        resultado = primeiro_valor + segundo_valor
    elif operacao == "-":
        resultado = primeiro_valor - segundo_valor
    elif operacao == "*":
        resultado = primeiro_valor * segundo_valor
    elif operacao == "/":
        if segundo_valor == 0:
            raise ZeroDivisionError
        resultado = primeiro_valor / segundo_valor
    else:
        raise ValueError("Operação inválida")

    if not math.isfinite(resultado):
        raise ValueError("Resultado fora do limite")
    return resultado


def main():
    sg.theme("LightGrey1")

    layout = [
        [
            sg.Input(
                "0",
                key="-DISPLAY-",
                size=(25, 1),
                font=("Helvetica", 18),
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

    def mostrar_erro(mensagem):
        nonlocal display, valor_guardado, operacao_pendente, iniciar_novo_numero
        display = mensagem
        valor_guardado = None
        operacao_pendente = None
        iniciar_novo_numero = True

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
            if not iniciar_novo_numero and not display.startswith("Erro:"):
                display = display[:-1] or "0"
        elif event in {"+", "-", "*", "/"}:
            if display.startswith("Erro:"):
                pass
            elif operacao_pendente is not None:
                if iniciar_novo_numero:
                    mostrar_erro("Erro: Expressão inválida")
                else:
                    try:
                        primeiro_valor = float(valor_guardado)
                        segundo_valor = float(display)
                        resultado = calcular(
                            primeiro_valor, segundo_valor, operacao_pendente
                        )
                    except ZeroDivisionError:
                        mostrar_erro("Erro: Divisão por zero")
                    except ValueError:
                        mostrar_erro("Erro: Expressão inválida")
                    else:
                        display = formatar_numero(resultado)
                        valor_guardado = resultado
                        operacao_pendente = event
                        iniciar_novo_numero = True
            else:
                try:
                    valor_guardado = float(display)
                    if not math.isfinite(valor_guardado):
                        raise ValueError
                except ValueError:
                    mostrar_erro("Erro: Expressão inválida")
                else:
                    operacao_pendente = event
                    iniciar_novo_numero = True
        elif event == "-EQUALS-":
            if operacao_pendente is None or iniciar_novo_numero:
                mostrar_erro("Erro: Expressão inválida")
            else:
                try:
                    segundo_valor = float(display)
                    resultado = calcular(
                        float(valor_guardado), segundo_valor, operacao_pendente
                    )
                except ZeroDivisionError:
                    mostrar_erro("Erro: Divisão por zero")
                except ValueError:
                    mostrar_erro("Erro: Expressão inválida")
                else:
                    display = formatar_numero(resultado)
                    valor_guardado = None
                    operacao_pendente = None
                    iniciar_novo_numero = True
        elif event == ".":
            if iniciar_novo_numero or display.startswith("Erro:"):
                display = "0."
            elif "." not in display:
                display += "."
            iniciar_novo_numero = False
        elif isinstance(event, str) and event.isdigit():
            if iniciar_novo_numero or display.startswith("Erro:"):
                display = event
            elif display == "0":
                display = event
            else:
                display += event
            iniciar_novo_numero = False

        window["-DISPLAY-"].update(display)

    window.close()


if __name__ == "__main__":
    main()
