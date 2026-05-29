import asyncio
import argparse
import datetime
import importlib.util
import os
import pickle
import re
import signal
import subprocess
import sys
import json
import traceback
from pathlib import Path
from time import perf_counter, sleep
from typing import List


import pandas as pd


SOLVER_RUN_TIMEOUT = 30
SUBPROCESS_GRACE_SECONDS = 3
EVAL_RESULT_MARKER = "__CPSYNC_EVAL_RESULT__"


def infer_probs_json_path(dataset_folder):
    dataset_folder = Path(dataset_folder).resolve()
    probs_json_path = dataset_folder / "problem_specs.json"
    if not probs_json_path.is_file():
        raise FileNotFoundError(f"Expected {probs_json_path} to exist")
    return probs_json_path


def get_prob_folder(dataset_folder, prob_id):
    return Path(dataset_folder).resolve() / f"prob{prob_id}"


def get_param_dir(prob_folder, data_type):
    params_dir = Path(prob_folder) / "params"
    if data_type == "dzn" and (params_dir / "dzn").is_dir():
        return params_dir / "dzn"
    return params_dir / data_type


def load_pkl(file_path):
    with open(file_path, "rb") as f:
        return pickle.load(f)


def load_data_dict_pkl(path):
    data_dict = None
    if path is not None and Path(path).is_file():
        with open(path, "rb") as file:
            data_dict = pickle.load(file)
    return data_dict


def load_function_from_file(filepath, function_name):
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)


def load_str(file_path):
    with open(file_path, "r") as f:
        return f.read()


def kill_process_group(proc, grace_seconds=SUBPROCESS_GRACE_SECONDS):
    if proc.poll() is not None:
        return

    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    except Exception:
        proc.terminate()

    try:
        proc.wait(timeout=grace_seconds)
        return
    except subprocess.TimeoutExpired:
        pass

    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    except Exception:
        proc.kill()

    try:
        proc.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        pass


def path_is_within(path, root):
    try:
        path = Path(path).resolve()
        root = Path(root).resolve()
    except Exception:
        return False
    return path == root or root in path.parents


def find_processes_in_dir(root_dir):
    root_dir = Path(root_dir).resolve()
    current_pid = os.getpid()
    targets = []
    proc_root = Path("/proc")
    if not proc_root.is_dir():
        return targets

    for entry in proc_root.iterdir():
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        if pid == current_pid:
            continue
        try:
            cwd = Path(os.readlink(entry / "cwd"))
        except Exception:
            continue
        if not path_is_within(cwd, root_dir):
            continue
        if not is_eval_related_process(pid):
            continue
        try:
            pgid = os.getpgid(pid)
        except ProcessLookupError:
            continue
        except Exception:
            pgid = None
        targets.append((pid, pgid))
    return targets


def is_eval_related_process(pid):
    try:
        raw_cmdline = Path(f"/proc/{pid}/cmdline").read_bytes()
    except Exception:
        return False

    cmdline = raw_cmdline.replace(b"\x00", b" ").decode(errors="ignore")
    eval_markers = (
        "ACE-2.3.jar",
        "model.py -check=",
        "model.py",
        "minizinc",
        "fzn-gecode",
        "fzn-chuffed",
        "gecode",
        "chuffed",
    )
    return any(marker in cmdline for marker in eval_markers)


def kill_processes_in_dir(root_dir, grace_seconds=SUBPROCESS_GRACE_SECONDS):
    targets = find_processes_in_dir(root_dir)
    if not targets:
        return

    current_pgid = os.getpgrp()
    pgids = {pgid for _, pgid in targets if pgid and pgid != current_pgid}
    pids = {pid for pid, _ in targets}

    for pgid in pgids:
        try:
            os.killpg(pgid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

    deadline = perf_counter() + grace_seconds
    while perf_counter() < deadline:
        if not find_processes_in_dir(root_dir):
            return
        sleep(0.1)

    for pgid in pgids:
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def append_limited_text(label, text, max_chars=4000):
    if not text:
        return ""
    text = str(text)
    if len(text) > max_chars:
        text = text[-max_chars:]
    return f"{label}:\n{text}"


def get_q_from_path(path, data_type):
    ext = {"dzn": "dzn", "pickle": "pkl"}[data_type]
    match = re.search(fr"_q(\d+).*\.{ext}$", Path(path).name)
    if not match:
        raise ValueError(f"Could not infer q id from {path}")
    return int(match.group(1))


def get_param_path_by_q(dataset_folder, prob_id, data_type):
    return {
        get_q_from_path(path, data_type): path
        for path in get_param_path(dataset_folder, prob_id, data_type=data_type)
    }



def str2bool(value):
    if isinstance(value, bool):
        return value
    value = value.lower()
    if value in {"true", "1", "yes", "y", "on"}:
        return True
    if value in {"false", "0", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Expected a boolean value, got {value!r}")


def get_param_path(dataset_folder, prob_id, data_type="dzn") -> List[str]:
    # return a list of param paths
    data_type_ext = {"dzn": "dzn", "pickle": "pkl"}
    curr_inst_folder_path = get_param_dir(get_prob_folder(dataset_folder, prob_id), data_type)
    curr_inst_path_list = []
    if os.path.exists(curr_inst_folder_path):
        curr_inst_path_list = [
            entry.path
            for entry in os.scandir(curr_inst_folder_path)
            if entry.is_file() and re.search(fr"_q\d+\.{data_type_ext[data_type]}$", entry.name)
        ]

    if len(curr_inst_path_list)>0:
        curr_inst_path_list.sort(key=lambda filename: int(re.search(fr"_q(\d+)\.{data_type_ext[data_type]}$", filename).group(1)))
    #
    return curr_inst_path_list


def get_solution_paths(prob_solution_dir):
    sol_paths = []
    for entry in os.scandir(prob_solution_dir):
        if not entry.is_file():
            continue
        match = re.fullmatch(r"q(\d+)_sol\.pkl", entry.name)
        if match:
            sol_paths.append((int(match.group(1)), Path(entry.path)))

    sol_paths.sort(key=lambda x: x[0])
    return sol_paths

def get_mzn_model_instance(mzn_path, dzn_path=None, eval_dvar_dzn_path=None, solver_tag="gecode"):
    from minizinc import Instance, Model, Solver

    model = Model(mzn_path)
    if dzn_path:
        model.add_file(dzn_path)
    if eval_dvar_dzn_path:
        model.add_file(eval_dvar_dzn_path)
    solver = Solver.lookup(solver_tag)
    return Instance(solver, model)


def org_mzn_error_msg(e):
    if not hasattr(e, "location") or not e.location:
        return f"Error: {e}"

    loc = e.location
    file_path = loc.file
    start_line = loc.lines[0]
    start_column = loc.columns[0]
    end_column = loc.columns[1]

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            error_line = lines[start_line - 1].rstrip("\n")
    except Exception as file_error:
        return f"Could not read file {file_path}: {file_error}\nError: {e}"

    return (
        f"model.mzn:{start_line}.{start_column}-{end_column}:\n"
        f"{error_line}\n"
        f"{' ' * (start_column - 1)}{'^' * (end_column - start_column + 1)}\n"
        f"Error: {e}"
    )


async def solve_instance_dvar(
    mzn_path,
    dzn_path=None,
    dvar_dict=None,
    check="sat",
    opt_check_str_path=None,
    solver_tag="gecode",
    all_solutions=False,
    exec_timeout=SOLVER_RUN_TIMEOUT,
):
    exec_timeout = datetime.timedelta(seconds=exec_timeout)
    decision_var_dict = {}
    error_msg, out_msg = "", ""
    cmd_args = f"minizinc {mzn_path} {dzn_path} --output-mode json"
    try:
        instance = get_mzn_model_instance(mzn_path, dzn_path=dzn_path, solver_tag=solver_tag)
        if check == "sat":
            for dvar_name, dvar_value in dvar_dict.items():
                instance[dvar_name] = dvar_value
        elif check == "opt":
            opt_check_str = load_str(opt_check_str_path).format(**dvar_dict)
            instance.add_string(opt_check_str)
        result = await instance.solve_async(timeout=exec_timeout, all_solutions=all_solutions)
    except Exception as e:
        return "", org_mzn_error_msg(e), "Error_", cmd_args, decision_var_dict

    if result.solution is not None:
        decision_var_dict = {k: v for k, v in result.solution.__dict__.items() if k != "_checker"}
        if "_output_item" in decision_var_dict:
            out_msg = decision_var_dict["_output_item"]

    return out_msg, error_msg, result.status.name, cmd_args, decision_var_dict


def get_dataset_checker_path(dataset_folder, problem_id):
    return get_prob_folder(dataset_folder, problem_id) / "model" / "model.py"


def run_model_checker(python_exec, script_path, script_args, run_dir, timeout=SOLVER_RUN_TIMEOUT):
    """
    Returns:
        A tuple (stdout, error_type, error_message):
        - On success: (stdout_string, None, None)
        - On timeout: (partial_stdout_string, 'timeout', None)
        - On other exceptions: (None, 'execution_error', error_details_string)
    """
    assert os.path.exists(run_dir), f"PYCSP3 Eval | Run directory does not exist: {run_dir}"
    cmd = [python_exec, script_path] + script_args
    proc = None
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=run_dir,
            start_new_session=True,
        )
        stdout, stderr = proc.communicate(timeout=timeout)
        kill_processes_in_dir(run_dir)
        stdout = (stdout or "").strip()
        stderr = (stderr or "").strip()
        if proc.returncode != 0 and stderr:
            return stdout, "exe_error", stderr
        return stdout, None, None
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        error_output = exc.stderr or ""
        if proc is not None:
            kill_process_group(proc)
            kill_processes_in_dir(run_dir)
            stdout, stderr = proc.communicate()
            output = output or stdout or ""
            error_output = error_output or stderr or ""
        error_msg = "\n".join(
            msg for msg in [
                f"Timed out after {timeout}s",
                append_limited_text("stdout", output),
                append_limited_text("stderr", error_output),
            ]
            if msg
        )
        return str(output).strip(), "timeout", error_msg
    except Exception as e:
        return None, "exe_error", str(e)


def parse_checker_output(output, prefix):
    """
    Extracts the result keyword (SAT, UNSAT, OPT, SUBOPT) after the given prefix@.
    Handles cases where the output is like 'sat@SATxxx' or has no whitespace separation.
    Returns (result, error_type, error_message).
    """
    if not output:
        return None, "parse_error", "Checker No Output."

    pattern = rf"{prefix}@(SAT|UNSAT|OPT|SUBOPT)"
    match = re.search(pattern, output)
    if match:
        return match.group(1), None, None
    
    # If keyword not found, treat the whole output as an error message
    return None, "parse_error", output


def eval_pycsp3_model(
    checker_py_path,
    param_pkl_path,
    ovar_path,
    problem_type="csp",
    python_exec=sys.executable,
    timeout=SOLVER_RUN_TIMEOUT,
):
    """
    Returns (sat_result, opt_result).
    """
    run_dir = os.path.dirname(os.path.abspath(ovar_path))
    sat_args = [f"-check=sat", f"-param={param_pkl_path}", f"-ovar={ovar_path}"]
    sat_raw_output, run_err_type, run_err_msg = run_model_checker(
        python_exec, checker_py_path, sat_args, run_dir, timeout
    )

    # Handle execution errors (timeout, subprocess error)
    if run_err_type:
        return "", "", run_err_type, run_err_msg

    # Parse the output from a successful run
    sat_status, parse_err_type, parse_err_msg = parse_checker_output(sat_raw_output, "sat")
    
    # Handle incorrect output format
    if parse_err_type:
        return "", "", parse_err_type, parse_err_msg

    # --- 2. EARLY EXIT FOR CSP PROBLEMS --- | # Success, no error
    if problem_type == "csp":
        return sat_status, "", None, None

    # For COP: only check opt if sat is SAT
    opt_status = ""
    if sat_status in ["SAT", "OPTIMUM"]:
        opt_args = [
            f'-check=opt',
            f'-param={param_pkl_path}',
            f'-ovar={ovar_path}'
        ]
        opt_raw, run_err_type, run_err_msg = run_model_checker(
            python_exec, checker_py_path, opt_args, run_dir, timeout
        )
        # Handle execution errors for the OPT check
        if run_err_type:
            return sat_status, "", run_err_type, run_err_msg or ""

        # Parse the output from the OPT check
        opt_status, parse_err_type, parse_err_msg = parse_checker_output(opt_raw, "opt")

        # Handle incorrect output format for the OPT check
        if parse_err_type:
            return sat_status, "", parse_err_type, parse_err_msg

    return sat_status, opt_status, None, None # Success


async def eval_mzn_model(
    ref_mzn_path,
    dzn_path,
    ovar_path=None,
    ovar_transformer_path=None,
    opt_check_str_path=None,
    param_pkl_path=None,
    solver_tag="gecode",
    problem_type="csp",
    timeout=SOLVER_RUN_TIMEOUT,
):
    """
    Returns (sat_status, opt_status, err_type, err_msg), matching PyCSP3 model_eval.
    """
    ovar_transformer_func = load_function_from_file(ovar_transformer_path, "ovar_transformer")
    param_dict = load_data_dict_pkl(param_pkl_path)
    try:
        ovar_dict = load_pkl(ovar_path)
        formated_dvar_dict = ovar_transformer_func(ovar_dict, param_dict)
    except Exception as e:
        error_type = type(e).__name__
        tb_str = traceback.format_exc()
        return "", "", "Error_", (
            f"ovar_transformer_func error:\n"
            f"Type: {error_type}\n"
            f"Message: {e}\n"
            f"Traceback:\n{tb_str}"
        )

    out_msg, error_msg, sat_status_raw, cmd_args, decision_var_dict = await solve_instance_dvar(
        mzn_path=ref_mzn_path,
        dzn_path=dzn_path,
        dvar_dict=formated_dvar_dict,
        solver_tag=solver_tag,
        all_solutions=False,
        exec_timeout=timeout,
        check="sat",
    )

    if sat_status_raw == "Error_":
        return "", "", "Error_", error_msg
    if sat_status_raw in ["UNSATISFIABLE"]:
        sat_status = "UNSAT"
    elif sat_status_raw in ["OPTIMAL_SOLUTION", "SATISFIED"]:
        sat_status = "SAT"
    else:
        return "", "", "Others", f"MiniZinc status: {sat_status_raw}"

    if problem_type == "cop" and sat_status in ["SAT"]:
        out_msg, error_msg, opt_status_raw, cmd_args, decision_var_dict = await solve_instance_dvar(
            mzn_path=ref_mzn_path,
            dzn_path=dzn_path,
            dvar_dict=formated_dvar_dict,
            solver_tag=solver_tag,
            all_solutions=False,
            exec_timeout=timeout,
            check="opt",
            opt_check_str_path=opt_check_str_path,
        )

        if opt_status_raw == "Error_":
            return sat_status, "", "Error_", error_msg
        if opt_status_raw in ["UNSATISFIABLE"]:
            opt_status = "OPT"
        elif opt_status_raw in ["OPTIMAL_SOLUTION", "SATISFIED"]:
            opt_status = "SUBOPT"
        else:
            return sat_status, "", "Others", f"MiniZinc status (opt): {opt_status_raw}"
        return sat_status, opt_status, None, None

    return sat_status, "", None, None


def safe_resolve(path):
    return Path(path).resolve() if path else None


def get_prob_type(prob_id, probs_json_path):
    with open(probs_json_path, "r") as f:
        probs = json.load(f)

    if str(prob_id) not in probs:
        raise KeyError(f"Problem id {prob_id} not found in {probs_json_path}")

    return probs[str(prob_id)]["type"]


async def eval_solution(dataset_folder, prob_id, hyp_out_path, prob_type, param_path_dict, timeout=SOLVER_RUN_TIMEOUT):
    

    if int(prob_id) > 30:
        sat_, opt_, error_, error_msg_ = eval_pycsp3_model(
            checker_py_path=get_dataset_checker_path(dataset_folder, prob_id),
            param_pkl_path=param_path_dict['pkl'],
            ovar_path=hyp_out_path,
            problem_type=prob_type,
            timeout=timeout,
        )
    else:
        prob_folder = get_prob_folder(dataset_folder, prob_id)
        ovar_transformer_path = prob_folder / "model" / "ovar_transformer.py"
        ref_mzn_model_path = prob_folder / "model" / f"prob{prob_id}_ref1.mzn"
        dzn_param_path = param_path_dict['dzn']
        opt_check_str_path = prob_folder / "model" / f"prob{prob_id}_opt_check"

        sat_, opt_, error_, error_msg_ = await eval_mzn_model(
            ref_mzn_path=ref_mzn_model_path,
            dzn_path=dzn_param_path,
            ovar_path=hyp_out_path,
            ovar_transformer_path=ovar_transformer_path,
            param_pkl_path=param_path_dict['pkl'],
            problem_type=prob_type,
            opt_check_str_path=opt_check_str_path,
            timeout=timeout,
        )

    return sat_, opt_, error_, error_msg_


async def run_single_eval(args):
    param_path_dict = {
        "pkl": args.param_pkl,
        "dzn": args.param_dzn,
    }
    payload = {
        "sat": "",
        "opt": "",
        "error": None,
        "error_msg": None,
    }
    try:
        sat, opt, error, error_msg = await eval_solution(
            dataset_folder=args.dataset_folder,
            prob_id=args.prob_id,
            hyp_out_path=args.hyp_out_path,
            prob_type=args.prob_type,
            param_path_dict=param_path_dict,
            timeout=args.timeout,
        )
        payload.update({
            "sat": sat,
            "opt": opt,
            "error": error,
            "error_msg": error_msg,
        })
    except Exception as e:
        payload.update({
            "error": type(e).__name__,
            "error_msg": f"{e}\n{traceback.format_exc()}",
        })

    print(f"{EVAL_RESULT_MARKER}{json.dumps(payload, ensure_ascii=False)}")


def parse_single_eval_payload(stdout):
    payload_lines = [
        line[len(EVAL_RESULT_MARKER):]
        for line in (stdout or "").splitlines()
        if line.startswith(EVAL_RESULT_MARKER)
    ]
    if not payload_lines:
        return None
    return json.loads(payload_lines[-1])


def eval_solution_subprocess(
    dataset_folder,
    prob_id,
    hyp_out_path,
    prob_type,
    param_path_dict,
    timeout=SOLVER_RUN_TIMEOUT,
):
    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--single-run",
        "--dataset_folder", str(dataset_folder),
        "--prob_id", str(prob_id),
        "--hyp_out_path", str(hyp_out_path),
        "--prob_type", str(prob_type),
        "--param_pkl", str(param_path_dict["pkl"]),
        "--timeout", str(timeout),
    ]
    if param_path_dict.get("dzn"):
        cmd.extend(["--param_dzn", str(param_path_dict["dzn"])])

    guard_timeout = timeout * 2 + 15 if prob_type == "cop" else timeout + 15
    proc = None
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        stdout, stderr = proc.communicate(timeout=guard_timeout)
        kill_processes_in_dir(Path(hyp_out_path).resolve().parent)
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if proc is not None:
            kill_process_group(proc)
            kill_processes_in_dir(Path(hyp_out_path).resolve().parent)
            extra_stdout, extra_stderr = proc.communicate()
            stdout = stdout or extra_stdout or ""
            stderr = stderr or extra_stderr or ""
        error_msg = "\n".join(
            msg for msg in [
                f"Instance evaluator timed out after {guard_timeout}s",
                append_limited_text("stdout", stdout),
                append_limited_text("stderr", stderr),
            ]
            if msg
        )
        return "", "", "timeout", error_msg
    except Exception as e:
        return "", "", "subprocess_error", f"{e}\n{traceback.format_exc()}"

    payload = None
    try:
        payload = parse_single_eval_payload(stdout)
    except Exception as e:
        return "", "", "parse_error", f"Could not parse child result: {e}\n{stdout}\n{stderr}"

    if payload is None:
        error_parts = [
            f"Child exited with return code {proc.returncode}",
            append_limited_text("stdout", stdout),
            append_limited_text("stderr", stderr),
        ]
        return "", "", "subprocess_error", "\n".join(part for part in error_parts if part)

    if proc.returncode != 0 and not payload.get("error"):
        payload["error"] = "subprocess_error"
        payload["error_msg"] = "\n".join(
            part for part in [
                f"Child exited with return code {proc.returncode}",
                append_limited_text("stderr", stderr),
            ]
            if part
        )

    return (
        payload.get("sat") or "",
        payload.get("opt") or "",
        payload.get("error"),
        payload.get("error_msg"),
    )


def get_para_path_dict(dataset_folder, prob_id):
    pkl_inst_path_list = get_param_path(
        dataset_folder=dataset_folder,
        prob_id=prob_id,
        data_type="pickle",
    )

    dzn_inst_path_list = get_param_path(
        dataset_folder=dataset_folder,
        prob_id=prob_id,
        data_type="dzn",
    )

    # no instances -> single solution problem
    if not pkl_inst_path_list:
        return None

    return {
        "pkl": pkl_inst_path_list,
        "dzn": dzn_inst_path_list,
    }


async def evaluate_all(
    dataset_folder,
    generated_solution_folder,
    output_folder,
    timeout=SOLVER_RUN_TIMEOUT,
    first_instance_only=True,
):
    summary_records = []
    detail_records = []

    dataset_folder = Path(dataset_folder).resolve()
    generated_solution_folder = Path(generated_solution_folder).resolve()
    probs_json = infer_probs_json_path(dataset_folder)
    output_folder = Path(output_folder).resolve()

    run_dir = output_folder / datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    
    #
    summary_csv = run_dir / "eval_res_summary.csv"
    detail_csv = run_dir / "eval_res_details.csv"

    root = generated_solution_folder
    if not root.is_dir():
        raise FileNotFoundError(f"Generated solution folder does not exist: {root}")

    subfolders = sorted(
        [p for p in root.iterdir() if p.is_dir() and p.name.isdigit()],
        key=lambda p: int(p.name)
    )

    for sub in subfolders:
        prob_id = sub.name
        prob_type = None
        instance_pass_list = []

        try:
            prob_type = get_prob_type(prob_id, probs_json).lower()
            pkl_inst_path_by_q = get_param_path_by_q(
                dataset_folder=dataset_folder,
                prob_id=prob_id,
                data_type="pickle",
            )
            dzn_inst_path_by_q = get_param_path_by_q(
                dataset_folder=dataset_folder,
                prob_id=prob_id,
                data_type="dzn",
            )

            q_values = [1] if first_instance_only and 1 in pkl_inst_path_by_q else sorted(pkl_inst_path_by_q)

            for q in q_values:
                pkl_inst_path = pkl_inst_path_by_q[q]
                hyp_out_path = sub / f"q{q}_sol.pkl"

                sat, opt = None, None
                error, error_msg = None, None
                eval_res = 0
                eval_time = 0.0
                eval_start_time = perf_counter()

                try:
                    param_path_dict = {
                        "pkl": pkl_inst_path,
                        "dzn": dzn_inst_path_by_q.get(q),
                    }

                    if int(prob_id) <= 30 and param_path_dict["dzn"] is None:
                        raise FileNotFoundError(f"Missing dzn params for prob{prob_id} q{q}")

                    if not hyp_out_path.exists():
                        error = "missing"
                        error_msg = f"q{q}_sol.pkl not found"
                    else:
                        sat, opt, error, error_msg = eval_solution_subprocess(
                            dataset_folder=dataset_folder,
                            prob_id=prob_id,
                            hyp_out_path=str(hyp_out_path),
                            prob_type=prob_type,
                            param_path_dict=param_path_dict,
                            timeout=timeout,
                        )

                        eval_res = 0
                        if prob_type == "cop" and opt == "OPT":
                            eval_res = 1
                        if prob_type == "csp" and sat == "SAT":
                            eval_res = 1

                except Exception as e:
                    error = type(e).__name__
                    error_msg = f"{e}\n{traceback.format_exc()}"
                finally:
                    eval_time = round(perf_counter() - eval_start_time, 2)

                instance_pass_list.append(eval_res)

                detail_records.append([
                    prob_id, q, prob_type, sat, opt, eval_res, eval_time, error, error_msg
                ])

            num_instance_passed = sum(instance_pass_list)
            num_instance = len(instance_pass_list)
            instance_pass_rate = (
                num_instance_passed / num_instance
                if num_instance > 0 else 0
            )
            summary_records.append([
                prob_id, prob_type, num_instance_passed, num_instance, round(instance_pass_rate,3), instance_pass_list
            ])


            print(
                f"✅ Evaluated prob {prob_id} ({prob_type}): "
                f"instance_pass_rate: {round(instance_pass_rate,3)}"
            )

        except Exception as e:
            tb_str = traceback.format_exc()
            summary_records.append([prob_id, prob_type, 0, 0, 0, []])
            detail_records.append([
                prob_id, None, prob_type, None, None, 0, 0.0, type(e).__name__, tb_str
            ])
            print(f"❌ Error evaluating prob {prob_id}: {e}")
            print(tb_str)

    ## Output to csv
    #
    summary_df = pd.DataFrame(
        summary_records,
        columns=["prob_id", "prob_type", 'num_instance_passed', 'num_instance', "instance_pass_rate", "instance_pass_list"]
    )
    summary_df.to_csv(summary_csv, index=False)
    #
    detail_df = pd.DataFrame(
        detail_records,
        columns=["prob_id", "q", "prob_type", "sat", "opt", "eval_res", "eval_time", "error", "error_msg"]
    )
    detail_df.to_csv(detail_csv, index=False)

    ###

    print(f"\n📄 Summary results saved to {summary_csv}")
    print(f"📄 Detail results saved to {detail_csv}")

    return summary_csv, detail_csv



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("positional", nargs="*", help=argparse.SUPPRESS)
    parser.add_argument(
        "--dataset_folder",
        help="Path to the CPSYNC dataset folder",
    )
    parser.add_argument(
        "--generated_solution_folder",
        help="Path to the generated solution folder",
    )
    parser.add_argument(
        "--output_folder",
        default="eval_res",
        help="Base output folder. A yymmdd_hhmmss subfolder will be created under it.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=SOLVER_RUN_TIMEOUT,
        help="Timeout in seconds for each SAT/OPT checker call.",
    )
    parser.add_argument(
        "--first_instance_only",
        default=True,
        type=str2bool,
        help="If true, evaluate only q1 for each problem instead of all instances. Default: true.",
    )
    parser.add_argument("--single-run", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--prob_id", help=argparse.SUPPRESS)
    parser.add_argument("--hyp_out_path", help=argparse.SUPPRESS)
    parser.add_argument("--prob_type", choices=["csp", "cop"], help=argparse.SUPPRESS)
    parser.add_argument("--param_pkl", help=argparse.SUPPRESS)
    parser.add_argument("--param_dzn", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if len(args.positional) > 3:
        parser.error("Expected at most 3 positional arguments: dataset_folder generated_solution_folder [output_folder]")

    if args.dataset_folder is None and len(args.positional) >= 1:
        args.dataset_folder = args.positional[0]
    if args.generated_solution_folder is None and len(args.positional) >= 2:
        args.generated_solution_folder = args.positional[1]
    if args.output_folder == "eval_res" and len(args.positional) >= 3:
        args.output_folder = args.positional[2]

    if args.single_run:
        required = ["dataset_folder", "prob_id", "hyp_out_path", "prob_type", "param_pkl"]
        missing = [name for name in required if not getattr(args, name)]
        if missing:
            parser.error(f"Missing required single-run arguments: {', '.join(missing)}")
        del args.positional
        return args

    if not args.dataset_folder or not args.generated_solution_folder:
        parser.error("dataset_folder and generated_solution_folder are required")

    del args.positional
    return args


def main():
    args = parse_args()
    if args.single_run:
        asyncio.run(run_single_eval(args))
        return

    output_csv = asyncio.run(
        evaluate_all(
            args.dataset_folder,
            args.generated_solution_folder,
            args.output_folder,
            timeout=args.timeout,
            first_instance_only=args.first_instance_only,
        )
    )
    print(output_csv)


if __name__ == "__main__":
    main()
