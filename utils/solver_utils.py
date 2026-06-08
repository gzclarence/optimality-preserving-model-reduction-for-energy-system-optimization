import os, re, time
import psutil, os

process = psutil.Process(os.getpid())

def get_rss_GB():
    """Resident Set Size (actual RAM in use)"""
    return process.memory_info().rss / 1e9

def pyomo_model_stats(m):
    """Basic model size from Pyomo (pre-presolve)."""
    try:
        return {
            "pyomo_nvars": int(m.nvariables()),
            "pyomo_ncons": int(m.nconstraints()),
            "pyomo_nobjs": int(m.nobjectives()),
        }
    except Exception:
        return {"pyomo_nvars": None, "pyomo_ncons": None, "pyomo_nobjs": None}

import os, re

def parse_gurobi_barrier_log(logfile):
    """
    Parse a Gurobi log written by LogFile option (Barrier / Method=2).
    Extract model size, presolve stats, barrier linear-algebra stats,
    iteration table last row (primal/dual/residual/compl), and final barrier summary.

    Designed to match logs like:
      - "Optimize a model with ... rows, ... columns and ... nonzeros"
      - "Presolve removed ... rows and ... columns"
      - "Presolved: ... rows, ... columns, ... nonzeros"
      - "Barrier statistics: AA' NZ : ..., Factor NZ : ..., Factor Ops : ..."
      - barrier iteration table
      - "Barrier solved model in ... iterations and ... seconds (... work units)"
    """
    out = {
        # Original model size
        "model_rows_log": None,
        "model_cols_log": None,
        "model_nz_log": None,

        # Presolve summary
        "gurobi_presolve_removed_rows": None,
        "gurobi_presolve_removed_cols": None,
        "gurobi_presolve_removed_nz": None,   # only appears in some formats
        "presolve_time_s_log": None,
        "presolved_rows_log": None,
        "presolved_cols_log": None,
        "presolved_nz_log": None,
        "ordering_time_s_log": None,

        # Barrier stats (linear algebra proxies)
        "barrier_AAt_NZ_log": None,     # AA' NZ
        "barrier_factor_NZ_log": None,  # Factor NZ
        "barrier_factor_ops_log": None, # Factor Ops
        "barrier_threads_log": None,
        "barrier_factor_mem_GB_log": None, # parsed "(roughly X GB of memory)" if present

        # Barrier summary
        "barrier_iters_log": None,
        "barrier_time_s_log": None,
        "barrier_work_units_log": None,

        # Final iteration snapshot from iteration table
        "final_primal_obj_log": None,
        "final_dual_obj_log": None,
        "final_primal_inf_log": None,   # "Primal" residual column in Gurobi output
        "final_dual_inf_log": None,     # "Dual" residual column in Gurobi output
        "final_comp_log": None,
        "final_iter_time_s_log": None,
    }

    if not os.path.exists(logfile):
        return out

    txt = open(logfile, "r", encoding="utf-8", errors="ignore").read()

    # --- Original model size ---
    m = re.findall(r"Optimize a model with\s+(\d+)\s+rows,\s+(\d+)\s+columns\s+and\s+(\d+)\s+nonzeros", txt)
    if m:
        out["model_rows_log"] = int(m[-1][0])
        out["model_cols_log"] = int(m[-1][1])
        out["model_nz_log"] = int(m[-1][2])

    # --- Presolve removed rows/cols/nz ---
    m = re.findall(r"Presolve removed\s+(\d+)\s+rows\s+and\s+(\d+)\s+columns\s+and\s+(\d+)\s+nonzeros", txt)
    if m:
        out["gurobi_presolve_removed_rows"] = int(m[-1][0])
        out["gurobi_presolve_removed_cols"] = int(m[-1][1])
        out["gurobi_presolve_removed_nz"] = int(m[-1][2])
    else:
        m = re.findall(r"Presolve removed\s+(\d+)\s+rows\s+and\s+(\d+)\s+columns", txt)
        if m:
            out["gurobi_presolve_removed_rows"] = int(m[-1][0])
            out["gurobi_presolve_removed_cols"] = int(m[-1][1])

    # Presolve time
    m = re.findall(r"Presolve time:\s*([0-9\.]+)s", txt)
    if m:
        out["presolve_time_s_log"] = float(m[-1])

    # Presolved size
    m = re.findall(r"Presolved:\s+(\d+)\s+rows,\s+(\d+)\s+columns,\s+(\d+)\s+nonzeros", txt)
    if m:
        out["presolved_rows_log"] = int(m[-1][0])
        out["presolved_cols_log"] = int(m[-1][1])
        out["presolved_nz_log"] = int(m[-1][2])

    # Ordering time
    m = re.findall(r"Ordering time:\s*([0-9\.]+)s", txt)
    if m:
        out["ordering_time_s_log"] = float(m[-1])

    # --- Barrier statistics ---
    # AA' NZ
    m = re.findall(r"AA'\s*NZ\s*:\s*([0-9\.eE\+\-]+)", txt)
    if m:
        out["barrier_AAt_NZ_log"] = float(m[-1])

    # Factor NZ
    m = re.findall(r"Factor\s+NZ\s*:\s*([0-9\.eE\+\-]+)\s*\(roughly\s*([0-9\.]+)\s*GB of memory\)", txt)
    if m:
        out["barrier_factor_NZ_log"] = float(m[-1][0])
        out["barrier_factor_mem_GB_log"] = float(m[-1][1])

    # Factor Ops
    m = re.findall(r"Factor\s+Ops\s*:\s*([0-9\.eE\+\-]+)", txt)
    if m:
        out["barrier_factor_ops_log"] = float(m[-1])

    # Threads
    m = re.findall(r"Threads\s*:\s*(\d+)", txt)
    if m:
        out["barrier_threads_log"] = int(m[-1])

    # --- Barrier solved summary ---
    # Example: "Barrier solved model in 50 iterations and 76.65 seconds (96.79 work units)"
    m = re.findall(
        r"Barrier solved model in\s+(\d+)\s+iterations\s+and\s+([0-9\.]+)\s+seconds\s+\(([0-9\.]+)\s+work units\)",
        txt
    )
    if m:
        out["barrier_iters_log"] = int(m[-1][0])
        out["barrier_time_s_log"] = float(m[-1][1])
        out["barrier_work_units_log"] = float(m[-1][2])
    else:
        # fallback if work units not printed
        m = re.findall(r"Barrier solved model in\s+(\d+)\s+iterations\s+and\s+([0-9\.]+)\s+seconds", txt)
        if m:
            out["barrier_iters_log"] = int(m[-1][0])
            out["barrier_time_s_log"] = float(m[-1][1])

    # --- Iteration table: capture last iteration row ---
    # Table row format in your log:
    # Iter  PrimalObj  DualObj  PrimalRes  DualRes  Compl  Time
    lines = txt.splitlines()
    iter_lines = []
    for ln in lines:
        # Match: iter + 6 numeric columns (primal, dual, primalres, dualres, compl, time-with-s)
        # Time is shown like "75s" so accept digits + 's'
        if re.match(r"^\s*\d+\s+[-+0-9\.eE]+\s+[-+0-9\.eE]+\s+[-+0-9\.eE]+\s+[-+0-9\.eE]+\s+[-+0-9\.eE]+\s+\d+s\s*$", ln):
            iter_lines.append(ln)

    if iter_lines:
        last = iter_lines[-1].split()
        try:
            out["final_primal_obj_log"] = float(last[1])
            out["final_dual_obj_log"] = float(last[2])
            out["final_primal_inf_log"] = float(last[3])
            out["final_dual_inf_log"] = float(last[4])
            out["final_comp_log"] = float(last[5])
            # strip trailing 's'
            out["final_iter_time_s_log"] = float(last[6].replace("s",""))
        except Exception:
            pass

    return out

def solve_with_gurobi_logging(pyomo_model, solver, log_path, options):
    """Run solve with Gurobi log file and return (results, metrics_dict)."""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Ensure log is fresh
    if os.path.exists(log_path):
        os.remove(log_path)

    # Jupyter-friendly wall clock
    t0 = time.time()

    # Make sure LogFile is passed (Pyomo forwards these to Gurobi)
    opts = dict(options)
    opts["LogFile"] = log_path

    mem_before = get_rss_GB()

    results = solver.solve(pyomo_model, tee=True, options=opts)

    wall = time.time() - t0

    mem_after = get_rss_GB()

    # Extract basic solver stats Pyomo gives you
    try:
        solver_wall = float(results['Solver'][0]['Wall time'])
    except Exception:
        solver_wall = None

    try:
        obj_lb = results['Problem'][0]['Lower bound']
    except Exception:
        obj_lb = None

    metrics = {
        "wall_time_py": wall,
        "solver_wall_time_reported": solver_wall,
        "reported_lower_bound": obj_lb,
    }

    metrics["rss_before_GB"] = mem_before
    metrics["rss_after_GB"] = mem_after
    metrics["rss_delta_GB"] = mem_after - mem_before

    metrics.update(pyomo_model_stats(pyomo_model))
    metrics.update(parse_gurobi_barrier_log(log_path))


    return results, metrics