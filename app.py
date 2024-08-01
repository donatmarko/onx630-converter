# Batch Converter for ChannelExpert reports of Viavi ONX-630 CATV Field Analyzer
# Adapted for Vidanet Zrt.
# created by Donat MARKO :: donatus@vidanet.hu :: 2024

import os
import json
from pathlib import Path

pilot_range = [108.0, 743.25]
ed3_range = [114.0, 298.0]
dtv_range = [306.0, 498.0]

if __name__ == "__main__":
    out = open("out.csv", "w")    

    print("Writing header...")
    out.write("TX;Pilot L;Pilot H;Pilot Tilt;ED3 L;ED3 H;ED3 Tilt;DTV L;DTV H;DTV Tilt;ED3-DTV delta;QAM tilt;Analóg-QAM delta\n")

    for fname in Path(".").rglob("*.json"):
        print(f"Processing {fname}...")
        f = open(fname, "r")
        tx = str(fname).split('.')[0]

        data = json.load(f)

        carriers = data["tests"][0]["results"]["data"]["01_downstreamLevelsChart"]["Passed"]["data"]

        pilots = list(filter(lambda x: x[0] in pilot_range, carriers))
        ed3s = list(filter(lambda x: ed3_range[0] <= x[0] <= ed3_range[1], carriers))
        dtvs = list(filter(lambda x: dtv_range[0] <= x[0] <= dtv_range[1], carriers))

        pilot_lower = min(pilots, key=lambda x: x[0])
        pilot_upper = max(pilots, key=lambda x: x[0])
        pilot_tilt = pilot_upper[1] - pilot_lower[1]

        ed3_lower = min(ed3s, key=lambda x: x[0])
        ed3_upper = max(ed3s, key=lambda x: x[0])
        ed3_tilt = ed3_upper[1] - ed3_lower[1]

        dtv_lower = min(dtvs, key=lambda x: x[0])
        dtv_upper = max(dtvs, key=lambda x: x[0])
        dtv_tilt = dtv_upper[1] - dtv_lower[1]

        pilot_qam_diff = ed3_lower[1] - pilot_lower[1]

        ed3_dtv_diff = dtv_lower[1] - ed3_upper[1]
        ed3_dtv_tilt = dtv_upper[1] - ed3_lower[1]

        line = f"{tx};{pilot_lower[1]};{pilot_upper[1]};{pilot_tilt:.02f};{ed3_lower[1]};{ed3_upper[1]};{ed3_tilt:.02f};{dtv_lower[1]};{dtv_upper[1]};{dtv_tilt:.02f};{ed3_dtv_diff:.02f};{ed3_dtv_tilt:.02f};{pilot_qam_diff:.02f}"
        out.write(f"{line}\n")
        print("...done!")

    out.close()
    print("Finished.")
    os.system("pause")