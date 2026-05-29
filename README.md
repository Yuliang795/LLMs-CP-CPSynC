# CP-SynC: Multi-Agent Zero-Shot Constraint Modeling in MiniZinc with Synthesized Checkers

This repository contains the official code and benchmark resources for the paper: **"CP-SynC: Multi-Agent Zero-Shot Constraint Modeling in MiniZinc with Synthesized Checkers"**

📄[Paper on arXiv](https://arxiv.org/abs/2605.01675)

---

## Environment Requirements

- Python 3.11

  - Install the required Python packages:

    ```bash
    pip install minizinc[dzn]
    pip install pycsp3
    pip install pandas
    ```

- Install MiniZinc locally: [MiniZinc installation guide](https://docs.minizinc.dev/en/stable/installation.html)

---

## Modeling Workflow Code

Coming soon.

---

## CP-SynC Benchmark

The benchmark contains 100 constraint programming problems across academic and industrial domains, drawn from established sources including [CSPLib](https://www.csplib.org/), [PyCSP3](https://github.com/xcsp3team/PyCSP3-models), and [CPEval](https://github.com/Yuliang795/LLMs-CP-CPEVAL). The dataset structure is:

```text
/path/to/dataset/
├── problem_specs.json
├── prob1/
│   ├── model/
│   ├── params/
│   └── sol/
└── ...
```

- `problem_specs.json` contains the metadata and problem context for each problem, including the source, problem type, natural-language problem description, input specification, and output format.
- The input instances for each problem are stored in the corresponding `params/` folder. Available instance formats include Python files, pickle files, and MiniZinc `.dzn` files.

## Evaluation

Generated solutions should be organized as follows:

```text
/path/to/generated_solutions/
├── 1/
│   └── q1_sol.pkl
├── 2/
│   └── q1_sol.pkl
└── ...
```

Each subfolder name corresponds to a problem ID. Each problem folder should contain a single generated solution file named `q1_sol.pkl` that contains the generated output solution for the corresponding benchmark problem.

To evaluate generated solutions, run:

```bash
python eval.py \
  --dataset_folder /path/to/dataset \
  --generated_solution_folder /path/to/generated_solutions \
  --output_folder /path/to/output_folder
```

The evaluation results will be written to:

```text
/path/to/output_folder/yymmdd_hhmmss/eval_res_details.csv
```

## Solution Format Checker
Coming soon

---

## Citation

```bibtex
@article{song2026cp,
  title={CP-SynC: Multi-Agent Zero-Shot Constraint Modeling in MiniZinc with Synthesized Checkers},
  author={Song, Yuliang and Cohen, Eldan},
  journal={arXiv preprint arXiv:2605.01675},
  year={2026}
}
```
