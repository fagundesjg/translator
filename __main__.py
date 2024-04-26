import os
import shutil
import datetime
import argparse
import googletrans
from pathlib import Path
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
        path_file = os.path.join(dest_folder, dest)
        if not os.path.exists(dest_folder):
            os.mkdir(dest_folder)
        logger.debug(f"Vai copiar {src} -> {path_file}")
        shutil.copy2(src, path_file)
    else:
        logger.debug("2", src, dest)
        os.rename(src, dest)


def translate(name: str, dest_folder: str, attempt: int = 1):
    detected_lang = translator.detect(name)
    if detected_lang.lang != "pt":
        try:
            translated = translator.translate(
                text=name, src=detected_lang.lang, dest='pt')
            logger.log(
                f"Será traduzido de {detected_lang.lang} {name} -> {translated.text}")
            copy_file(src=name, dest=translated.text, dest_folder=dest_folder)
            logger.success(f"Arquivo renomeado {name} -> {translated.text}")
        except Exception as err:
            logger.error(f"Ocorreu um erro na tradução de '{name}': ", err)
            if attempt < 3:
                logger.warn(
                    f"({attempt + 1}) Tentando novamente realizar a tradução de '{name}'")
                translate(name=name,
                          dest_folder=dest_folder, attempt=attempt+1)
    else:
        logger.log(f"OK: {name}")
        copy_file(src=name, dest=os.path.join(
            dest_folder, name), dest_folder=dest_folder)


def translate_all(folder: str, dest_folder: str):
    if not os.path.isfile(folder):
        files = os.listdir(folder)
        files.sort()

        os.chdir(folder)
        logger.debug("Diretório atual: ", os.getcwd())

        for file_name in files:
            if file_name == dest_folder:
                continue
            logger.debug("Arquivo atual: ", file_name)
            translate_all(folder=file_name, dest_folder=dest_folder)
            translate(name=file_name, dest_folder=dest_folder)

        logger.debug("Voltou um diretorio")
        os.chdir("..")


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
