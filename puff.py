#!/usr/bin/env python3
#
#  PUFF: an easy and json friendly Windows prefetch file parser based on pyscca library
#
#  developed by Massimiliano Dal Cero
#
#  derived from Plaso project 
#  https://github.com/log2timeline/plaso/blob/main/plaso/parsers/winprefetch.py
#
#                     Apache License
#                Version 2.0, January 2004
#

import argparse
import pyscca
import json
import sys
from datetime import datetime, timedelta
from filtration import Expression


def ParseSCCAFile(scca_file, no_map = False):

    format_version          = scca_file.format_version
    executable_filename     = scca_file.executable_filename
    prefetch_hash           = scca_file.prefetch_hash
    run_count               = scca_file.run_count
    number_of_volumes       = scca_file.number_of_volumes
	
    event_data              = {}
    volume_serial_numbers   = []
    volume_device_paths     = []
    path_hints              = []
    devices                 = []
    timestamps              = []

    for volume_information in iter(scca_file.volumes):
      volume_serial_number  = volume_information.serial_number
      volume_device_path    = volume_information.device_path
      devtimestamp             = volume_information.get_creation_time_as_integer()

      volume_serial_numbers.append(volume_serial_number)
      volume_device_paths.append(volume_device_path.replace('\\',"/"))

      if devtimestamp:
        dev                     = {}
        dev["device_path"]      = volume_device_path.replace('\\',"/")
        dev["serial_number"]    = volume_serial_number
        dev["timestamp"]        = (datetime(1601, 1, 1) + timedelta(seconds=devtimestamp/10000000)).strftime("%m/%d/%Y, %H:%M:%S")
        
        devices.append(dev)

      for filename in iter(scca_file.filenames):
        if not filename:
          continue

        if (filename.startswith(volume_device_path) and filename.endswith(executable_filename)):
          _, _, path = filename.partition(volume_device_path)
          path_hints.append(path.replace('\\',"/"))

    mapped_files = []
    if not no_map:
        for entry_index, file_metrics in enumerate(scca_file.file_metrics_entries):
          
          mapped_file_string = file_metrics.filename
          if not mapped_file_string:
            continue

          file_reference = file_metrics.file_reference
          if file_reference:
            mapped_file_string = '{0:s} [{1:d}-{2:d}]'.format(
                    mapped_file_string, file_reference & 0xffffffffffff,
                    file_reference >> 48
                )

          mapped_files.append(mapped_file_string.replace('\\',"/") )

    timestamps.append( datetime(1601, 1, 1) + timedelta(seconds=scca_file.get_last_run_time_as_integer(0)/10000000) )

    if format_version >= 26:
      for last_run_time_index in range(1, 20):
        try:
            T = scca_file.get_last_run_time_as_integer(last_run_time_index)
            if T > 0:
                timestamps.append( datetime(1601, 1, 1) + timedelta(seconds=T/10000000) )
        except:
            pass
    
    mapped_files.sort()
    path_hints.sort()
    volume_device_paths.sort()
    volume_serial_numbers.sort()
    timestamps.sort()

    event_data["format_version"]        = format_version
    event_data["last_runs"]             = [] 
    for T in timestamps:
        event_data["last_runs"].append(T.strftime("%d/%m/%Y, %H:%M:%S"))
    event_data["last_runs_dt"]          = timestamps
    event_data["devices"]               = devices
    event_data["executable"]            = executable_filename
    event_data["mapped_files"]          = mapped_files
    event_data["number_of_volumes"]     = number_of_volumes
    event_data["path_hints"]            = path_hints
    event_data["prefetch_hash"]         = prefetch_hash
    event_data["run_count"]             = run_count
    event_data["version"]               = format_version
    event_data["volume_device_paths"]   = volume_device_paths
    event_data["volume_serial_numbers"] = volume_serial_numbers
    
    return event_data




if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog = 'puff',
                    description = 'Puff 1.0.1: An easy and JSON friendly Windows prefetch file parser based on pyscca library',
                    epilog = '--- [developed by Massimiliano Dal Cero] ---'
    )

    parser.add_argument('--no-mapped', required=False, help="Don't extract mapped file", action='store_true')
    parser.add_argument('--minimal', required=False, help="Minimal output: only essential evidences", action='store_true')
    parser.add_argument('-F', '--filter', type=str, required=False, help="Last Run Date Filter: last_run > 2022-11-25 18:00:00 and last_run < 2022-11-26 02:00:00", default=None)
    parser.add_argument('file.pf', type=str, nargs='+', help="Windows prefetch file")

    args = parser.parse_args()
    
    out = {}
    for fn1 in sys.argv[1:]:
        scca_file = pyscca.file()
        try:
            scca_file.open(fn1)
            pf = ParseSCCAFile(scca_file, args.no_mapped)
            scca_file.close()

            adding = True

            if args.filter:
                adding = False
                #Expression.parseString("last_run > 2022-11-01 20:04:00 and last_run < 2022-11-01 20:30:00 ")
                expr = Expression.parseString(args.filter)
                for lr in pf["last_runs_dt"]:
                    c={'last_run': lr}
                    if expr(c):
                        adding = True
            
            if args.no_mapped and not args.minimal:
                del(pf["mapped_files"])

            if args.minimal:
                del(pf["mapped_files"])
                del(pf["devices"])
                del(pf["format_version"])
                del(pf["number_of_volumes"])
                del(pf["executable"])
                del(pf["prefetch_hash"])
                del(pf["version"])
                del(pf["volume_device_paths"])
                del(pf["volume_serial_numbers"])


            del(pf["last_runs_dt"])

            if adding:
                out[fn1] = pf

        except:
            pass
   
    print( json.dumps(out, sort_keys=True, indent=3) )
    if args.filter:
        print("\nDATE FILTER:", file=sys.stderr)
        print(args.filter, file=sys.stderr)
