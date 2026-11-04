import math

import FreeSimpleGUI as sg


def formatar_numero(valor):
    return format(valor, ".15g")


def criar_layout():
    """Monta o display, teclado e histórico da calculadora."""
    return [
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
        [sg.Text("Histórico recente (últimos 5)")],
        [
            sg.Listbox(
                values=[],
                key="-HISTORY-",
                size=(34, 5),
                expand_x=True,
                no_scrollbar=True,
            )
        ],
    ]


def calcular(primeiro_valor, segundo_valor, operacao):
    """Executa uma operação e rejeita divisão por zero ou resultado inválido."""
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


def tratar_erro(estado, mensagem):
    """Mostra o erro e descarta a operação incompleta."""
    estado["display"] = mensagem
    estado["valor_guardado"] = None
    estado["operacao_pendente"] = None
    estado["iniciar_novo_numero"] = True


def registrar_calculo(estado, window, primeiro, segundo, operacao, resultado):
    estado["historico"].append(
        f"{formatar_numero(primeiro)} {operacao} "
        f"{formatar_numero(segundo)} = {formatar_numero(resultado)}"
    )
    del estado["historico"][:-5]
    window["-HISTORY-"].update(values=estado["historico"])


def processar_evento(event, estado, window):
    if event == "-CLEAR-":
        estado["display"] = "0"
        estado["valor_guardado"] = None
        estado["operacao_pendente"] = None
        estado["iniciar_novo_numero"] = False
        estado["historico"].clear()
        window["-HISTORY-"].update(values=estado["historico"])
    elif event == "-BACKSPACE-":
        if not estado["iniciar_novo_numero"] and not estado["display"].startswith(
            "Erro:"
        ):
            estado["display"] = estado["display"][:-1] or "0"
    elif event in {"+", "-", "*", "/"}:
        _processar_operador(event, estado, window)
    elif event == "-EQUALS-":
        _processar_igual(estado, window)
    elif event == ".":
        if estado["iniciar_novo_numero"] or estado["display"].startswith("Erro:"):
            estado["display"] = "0."
        elif "." not in estado["display"]:
            estado["display"] += "."
        estado["iniciar_novo_numero"] = False
    elif isinstance(event, str) and event.isdigit():
        if estado["iniciar_novo_numero"] or estado["display"].startswith("Erro:"):
            estado["display"] = event
        elif estado["display"] == "0":
            estado["display"] = event
        else:
            estado["display"] += event
        estado["iniciar_novo_numero"] = False


def _processar_operador(event, estado, window):
    if estado["display"].startswith("Erro:"):
        return

    operacao = estado["operacao_pendente"]
    if operacao is not None:
        if estado["iniciar_novo_numero"]:
            tratar_erro(estado, "Erro: Expressão inválida")
            return
        try:
            primeiro = float(estado["valor_guardado"])
            segundo = float(estado["display"])
            resultado = calcular(primeiro, segundo, operacao)
        except ZeroDivisionError:
            tratar_erro(estado, "Erro: Divisão por zero")
            return
        except ValueError:
            tratar_erro(estado, "Erro: Expressão inválida")
            return

        registrar_calculo(estado, window, primeiro, segundo, operacao, resultado)
        estado["display"] = formatar_numero(resultado)
        estado["valor_guardado"] = resultado
    else:
        try:
            estado["valor_guardado"] = float(estado["display"])
            if not math.isfinite(estado["valor_guardado"]):
                raise ValueError
        except ValueError:
            tratar_erro(estado, "Erro: Expressão inválida")
            return

    estado["operacao_pendente"] = event
    estado["iniciar_novo_numero"] = True


def _processar_igual(estado, window):
    if estado["operacao_pendente"] is None or estado["iniciar_novo_numero"]:
        tratar_erro(estado, "Erro: Expressão inválida")
        return

    operacao = estado["operacao_pendente"]
    try:
        primeiro = float(estado["valor_guardado"])
        segundo = float(estado["display"])
        resultado = calcular(primeiro, segundo, operacao)
    except ZeroDivisionError:
        tratar_erro(estado, "Erro: Divisão por zero")
        return
    except ValueError:
        tratar_erro(estado, "Erro: Expressão inválida")
        return

    registrar_calculo(estado, window, primeiro, segundo, operacao, resultado)
    estado["display"] = formatar_numero(resultado)
    estado["valor_guardado"] = None
    estado["operacao_pendente"] = None
    estado["iniciar_novo_numero"] = True


def main():
    """Inicializa a janela e mantém o loop principal da interface."""
    sg.theme("LightGrey1")
    window = sg.Window(
        "Calculadora", criar_layout(), element_justification="center"
    )
    estado = {
        "display": "0",
        "valor_guardado": None,
        "operacao_pendente": None,
        "iniciar_novo_numero": False,
        "historico": [],
    }

    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
        processar_evento(event, estado, window)
        window["-DISPLAY-"].update(estado["display"])

    window.close()


if __name__ == "__main__":
    main()
