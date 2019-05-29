from spydrnet.transform.triplicate import Triplicater
from spydrnet.transform.inserter import TMRInserter
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif

class TMR:
    def __init__(self):
        self.triplicator = Triplicater(3)
        self.inserter = TMRInserter()

    def run(self, cell_target, net_target, ir=None):
        self.triplicator.run(cell_target, ir)
        self.inserter.run(net_target, ir)


if __name__ == "__main__":
    filename = "add.edf"
    out_filename = "add_test.edf"
    parser = EdifParser.from_filename(filename)
    parser.parse()
    ir = parser.netlist

    triplicater = TMR()
    cell_test = ["add0", "co_INST_0", "add7", "a", "seg", "seg2"]
    # net_test = ["segment_OBUF_7_"]
    net_test = ["s_0_", "c_0", "co", "c_7", "s_7_", "led_OBUF_0_", "led_OBUF_1_", "led_OBUF_2_", "led_OBUF_3_",
                "led_OBUF_4_", "led_OBUF_5_", "led_OBUF_6_", "led_OBUF_7_", "led_OBUF_8_", "segment_OBUF_6_",
                "segment_OBUF_5_", "segment_OBUF_4_", "segment_OBUF_3_", "segment_OBUF_2_", "segment_OBUF_1_",
                "segment_OBUF_0_", "segment_2_"]
    # net_test = ["segment_OBUF_6_", "segment_OBUF_5_", "segment_OBUF_4_", "segment_OBUF_3_",
    #             "segment_OBUF_2_", "segment_OBUF_1_", "segment_OBUF_0_", "segment1_2_", "segment1_3_"]
    # cell_test = ["out_0__i_1", "out_reg_0_", "out_reg_1_"]
    # cell_test = ["out_0__i_1", "out_reg_0_", "out_1__i_1", "out_reg_1_", "out_2__i_1", "out_reg_2_", "out_3__i_1",
    #             "out_reg_3_"]
    # net_test = ["out_OBUF_0_", "out_OBUF_1_"]
    # net_test = ["out_OBUF_0_", "out_OBUF_1_", "out_OBUF_2_", "out_OBUF_3_"]

    triplicater.run(cell_test, net_test, ir)
    compose = ComposeEdif()

    compose.run(ir, out_filename)
