# set file fourBitCounter.edf
# set module fourBitCounter

#set file [lindex $argv 0]
#set file [lindex $argv 0].edf
#put $file
#set dot [expr [string length $file] - 5]
#set module [string range $file 0 $dot]
#puts "*******************************************"
#put $module
#add_files $file
#set_property top $module [current_fileset]
#link_design -name netlist_1
#write_verilog -file [pwd]/$module.v -include_xilinx_libs -force
#write_vhdl -file [pwd]/$module.vhd -include_xilinx_libs -force
#close_design
#remove_file $file
#if {[lindex [split [lindex $argv 0] .] 1] == "edf"} { puts "You want to convert an EDIF file" }


set files [glob *.edf]	;
foreach file $files {	;
	set dot [expr [string length $file] - 5]
	set module [string range $file 0 $dot]
	puts "*******************************************"
	put $module
	add_files $file
	set_property top $module [current_fileset]
	if {[catch {link_design -name netlist_1} issue]} {
		remove_file $file
		continue
	}
	#link_design -name netlist_1
	write_verilog -file [pwd]/$module.v -include_xilinx_libs -force
	write_vhdl -file [pwd]/$module.vhd -include_xilinx_libs -force
	close_design
	remove_file $file
}