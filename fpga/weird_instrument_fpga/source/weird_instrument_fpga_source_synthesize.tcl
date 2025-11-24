if {[catch {

# define run engine funtion
source [file join {C:/lscc/radiant/2024.2} scripts tcl flow run_engine.tcl]
# define global variables
global para
set para(gui_mode) "1"
set para(prj_dir) "C:/Users/mkan/Documents/GitHub/s-m_microp_project/fpga/weird_instrument_fpga"
if {![file exists {C:/Users/mkan/Documents/GitHub/s-m_microp_project/fpga/weird_instrument_fpga/source}]} {
  file mkdir {C:/Users/mkan/Documents/GitHub/s-m_microp_project/fpga/weird_instrument_fpga/source}
}
cd {C:/Users/mkan/Documents/GitHub/s-m_microp_project/fpga/weird_instrument_fpga/source}
# synthesize IPs
# synthesize VMs
# synthesize top design
file delete -force -- weird_instrument_fpga_source.vm weird_instrument_fpga_source.ldc
::radiant::runengine::run_engine_newmsg synthesis -f "C:/Users/mkan/Documents/GitHub/s-m_microp_project/fpga/weird_instrument_fpga/source/weird_instrument_fpga_source_lattice.synproj" -logfile "weird_instrument_fpga_source_lattice.srp"
::radiant::runengine::run_postsyn [list -a iCE40UP -p iCE40UP5K -t SG48 -sp High-Performance_1.2V -oc Industrial -top -w -o weird_instrument_fpga_source_syn.udb weird_instrument_fpga_source.vm] [list weird_instrument_fpga_source.ldc]

} out]} {
   ::radiant::runengine::runtime_log $out
   exit 1
}
