import os
from zipfile import ZipFile
import glob

import time


if __name__ == '__main__':
    start_time = time.time()

    # print("Unzipping files")
    # test = glob.glob('../../support_files/EDIF_netlists/*.edf.zip')
    # for file in test:
    #     with ZipFile(file, 'r') as zip:
    #         zip.extractall()
    # # os.system('vivado -mode batch -source convert.tcl')
    # test = glob.glob('*.edf')
    # for file in test:
    #     os.remove(file)
    # test = glob.glob('*.v')
    # print("Zipping verilog files")
    path = '../../support_files/'
    # for file in test:
    #     with ZipFile(path + 'verilog_netlists/' + file + '.zip', 'w') as zip:
    #         zip.write(file)
    #     os.remove(file)
    print("Zipping vhdl files")
    test = glob.glob('*.vhd')
    for file in test:
        with ZipFile(path + 'VHDL_netlists/' + file + '.zip', 'w') as zip:
            zip.write(file)
        os.remove(file)

    print("--- %s seconds ---" % (time.time() - start_time))