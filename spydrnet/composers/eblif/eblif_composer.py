import os
from spydrnet.util.selection import Selection
import spydrnet as sdn

class EBLIFComposer:
    def __init__(self,write_blackbox):
        self.netlist = None
        self.open_file = None
        self.write_blackbox = write_blackbox

    def run(self, ir, file_out):
        self.open_file = self.prepare_file(file_out)
        self._compose(ir)
    
    def prepare_file(self,out_file):
        if (os.path.exists(out_file)):
            f = open(out_file,"w")
        else:
            f = open(out_file,"x")
        return f
    
    def write_out(self,string):
        self.open_file.write(string)
    
    def clean_up(self):
        self.open_file.close()

    def _compose(self,ir):
        self.netlist = ir
        # print("Composing...")
        self.compose_comments()
        self.compose_top_model()
        self.clean_up()
    
    def compose_comments(self):
        for comment in self.netlist["EBLIF.comment"]:
            to_write = "# "+comment+"\n"
            self.write_out(to_write)
        self.write_out("\n")
    
    def compose_top_model(self):
        top_instance = self.netlist.top_instance
        to_write = ".model "+top_instance.reference.name+"\n"
        self.write_out(to_write)
        self.compose_top_level_ports()
        self.compose_top_level_clocks()
        self.compose_default_wires()
        self.compose_instances()
        self.compose_end()
        if (self.write_blackbox):
            self.compose_blackboxes()

    def compose_top_level_ports(self):
        to_write = ".inputs "
        for port in self.netlist.top_instance.get_ports(filter = lambda x: x.direction is sdn.Port.Direction.IN):
            if len(port.pins) > 1:
                for i in range(len(port.pins)):
                    to_write+=port.name+"["+str(i)+"] "
            else:
                to_write+=port.name+" "
        to_write+="\n"
        self.write_out(to_write)

        to_write = ".outputs "
        for port in self.netlist.top_instance.get_ports(filter = lambda x: x.direction is sdn.Port.Direction.OUT):
            if len(port.pins) > 1:
                for i in range(len(port.pins)):
                    to_write+=port.name+"["+str(i)+"] "
            else:
                to_write+=port.name+" "
        to_write+="\n"
        self.write_out(to_write)
    
    def compose_top_level_clocks(self):
        if "EBLIF.clock" in self.netlist.top_instance.data:
            to_write = ".clock "
            for clock in self.netlist.top_instance["EBLIF.clock"]:
                to_write+=clock+" "
            self.write_out(to_write+"\n")
    
    def compose_default_wires(self):
        default_wires = list()
        try:
            self.netlist["EBLIF.default_wires"]
            default_wires = self.netlist['EBLIF.default_wires']
        except KeyError:
            None
        if "$false" in default_wires:
            self.write_out(".names $false\n")
        if "$true" in default_wires:
            self.write_out(".names $true\n1\n")
        if "$undef" in default_wires:
            self.write_out(".names $undef\n")
        self.write_out("\n")
    
    def compose_instances(self):
        categories = self.separate_by_type()
        if "EBLIF.subckt" in categories.keys():
            self.compose_subcircuits(categories["EBLIF.subckt"])
        if "EBLIF.gate" in categories.keys():
            self.compose_subcircuits(categories["EBLIF.gate"],is_gate=True)
        if "EBLIF.other" in categories.keys():
            self.compose_subcircuits(categories["EBLIF.other"])
        if "EBLIF.names" in categories.keys():
            self.compose_names(categories["EBLIF.names"])
        if "EBLIF.latch" in categories.keys():
            self.compose_latches(categories["EBLIF.latch"])
    
    def separate_by_type(self):
        dict_by_types = dict()
        for instance in self.netlist.get_instances():
            try:
                instance["EBLIF.type"]
            except KeyError:
                # print("Error, no type found")
                instance["EBLIF.type"] = "EBLIF.other"
            type = instance["EBLIF.type"]
            try:
                dict_by_types[type]
            except KeyError:
                dict_by_types[type] = list()
            dict_by_types[type].append(instance)
        return dict_by_types
    
    def compose_subcircuits(self,list_of_subcircuits,is_gate=False):
        for subckt in list_of_subcircuits:
            to_add = ""
            if is_gate:
                to_write = ".gate "+ subckt.reference.name+" "
            else:
                to_write = ".subckt "+ subckt.reference.name+" "
            amount_of_ports_to_write = 0
            for port in subckt.get_ports():
                for pin in port.pins:
                    amount_of_ports_to_write+=1
            for port in subckt.reference.get_ports():
                inner_pin_list = port.pins     
                for pin in subckt.get_pins(selection=Selection.OUTSIDE,filter=lambda x: x.inner_pin.port is port):
                    if (amount_of_ports_to_write > 5):
                        to_write+=to_add+" \\ \n"
                        to_add = ""
                    if len(inner_pin_list) > 1:
                        index = inner_pin_list.index(pin.inner_pin)
                        to_add+=port.name+"["+str(index)+"]"+"="
                    else:
                        to_add+=port.name+"="
                    if pin.wire:
                        to_add+=self.find_connected_wire_info(pin)
                    else:
                        to_add+='unconn'
                    to_add+=" "
            to_write+=to_add+'\n'
            self.write_out(to_write)
            self.find_and_write_additional_instance_info(subckt)
    
    def compose_names(self,list_of_names):
        for name_instance in list_of_names:
            to_write = ".names "
            in_pin_list = list(x for x in name_instance.get_pins(selection=Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.direction is sdn.IN))
            in_pin_list.reverse()
            for pin in in_pin_list:
            # for pin in name_instance.get_pins(selection=Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.direction is sdn.IN):
                if pin.wire:
                    to_write+=pin.wire.cable.name
                    if len(pin.wire.cable.wires) > 1: # if a multi bit wire, add the index
                        to_write+="["+str(pin.wire.cable.wires.index(pin.wire))+"]"
                else:
                    to_write+="unconn"
                to_write+=" "
            for pin in name_instance.get_pins(selection=Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.direction is sdn.OUT):
                if pin.wire:
                    to_write+=pin.wire.cable.name
                    if len(pin.wire.cable.wires) > 1: # if a multi bit wire, add the index
                        to_write+="["+str(pin.wire.cable.wires.index(pin.wire))+"]"
                else:
                    to_write+="unconn"
                to_write+=" "
            to_write+="\n"
            try:
                name_instance["EBLIF.output_covers"]
                for output_cover in name_instance["EBLIF.output_covers"]:
                    to_write+=output_cover+"\n"
            except KeyError:
                None
            self.write_out(to_write)
            self.find_and_write_additional_instance_info(name_instance)

    def compose_latches(self,latch_list):
        for latch_instance in latch_list:
            to_write = ".latch "
            # port_list = list(x for x in latch_instance.get_ports())
            for port_type in ['input', 'output', 'type', 'control', 'init-val']: # this is the specific order of ports
                # current_port = next(port for port in port_list if port.name == port_type)
                for pin in latch_instance.get_pins(selection=Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.name == port_type):
                    # connection_name = None
                    if pin.wire:
                        to_write+=pin.wire.cable.name
                        if (len(pin.wire.cable.wires)>1):
                            to_write+="["+str(pin.wire.index())+"]"
                        to_write+=" "
                        # connection_name=pin.wire.cable.name
                    else:
                        to_write+="unconn "
                        # connection_name="unconn"
            to_write+='\n'
            self.write_out(to_write)
            self.find_and_write_additional_instance_info(latch_instance)

    def find_connected_wire_info(self,pin):
        string_to_return = ""
        cable = pin.wire.cable
        string_to_return+=cable.name
        if len(cable.wires) > 1:
            string_to_return+="["+str(pin.wire.index()) +"]"
        return string_to_return

    def find_and_write_additional_instance_info(self,instance):
        to_write = ""
        if "EBLIF.cname" in instance.data:
            to_write+=".cname "+instance["EBLIF.cname"]+'\n'
        if "EBLIF.attr" in instance.data:
            for key, value in instance.data["EBLIF.attr"].items():
                to_write+=".attr "+key+" "+value+'\n'
        if "EBLIF.param" in instance.data:
            for key, value in instance.data["EBLIF.param"].items():
                to_write+=".param "+key+" "+value+'\n'
        self.write_out(to_write)
    
    def compose_blackboxes(self):
        for definition in self.netlist.get_definitions():
            if "EBLIF.blackbox" in definition.data.keys():
                to_write = "\n.model "+definition.name
                to_write+="\n.inputs"
                for port in definition.get_ports(filter=lambda x: x.direction is sdn.IN):
                    to_write+=" "+port.name
                to_write+="\n.outputs"
                for port in definition.get_ports(filter=lambda x: x.direction is sdn.OUT):
                    to_write+=" "+port.name
                self.write_out(to_write+"\n")
                self.write_out(".blackbox\n")
                self.compose_end()

    def compose_end(self):
        self.write_out(".end\n")
