"""
Invokes capco commands when the src module is run as a script.
Example: python3 -m src templates list
"""
import src.commands.commands


def main():
    src.commands.commands.commands()


if __name__ == "__main__":
    main()
