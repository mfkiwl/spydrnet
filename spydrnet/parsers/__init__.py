import os
import zipfile
import tempfile


def parse(filename):
    basename_less_final_extension = os.path.splitext(os.path.basename(filename))[0]
    extension = get_lowercase_extension(filename)
    if extension == ".zip":
        assert zipfile.is_zipfile(filename), \
            "Input filename {} with extension .zip is not a zip file.".format(basename_less_final_extension)
        with tempfile.TemporaryDirectory() as tempdirname:
            with zipfile.ZipFile(filename) as zip:
                files = zip.namelist()
                assert len(files) == 1 and files[0] == basename_less_final_extension, \
                    "Only single file archives allowed with a file whose name matches the name of the archive"
                zip.extract(basename_less_final_extension, tempdirname)
                filename = os.path.join(tempdirname, basename_less_final_extension)
                return _parse(filename)
    return _parse(filename)


def _parse(filename):
    extension = get_lowercase_extension(filename)
    if extension in [".edf", ".edif"]:
        from spydrnet.parsers.edif.parser import EdifParser
        parser = EdifParser.from_filename(filename)
    elif extension in [".v", ".vh"]:
        from spydrnet.parsers.verilog.parser import VerilogParser
        parser = VerilogParser.from_filename(filename)
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))
    parser.parse()
    return parser.netlist

def get_lowercase_extension(filename):
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    return extension_lower