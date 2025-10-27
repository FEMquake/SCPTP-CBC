#  CBC Prediction Platform

interactive platform for predicting the **Cyclic Backbone Curve (CBC)** of Self-Centering Precast Concrete (SCPC) bridge piers.

This app allows users to input design parameters and configuration types and visualize the resulting backbone response curve.  

## Author
**S. Mohammad Hosseini V.**  
Shahid Beheshti University  
Civil, Water, and Environmental Engineering Faculty 
Email: s_hosseinii@.sbu.ac.ir


## Features

- Adjustable design parameters:
- Concrete strength, pier dimensions, aspect ratio, etc.
- Configurable system setup:
- Internal/External ED bars, Monolithic/Segmental, Toe type, Cross-section
- Auto-generated schematic of configuration
- Predicted cyclic backbone curve (Base Shear vs Drift)
- Downloadable results in CSV and PDF formats
- Fully self-contained Streamlit app

##  Installation & Run Locally

1. Clone the repository:

```bash
# 1️⃣ Clone this repo
git clone https://github.com/FEMquake/SCPTP-CBC
cd SCPTP-CBC
```
# 2️⃣ Install dependencies
pip install -r requirements.txt

# 3️⃣ Run the app
streamlit run app.py
```
2. Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

📘 Usage

Adjust the input parameters on the left tab (“Platform tuning”).

Click Run Prediction.

View and download the results in the Results tab.

## Dependencies

- streamlit
- pandas
- numpy
- matplotlib

