# Exact, optimality-preserving model reduction for energy system optimization

This repository implements a **three‑stage optimization framework** for large‑scale economic dispatch:

1. **Dense Full‑Resolution Model** – hourly benchmark (8760 h)  
2. **Surrogate Bounding Model** – variable bound tightening and removal
3. **Reduced Problem Model** – solve with speedup and reduced memory usage 

The framework supports **two climate years (1985, 2014)**, **five system configurations**, and **multiple temporal resolutions**.

---

## 📚 Notebooks

### 1️⃣ `01_dense_problem.ipynb`
> Full‑resolution benchmark model

**Key features**
- Hourly electricity balance  
- Transmission constraints  
- Storage dynamics  
- Optional grid tariff & storage self‑dissipation  

---

### 2️⃣ `02_surrogate.ipynb`
> Low-resolution bounding surrogate model

**Key features**
- Time aggregation (2 h – seasonal)  
- Consistent under- and over-estimation surrogates
- Automatic variable elimination  

---

### 3️⃣ `03_reduced_problem.ipynb`
> Reduced problem model

**Key features**
- Uses surrogate‑derived bounds  
- Restores full‑year objective value  
- Validates against dense model  

---

## ⚙️ Configuration

All experiments are controlled via the first cell of each notebook.

---

## 📁 Repository Structure
├── 01_dense_problem.ipynb  
├── 02_surrogate.ipynb  
├── 03_reduced_problem.ipynb  
├── utils/  
│ ├── solver_utils.py # Gurobi logging & metrics  
│ └── time_clusters.py # time aggregation  
├── data/ # input data  
├── surrogates_individual/ # variable sets reduced by surrogates & performance, appear after run  
├── logs/ # solver logs, appear after run  
├── requirements.txt  
└── README.md  

---

## 🚀 Quick Start

1. Clone repository
1. Install dependencies: `pip install -r requirements.txt`
1. Run notebooks in order (manually set weather-demand year and model configuration):
   - `01_dense_problem.ipynb`
   - `02_surrogate.ipynb`
   - `03_reduced_problem.ipynb`

Expected runtime: ~30 minutes (depending on configuration).  

⚠️ **Gurobi License Required**

`gurobipy` is **not included in `requirements.txt`** because it cannot be installed via pip.  
You must separately install Gurobi and activate a valid license.

Academic licenses are free: https://www.gurobi.com/academia/

> **Note:** While this framework is optimized for Gurobi, other solvers supported by Pyomo (e.g., HiGHS, SCIP, CPLEX) may be used with minor adjustments to the solver configuration code.

---

## 📜 License

MIT License – free for academic use.

---

## ✉️ Contact

**Zhi Gao**  
Utrecht University  
z.gao1@uu.nl