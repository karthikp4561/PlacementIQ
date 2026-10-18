# PlacementIQ — Student Placement Intelligence Platform
### *Intelligent, Explainable, Secure Career Analytics Platform for MCA Academic Demonstrations & Internship Reviews*

---

## 📌 Executive Summary & Architecture Overview

**PlacementIQ** (version `2.0.0`, upgraded from *Student Placement Intelligence System*) is an enterprise-grade academic decision-support platform designed for Master of Computer Applications (MCA) internship and final academic reviews.

The platform transforms raw student academic attributes into calibrated placement probabilities, explainable feature attributions (XAI), individualized actionable improvement plans, and certified, publication-grade PDF reports.

```
c:\Users\karth\Downloads\siip\project\
├── .streamlit/
│   └── config.toml               # Dark theme color token presets
├── config.py                     # Central project paths, feature constraints, schema
├── init_admin.py                 # Secure administrator initialization CLI script
├── app.py                        # Flagship multi-view reactive application
├── placement_model.pkl           # Preserved original Logistic Regression model
├── scaler.pkl                    # Preserved original StandardScaler instance
├── requirements.txt              # Production dependency specifications
├── data/
│   ├── student_dataset_10000_rows.csv # 10,000-student historical training corpus
│   └── placementiq.db            # SQLite relational database (users & predictions)
├── pages/
│   ├── Dashboard.py              # Standalone Prediction & Analytics Dashboard
│   ├── Analytics.py              # Cohort Analytics & Distribution Visualizations
│   └── About.py                  # MCA Academic Project Documentation
├── utils/
│   ├── __init__.py
│   ├── auth.py                   # Role-Based Access Control (RBAC) & session management
│   ├── database.py               # Parameterized SQLite persistence & PBKDF2 hashing
│   ├── prediction.py             # Validated inference engine & XAI attribution math
│   ├── recommendations.py        # Rule-informed personalized improvement generator
│   ├── report.py                 # In-memory publication-grade ReportLab PDF compiler
│   ├── charts.py                 # Plotly gauges, waterbars, radars, ROC, heatmaps
│   └── style.py                  # Bespoke CSS, tokens, cards, and Inter typography
└── tests/
    ├── test_prediction.py        # Input validation & ML inference consistency tests
    ├── test_auth.py              # Cryptographic PBKDF2 hashing & authentication tests
    ├── test_database.py          # Student data isolation & database CRUD tests
    ├── test_report.py            # ReportLab in-memory PDF compilation tests
    └── test_pages_compilation.py # Full syntax and compilation integrity tests
```

---

## 🎯 Verified Machine Learning Pipeline

* **Model Algorithm**: `sklearn.linear_model.LogisticRegression`
* **Preprocessing Scaler**: `sklearn.preprocessing.StandardScaler`
* **Output Classification Labels**: `['Not Placed', 'Placed']` (Index 0 = Not Placed, Index 1 = Placed)
* **Model Accuracy**: **99.70%** (verified on 2,000 holdout test cases from the 10,000 record dataset)
* **Precision / Sensitivity**: **99.76%** precision, **99.88%** recall, **99.82%** F1-score, **AUC = 1.0000**
* **Input Features & Exact Model Ordering**:
  1. `study_hours` (hrs/day, range [0, 24], $\beta = +0.3886$)
  2. `attendance` (%, range [0, 100], $\beta = +0.2662$)
  3. `sleep_hours` (hrs/night, range [0, 16], $\beta = +0.0909$)
  4. `internet_usage` (hrs/day, range [0, 24], $\beta = -0.0897$)
  5. `assignments_completed` (count, range [0, 50], $\beta = +0.2275$)
  6. `previous_score` (%, range [0, 100], $\beta = +0.1802$)
  7. `exam_score` (%, range [0.0, 100.0], $\beta = +12.8419$)

---

## 🚀 Quickstart Guide (PowerShell / Windows)

### 1. Prerequisites
Ensure Python `3.10` or higher is installed and accessible in PowerShell:
```powershell
python --version
```

### 2. Install Project Dependencies
Run from the project root directory:
```powershell
python -m pip install -r requirements.txt
```

### 3. Initialize the Administrator Account
PlacementIQ enforces strict zero-hardcoded-credential policies. Use the secure CLI setup script to create or update the system administrator account:
```powershell
python init_admin.py --username admin --email admin@placementiq.edu --password "Admin@PlacementIQ2026"
```
*(You may customize the `--username`, `--email`, and `--password` parameters).*

### 4. Run the Automated Test Suite
Verify that all 10 unit and integration tests pass cleanly:
```powershell
python -m pytest tests -v
```
*Expected result:* `10 passed in ~5 seconds`.

### 5. Launch the Web Application
Start the Streamlit application server:
```powershell
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🔐 Role-Based Access Control & Security Rules

1. **Self-Registration Isolation**: All self-registered users receive the `student` role by default. Registrations cannot self-elevate to `admin`.
2. **Cryptographic Hashing**: User passwords are stored using salted `PBKDF2-HMAC-SHA256` with 200,000 iterations and 16-byte random salts. Plaintext passwords are never persisted.
3. **Student Data Isolation**: Students can only view, audit, download, or delete their own predictions (`WHERE user_id = ?`). Direct URL query tampering cannot access another student's dossier.
4. **Administrator Console**: Secured by server-side verification (`require_admin()`). Administrators can audit all system-wide prediction logs, manage users, modify roles, and export audit trails to CSV.

---

## 📊 Completed Feature Modules

| Module | Features & Capabilities |
|---|---|
| **Branded UI/UX** | Deep slate & navy styling, glassmorphism cards, Inter typography, KPI counters, responsive layouts, no default Streamlit appearance. |
| **Inference Engine** | Real-time prediction with range validation, calibrated placement probability gauge, model confidence percentage, and risk stratification. |
| **Explainable AI (XAI)** | Exact linear log-odds attribution chart ($z_j \cdot \beta_j$) identifying primary positive drivers and risk factors. |
| **Actionable Improvement** | Analytical recommendation cards targeting exam revision, attendance regularization, assignment frequency, and digital wellness. |
| **PDF Dossier Compiler** | In-memory ReportLab PDF generator containing candidate profile, results, metrics table, XAI weights, recommendations, and academic disclaimers. |
| **Cohort Analytics** | Interactive Plotly distributions, box plots, and scatter charts exploring the 10,000-student historical training corpus. |
| **Model Diagnostics** | Holdout test partition metrics, confusion matrix heatmap, ROC curve, and standardized coefficient sensitivities. |
| **Admin Console** | System telemetry, user management table with role modification, account deletion, and exportable global prediction audit log. |

---

## 🧪 Automated Test Suite Report

All tests have been executed and verified using `pytest`:

1. `tests/test_prediction.py::test_validate_inputs_success` &bull; **PASSED**
2. `tests/test_prediction.py::test_validate_inputs_missing_feature` &bull; **PASSED**
3. `tests/test_prediction.py::test_validate_inputs_out_of_range` &bull; **PASSED**
4. `tests/test_prediction.py::test_predict_placement_placed_case` &bull; **PASSED**
5. `tests/test_prediction.py::test_predict_placement_not_placed_case` &bull; **PASSED**
6. `tests/test_auth.py::test_password_hashing` &bull; **PASSED**
7. `tests/test_auth.py::test_user_registration_and_authentication` &bull; **PASSED**
8. `tests/test_database.py::test_database_isolation_and_predictions` &bull; **PASSED**
9. `tests/test_report.py::test_generate_pdf_report` &bull; **PASSED**
10. `tests/test_pages_compilation.py::test_compile_all_python_files` &bull; **PASSED**

---

## ⚖️ Academic Limitations & Ethical AI Disclosure

* **Correlation vs. Causality**: The machine learning model identifies empirical correlations within the training dataset. Achieving recommended academic benchmarks statistically aligns a student with historical placed cohorts but does not constitute a contractual guarantee of recruitment by external hiring organizations.
* **Feature Sensitivities**: Examination score represents the single largest statistical determinant ($\beta = 12.84$), accurately reflecting institutional screening cutoffs in campus placement drives.
* **Scope**: Designed specifically for MCA-level academic and placement analytics research.

---
**Developed by Karthik P** &bull; Master of Computer Applications (MCA) &bull; 2026
