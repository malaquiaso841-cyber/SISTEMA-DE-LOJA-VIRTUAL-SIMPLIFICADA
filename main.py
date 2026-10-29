import argparse

from interface.menu import menu


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sistema de loja virtual"
    )
    interfaces = parser.add_mutually_exclusive_group(required=True)

    interfaces.add_argument(
        "--terminal",
        action="store_true",
        help="Abrir a interface de terminal",
    )
    interfaces.add_argument(
        "--grafica",
        action="store_true",
        help="Abrir a interface gráfica",
    )

    argumentos = parser.parse_args()

    if argumentos.terminal:
        menu()
    elif argumentos.grafica:
        from interface.gui import iniciar_interface

        iniciar_interface()


if __name__ == "__main__":
    main()
