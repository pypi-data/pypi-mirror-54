import colorama
from colorama.ansi import AnsiFore
from colorama import Fore, Back

from pathlib import Path
from os import startfile, system

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR.joinpath('template')


def highlight_print(msg: str, fore_color: AnsiFore = Fore.RED) -> None:
    print(Back.LIGHTYELLOW_EX + fore_color + msg)


def main(args):
    template_file = TEMPLATE_DIR / f'{args.ref}.template'
    if not template_file.exists():
        raise FileNotFoundError(template_file)

    template_text = template_file.read_text()
    work_dir = Path('.')  # current command line path
    outfile = work_dir / args.outfile
    outfile.write_text(template_text)
    startfile(work_dir)


class FormatText:
    __slots__ = ['align_list']

    def __init__(self, align_list: list):
        self.align_list = align_list

    def __call__(self, text_list: list):
        if len(text_list) != len(self.align_list):
            raise AttributeError
        return ' '.join(f'{txt:{flag}{int_align}}' for txt, (int_align, flag) in zip(text_list, self.align_list))

    @classmethod
    def text(cls, msg, fore_color: Fore = Fore.GREEN, back_color: Back = ""):
        return back_color + fore_color + msg + Fore.RESET


if __name__ == '__main__':
    colorama.init(autoreset=True)

    from argparse import ArgumentParser, RawTextHelpFormatter

    text = FormatText.text
    format_text = FormatText([(20, '<'), (60, '<')])

    script_description = \
        '\n'.join([desc for desc in
                   [f'\n{text("create_template.bat [REFERENCE TEMPLATE] [OUTPUT FILE NAME]")} to create template, for example:{text("create_template.bat PEP PEP.0484.py")}',
                    f'{text("create_template.bat -l *")} to get all available template',
                    f'{text("create_template.bat -o open")} open template directory so that you can put your template file there.',
                    ]])
    script_arg_parser = ArgumentParser(description='CREATE TEMPLATE TOOL',
                                       # conflict_handler='resolve',
                                       usage=script_description, formatter_class=RawTextHelpFormatter)
    arg_parser = script_arg_parser

    arg_parser.add_argument("ref", help="reference template", nargs='?')
    arg_parser.add_argument("outfile", help="output file name", nargs='?')
    arg_parser.add_argument('--list', "-l", dest='list',
                            help=f"example: {text('-l *')} \n"
                                 "description: list current available template. (accept regex)")

    arg_parser.add_argument('--option', "-o", dest='option',
                            help='\n'.join([format_text(msg_data_list) for msg_data_list in[
                                ['example', 'description'],
                                [text('-o open'), 'open template directory so that you can put your template file there.'],
                            ]]))

    g_args = arg_parser.parse_args()
    if g_args.option == 'open':
        startfile(TEMPLATE_DIR)
        exit(0)
    if g_args.list:
        [print(template_file_path.stem) for template_file_path in TEMPLATE_DIR.glob(f'{g_args.list}.template')]
        exit(0)

    for attr in ['ref', 'outfile']:
        if vars(g_args)[attr] is None:
            system('cls')
            print(f'error required values of {text(attr)} is None')
            print(f"if you need help, please use help command to help you: {text('create_template.bat -h', fore_color=Fore.RED, back_color=Back.LIGHTYELLOW_EX)}")
            exit(-1)

    highlight_print('GLOBAL ARGUMENT PARSER')
    print(f"{'key':<20} {'value':<40}")
    for key, value in vars(g_args).items():
        print(f"{key:<20} {value if value is not None else '':<40}")
    main(g_args)
