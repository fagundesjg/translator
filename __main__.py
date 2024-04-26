import os
import shutil
import datetime
import argparse
import googletrans
from termcolor import colored

translator = googletrans.Translator()
DEBUG = False


class Logger:
    def log(self, *args, **kwargs):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(colored(timestamp, "grey", attrs=["bold"]), colored("[LOG]", "white", attrs=["bold"]), colored(
            ' '.join(map(str, args)), "grey"), **kwargs)

    def error(self, *args, **kwargs):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(colored(timestamp, "grey", attrs=["bold"]), colored("[ERROR]", "light_red", attrs=["bold"]), colored(
            ' '.join(map(str, args)), "red"), **kwargs)

    def success(self, *args, **kwargs):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(colored(timestamp, "grey", attrs=["bold"]), colored("[SUCCESS]", "light_green", attrs=["bold"]), colored(
            ' '.join(map(str, args)), "green"), **kwargs)

    def warn(self, *args, **kwargs):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        print(colored(timestamp, "grey", attrs=["bold"]), colored("[WARN]", "light_yellow", attrs=["bold"]), colored(
            ' '.join(map(str, args)), "grey"), **kwargs)

    def debug(self, *args, **kwargs):
        if DEBUG:
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            print(colored(timestamp, "grey", attrs=["bold"]), colored("[DEBUG]", "magenta", attrs=["bold"]), colored(
                ' '.join(map(str, args)), "light_magenta"), **kwargs)


logger = Logger()


def copy_file(src: str, dest: str, dest_folder: str) -> bool:
    if os.path.isfile(src):
        logger.debug("1", src, dest)
        dirname = os.path.dirname(dest)
        if not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        logger.debug(f"Vai copiar {src} -> {dest}")
        shutil.copy2(src, dest)
    else:
        logger.debug("2", src, dest)
        os.makedirs(dest, exist_ok=True)
        try:
            os.rename(os.path.join(dest_folder, src), dest)
            logger.success(f"{dest} renomeado com sucesso.")
        except Exception as err:
            logger.error(f"Erro ao renomear: {err}")


def translate(file: str, current_folder: str, dest_folder: str, attempt: int = 1):
    try:
        detected_lang = translator.detect(file)
        if detected_lang.lang != "pt":
            translated = translator.translate(
                text=file, src=detected_lang.lang, dest='pt')
            logger.log(
                f"[{detected_lang.lang}] Será traduzido de {file} -> {translated.text}")
            copy_file(src=os.path.join(current_folder, file), dest=os.path.join(
                dest_folder, current_folder, translated.text), dest_folder=dest_folder)
            logger.success(f"Arquivo renomeado {file} -> {translated.text}")
        else:
            logger.log(f"OK: {file}")
            copy_file(src=os.path.join(current_folder, file), dest=os.path.join(
                dest_folder, current_folder, file), dest_folder=dest_folder)
    except Exception as err:
        logger.error(f"Ocorreu um erro na tradução de '{file}': ", err)
        if attempt < 3:
            logger.warn(
                f"({attempt + 1}) Tentando novamente realizar a tradução de '{file}'")
            translate(file=file,
                      current_folder=current_folder, dest_folder=dest_folder, attempt=attempt+1)


def translate_all(folder: str, dest_folder: str):
    if not os.path.isfile(folder):
        files = os.listdir(folder)
        files.sort()

        for file_name in files:
            logger.debug("Arquivo atual: ", file_name)
            translate_all(folder=os.path.join(
                folder, file_name), dest_folder=dest_folder)
            translate(file=file_name, current_folder=folder,
                      dest_folder=dest_folder)


def main():
    global DEBUG

    parser = argparse.ArgumentParser(
        description='Processa os caminhos de input e output.')

    parser.add_argument('--input', type=str, default='.',
                        help='Caminho do arquivo de entrada. Padrão: "./input".')

    parser.add_argument('--output', type=str, default='./output',
                        help='Caminho do arquivo de saída. Padrão: "./output".')

    parser.add_argument('--debug', type=bool, default=False,
                        help='Exibir logs de debug')

    args = parser.parse_args()

    DEBUG = args.debug

    translate_all(folder=os.path.normpath(args.input),
                  dest_folder=os.path.normpath(args.output))

    return 0


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warn("Programa encerrado pelo usuário")
