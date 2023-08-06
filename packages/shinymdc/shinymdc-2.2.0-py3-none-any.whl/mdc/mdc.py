import argparse
from collections import defaultdict
import os
import pkgutil
import shutil
import subprocess
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory

from shinyutils import LazyHelpFormatter

from mdc import __version__ as mdc_version

__all__ = ["build_pandoc_cmd", "run_compile"]

DEFAULT_FROM = "markdown-markdown_in_html_blocks-native_divs"
AVAILABLE_TEMPLATES = [
    "iclr",
    "icml",
    "neurips",
    "note",
    "simple",
    "standalone",
    "stylish",
]
DEFAULT_TEMPLATE = "simple"
TEMPLATE_RESOURCES = defaultdict(
    list,
    {
        "iclr": ["iclr.bst", "iclr.sty"],
        "icml": ["icml.bst", "icml.sty"],
        "neurips": ["neurips.sty"],
        "simple": [
            "ebgaramond12-regular.otf",
            "ebgaramond12-italic.otf",
            "ebgaramondcaps12-regular.otf",
            "lmmono10-regular.otf",
            "lmmono10-italic.otf",
            "lmmonocaps10-regular.otf",
        ],
        "stylish": [
            "ebgaramond12-regular.otf",
            "ebgaramond12-italic.otf",
            "ebgaramondcaps12-regular.otf",
            "futurabook-regular.ttf",
            "futurabook-italic.ttf",
            "futuramedium-regular.ttf",
            "lmmono10-regular.otf",
            "lmmono10-italic.otf",
            "lmmonocaps10-regular.otf",
        ],
    },
)
DEFAULT_BIBTYPE = "natbib"
DEFAULT_META = (
    "figPrefix=Figure",
    "eqnPrefix=Equation",
    "tblPrefix=Table",
    "lstPrefix=List",
    "secPrefix=Section",
)
DEFAULT_PANDOC = "pandoc"
DEFAULT_LATEXMK = "latexmk"
DEFAULT_CROSSREF = "pandoc-crossref"
DEFAULT_DEFAULT_IMG_EXT = "pdf"
DEFAULT_VERBOSE = False


def build_pandoc_cmd(
    input_file,
    from_=DEFAULT_FROM,
    template=DEFAULT_TEMPLATE,
    bibliography=None,
    bib_type=DEFAULT_BIBTYPE,
    crossref=DEFAULT_CROSSREF,
    include=None,
    meta=DEFAULT_META,
    pandoc=DEFAULT_PANDOC,
    default_img_ext=DEFAULT_DEFAULT_IMG_EXT,
):
    """Build required pandoc command from given arguments."""
    cmd = [pandoc]

    cmd.append(f"--from={from_}")
    cmd.append("--to=latex")

    if template in AVAILABLE_TEMPLATES:
        if not os.path.exists(f"{template}.tex"):
            template_data = pkgutil.get_data("mdc", f"templates/{template}.tex")
            if not template_data:
                raise AssertionError(
                    f"failed to load '{template}' template: "
                    f"installation might be corrupt: try reinstalling"
                )
            with open(f"{template}.tex", "wb") as f:
                f.write(template_data)
        cmd.append(f"--template={template}.tex")
    else:
        cmd.append(f"--template={template}")

    if bibliography is not None:
        cmd.append(f"--bibliography={bibliography}")
        cmd.append(f"--{bib_type}")

    if crossref is not None:
        cmd.append(f"--filter={crossref}")

    if include:
        for f in include:
            cmd.append(f"--include-before-body={f}")

    if meta:
        for m in meta:
            cmd.append(f"--metadata={m}")

    cmd.append(f"--default-image-extension={default_img_ext}")

    cmd.append(input_file)
    return cmd


def run_compile(
    pandoc_cmd,
    template,
    output_file=None,
    latexmk=DEFAULT_LATEXMK,
    verbose=DEFAULT_VERBOSE,
):
    """Run pandoc command to generate tex/pdf output."""
    if TEMPLATE_RESOURCES[template]:
        # Create and populate resources directory
        if not os.path.exists("resources"):
            os.mkdir("resources")
        for resc in TEMPLATE_RESOURCES[template]:
            if not os.path.exists(os.path.join("resources", resc)):
                resc_data = pkgutil.get_data("mdc", f"resources/{resc}")
                if not resc_data:
                    raise AssertionError(
                        f"failed to load 'resources/{resc}: "
                        f"installation might be corrupt: try reinstalling"
                    )
                with open(os.path.join("resources", resc), "wb") as f:
                    f.write(resc_data)

    if output_file is None:
        subprocess.run(pandoc_cmd, check=True)
    elif output_file.endswith(".tex"):
        pandoc_cmd.append(f"--output={output_file}")
        subprocess.run(pandoc_cmd, check=True)
    elif output_file.endswith(".pdf"):
        # Generate tex, then compile with latexmk
        with NamedTemporaryFile(dir="") as temp_file:
            pandoc_cmd.append(f"--output={temp_file.name}")
            subprocess.run(pandoc_cmd, check=True)

            with TemporaryDirectory() as temp_dir:
                latexmk_cmd = [
                    latexmk,
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "-pdf",
                    "-lualatex",
                    f"-output-directory={temp_dir}",
                    f"{temp_file.name}",
                ]
                if not verbose:
                    latexmk_cmd.append("-quiet")
                subprocess.run(latexmk_cmd, check=True)

                # Copy generated output file
                tf_only_name = os.path.basename(temp_file.name)
                shutil.copyfile(
                    os.path.join(temp_dir, f"{tf_only_name}.pdf"), f"{output_file}"
                )
    else:
        raise ValueError("output file extension must be .tex/.pdf")


def main():
    """Entry point."""

    def _meta_arg(string):
        """Argument type for passing meta variables."""
        if "=" not in string:
            raise argparse.ArgumentTypeError(
                "meta var should be passed as " "`key=val`"
            )
        k, v = string.split("=")
        return f"{k}:{v}"

    arg_parser = argparse.ArgumentParser(formatter_class=LazyHelpFormatter)
    arg_parser.add_argument("input_file", type=argparse.FileType("r"))
    arg_parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {mdc_version}"
    )
    arg_parser.add_argument(
        "-v", "--verbose", action="store_true", help="make latexmk verbose"
    )
    arg_parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default=None,
        help="write output to this file instead of stdout",
    )
    arg_parser.add_argument(
        "-f",
        "--from",
        type=str,
        dest="from_",
        metavar="FROM",
        default=DEFAULT_FROM,
        help="pandoc input format",
    )
    template_parser = arg_parser.add_mutually_exclusive_group(required=False)
    template_parser.add_argument(
        "-t",
        "--builtin-template",
        type=str,
        dest="template",
        metavar="TEMPLATE",
        choices=AVAILABLE_TEMPLATES,
        help="use one of the built-in templates",
    )
    template_parser.add_argument(
        "-T",
        "--custom-template",
        type=str,
        dest="template",
        metavar="CUSTOM_TEMPLATE",
        help="use a custom template",
    )
    arg_parser.set_defaults(template=DEFAULT_TEMPLATE)
    arg_parser.add_argument(
        "-b",
        "--bibliography",
        type=argparse.FileType("r"),
        default=None,
        help="bibliography argument for pandoc",
    )
    arg_parser.add_argument(
        "-B",
        "--bib-type",
        type=str,
        choices=["natbib", "biblatex"],
        default=DEFAULT_BIBTYPE,
        help="bibliography type sent to pandoc",
    )
    arg_parser.add_argument(
        "-i",
        "--include",
        type=argparse.FileType("r"),
        nargs="*",
        help="files to include before body",
    )
    arg_parser.add_argument(
        "-m",
        "--meta",
        type=_meta_arg,
        nargs="*",
        default=DEFAULT_META,
        help="additional meta variables to pass to pandoc",
    )
    arg_parser.add_argument(
        "-x",
        "--def-img-ext",
        type=str,
        default=DEFAULT_DEFAULT_IMG_EXT,
        help="default image extension for pandoc",
    )
    arg_parser.add_argument(
        "-P",
        "--pandoc",
        type=str,
        default=DEFAULT_PANDOC,
        help="path to pandoc executable",
    )
    arg_parser.add_argument(
        "-L",
        "--latexmk",
        type=str,
        default=DEFAULT_LATEXMK,
        help="path to latexmk executable",
    )
    arg_parser.add_argument(
        "-X",
        "--crossref",
        type=str,
        default=DEFAULT_CROSSREF,
        help="path to crossref executable",
    )
    args = arg_parser.parse_args()

    try:
        pandoc_cmd = build_pandoc_cmd(
            args.input_file.name,
            args.from_,
            args.template,
            args.bibliography.name if args.bibliography is not None else None,
            args.bib_type,
            args.crossref,
            [i.name for i in args.include] if args.include is not None else [],
            args.meta,
            args.pandoc,
            args.def_img_ext,
        )
        run_compile(
            pandoc_cmd, args.template, args.output_file, args.latexmk, args.verbose
        )
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e.cmd[0]} failed with return code {e.returncode}")
        return e.returncode
