"""
Utility script used during OTA design to generate gm/Id lookup tables
from ngspice DC sweep data. The LUTs are used for transistor sizing
and trade-off analysis during the design process.
"""

#!/usr/bin/env python3

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from scipy.signal import savgol_filter
    HAVE_SAVGOL = True
except Exception:
    HAVE_SAVGOL = False


def basename_no_ext(path):
    return path.replace("\\", "/").split("/")[-1].rsplit(".", 1)[0]


def read_raw(path):
    return pd.read_csv(path, delim_whitespace=True)


def detect_cols(df):
    num_df = df.select_dtypes(include=[np.number])
    cols = list(num_df.columns)

    # Vgs column (v(net2), v(g), etc.)
    vgs_col = None
    for c in cols:
        cl = c.lower()
        if "v(" in cl or "vgs" in cl or "net2" in cl or "gate" in cl:
            vgs_col = c
            break
    if vgs_col is None:
        vgs_col = cols[0]

    # Current column (i(v2), etc.)
    id_col = None
    for c in cols:
        cl = c.lower()
        if "i(" in cl:
            id_col = c
            break
    if id_col is None:
        # fallback: second numeric column
        id_col = cols[1] if len(cols) > 1 else cols[0]

    print(f"Using Vgs column: {vgs_col}")
    print(f"Using Id  column: {id_col}")

    vgs = num_df[vgs_col].to_numpy(dtype=float)
    id_raw = num_df[id_col].to_numpy(dtype=float)
    return vgs, id_raw


def smooth_vec(x, window=31):
    n = len(x)
    if n < 5:
        return x
    if HAVE_SAVGOL:
        w = min(window, n if n % 2 == 1 else n - 1)
        if w < 5:
            w = 5 if n >= 5 else (n if n % 2 == 1 else n - 1)
        try:
            return savgol_filter(x, w, 3)
        except Exception:
            pass
    w = min(11, n if n % 2 == 1 else n - 1)
    if w < 3:
        return x
    k = np.ones(w) / w
    return np.convolve(x, k, mode="same")


def process_file(path):
    base = basename_no_ext(path)
    print("\nProcessing:", base)

    df = read_raw(path)
    vgs, id_raw = detect_cols(df)

    # Make Id positive (ngspice branch currents are usually negative)
    if np.median(id_raw) < 0:
        id_raw = -id_raw

    # Smooth Id a bit
    id_s = smooth_vec(id_raw, window=41)

    # Compute gm = dId/dVgs
    gm = np.gradient(id_s, vgs)
    gm_id = gm / (id_s + 1e-30)

    # Id per um (you simulated with W = 1um)
    id_per_um = id_s.copy()

    lut = pd.DataFrame(
        {
            "Vgs(V)": vgs,
            "Id(A)": id_s,
            "gm(A/V)": gm,
            "gm_Id(1/V)": gm_id,
            "Id_per_um(A/um)": id_per_um,
        }
    )

    out_name = f"{base}_gm_lookup.csv"
    lut.to_csv(out_name, index=False)
    print("Saved lookup:", out_name)

    # Quick plots
    plt.figure()
    plt.plot(vgs, id_raw, label="Id raw")
    plt.plot(vgs, id_s, label="Id smoothed")
    plt.xlabel("Vgs (V)")
    plt.ylabel("Id (A)")
    plt.grid(True)
    plt.legend()
    plt.title(f"{base} : Id vs Vgs")
    plt.show()

    plt.figure()
    plt.plot(vgs, gm)
    plt.xlabel("Vgs (V)")
    plt.ylabel("gm (A/V)")
    plt.grid(True)
    plt.title(f"{base} : gm vs Vgs")
    plt.show()

    plt.figure()
    plt.plot(vgs, gm_id)
    plt.xlabel("Vgs (V)")
    plt.ylabel("gm/Id (1/V)")
    plt.grid(True)
    plt.title(f"{base} : gm/Id vs Vgs")
    plt.show()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 process_gmid.py file1 [file2 ...]")
        sys.exit(0)
    for p in sys.argv[1:]:
        try:
            process_file(p)
        except Exception as e:
            print("Error processing", p, ":", e)


if __name__ == "__main__":
    main()

