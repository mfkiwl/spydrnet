import unittest
import spydrnet as sdn
from spydrnet import composers
from spydrnet import parsers
import tempfile
from pathlib import Path
import zipfile

class TestVerilogComposer(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_of_verilog_netlists = Path(sdn.example_netlists_path, "verilog_netlists")        
        cls.verilog_files = sorted(Path.glob(cls.dir_of_verilog_netlists, "*.v.zip"))

    @unittest.skip("Test takes a long time right now.")
    def test_large_verilog_compose(self):
        i = 0
        errors = 0
        for ii, filepath in enumerate(self.verilog_files):
            with self.subTest(i=ii):
                if Path(filepath).stat().st_size <= 1024 * 10:
                    continue
                if zipfile.is_zipfile(filepath):
                    with tempfile.TemporaryDirectory() as tempdirectory:
                        # try:
                            print("*********************"+filepath.name+"*********************")
                            # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename(os.path.join(directory, filename))
                            # netlist = vp.parse()
                            netlist = parsers.parse(filepath)
                            composers.compose(netlist, Path(tempdirectory).joinpath(filepath.name +  "-spydrnet.v"))
                            #comp.run(netlist,"temp2/"+filename[:len(filename)-6] + "-spydrnet.v")
                            # comp.run(netlist,os.path.join(tempdirectory, filename[:len(filename)-6] + "-spydrnet.v"))
                            i+=1
                            print("pass")
                        # except Exception as identifier:
                        #     print("FAIL")
                        #     print(identifier)
                        #     errors += 1
                else:
                    continue

        print("processed",i,"errors", errors)
        
        assert errors == 0, "there were errors while parsing and composing files. Please see the output."

    def test_small_verilog_compose(self):
        i = 0
        errors = 0
        for ii, filepath in enumerate(self.verilog_files):
            with self.subTest(i=ii):
                if filepath.stat().st_size > 1024 * 10:
                    continue
                # if filename.endswith(".zip"):
                if zipfile.is_zipfile(filepath):
                    with tempfile.TemporaryDirectory() as tempdirectory:
                        # try:
                            print("*********************"+filepath.name+"*********************")
                            # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename(os.path.join(directory, filename))
                            # netlist = vp.parse()
                            netlist = parsers.parse(filepath)
                            composers.compose(netlist, Path(tempdirectory).joinpath(filepath.name + "-spydrnet.v"))
                            #comp.run(netlist,"temp2/"+filename[:len(filename)-6] + "-spydrnet.v")
                            # comp.run(netlist,os.path.join(tempdirectory, filename[:len(filename)-6] + "-spydrnet.v"))
                            i+=1
                            print("pass")
                        # except Exception as identifier:
                        #     print("FAIL")
                        #     print(identifier)
                        #     errors += 1
                else:
                    continue

        print("processed",i,"errors", errors)
        
        assert errors == 0, "there were errors while parsing and composing files. Please see the output."

    def test_definition_list_option(self):
        for filename in Path.glob(self.dir_of_verilog_netlists, "*4bitadder.v.zip"):
            with tempfile.TemporaryDirectory() as tempdirectory:
                netlist = parsers.parse(filename)
                out_file = Path(
                    tempdirectory, Path(filename).name + "-spydrnet.v")
                composers.compose(netlist, out_file, definition_list=['adder'])

                with open(out_file, "r") as fp:
                    lines = fp.readlines()
                    print(len(lines))
                    m = list(filter(lambda x: x.startswith('module'), lines))
            self.assertGreater(len(m), 0, "Adder module not written")
            self.assertLess(len(m), 2, "Failed to write only definition_list")
            return
        raise AssertionError("Adder design not found " +
                             "definition_list options not tested,")

    def test_write_blackbox_option(self):
        for filename in Path.glob(self.dir_of_verilog_netlists, "*4bitadder.v.zip"):
            print(filename)
            with tempfile.TemporaryDirectory() as tempdirectory:
                netlist = parsers.parse(filename)
                out_file = Path(
                    tempdirectory, Path(filename).name + "-spydrnet.v")
                composers.compose(netlist, out_file, write_blackbox=False)

                with open(out_file, "r") as fp:
                    lines = fp.readlines()
                    print(len(lines))
                    m = list(filter(lambda x: x.startswith('module'), lines))
            self.assertGreater(len(m), 0, "Adder module not written")
            self.assertLess(len(m), 2, "Failed to write only definition_list" +
                            "%s" % m)
            return
        raise AssertionError("definition_list options not test," +
                             "Adder design not found")
