import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io


def predict_backbone(inputs, config):
    """
    Demo-the Ml model Not implemented yet
    Args:
        inputs (dict): A dictionary of the numerical input parameters.
        config (dict): A dictionary of the categorical configuration choices.

    Returns:
        pd.DataFrame: A DataFrame with 'Drift' and 'BaseShear' columns.
    """
    st.info("Using placeholder model (based on Fig. 12a from the paper).")

    # TODO: Replace this with the actual model.predict() call.
    data = {
        'Drift': [0.00, 0.2, 0.5, 0.8, 1, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0],
        'BaseShear': [0, 200, 450, 520, 550, 580, 600, 650, 640, 630, 620]
    }
    
    if config['ed_type'] == 'Internal' and inputs['rho_b'] == 0:
        # This logic is just for show.
        pass
        
    return pd.DataFrame(data)

# --- Helper Functions for Plotting ---

def plot_configuration(ed_type, segmentation, toe, section):
    """
    Draws a simple schematic based on user's configuration choices.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    # Base
    ax.add_patch(plt.Rectangle((0, 0), 2, 0.5, color='#aaa'))
    
    # Cross-Section
    if section == 'Circular':
        center_x, width = 1, 1.2
        pier = plt.Rectangle((center_x - width/2, 0.5), width, 3, color='#ddd')
    else: # Quadrilateral
        center_x, width = 1, 1.0
        pier = plt.Rectangle((center_x - width/2, 0.5), width, 3, color='#ddd')
    ax.add_patch(pier)

    # Segmentation
    if segmentation == 'Segmental':
        # FIX: y-data must have the same dimension as x-data (2 points)
        ax.plot([center_x - width/2, center_x + width/2], [1.5, 1.5], 'k-')
        ax.plot([center_x - width/2, center_x + width/2], [2.5, 2.5], 'k-')
        ax.set_title("Segmental Pier", fontsize=10)
    else:
        ax.set_title("Monolithic Pier", fontsize=10)

    # Rocking Toe
    if toe == 'Strengthened (Rigid)':
        ax.add_patch(plt.Rectangle((center_x - width/2 - 0.1, 0.5), width + 0.2, 0.75, color='#888', fill=False, hatch='//'))
        ax.text(center_x, -0.2, "Strengthened Toe", ha='center', fontsize=9)
    else:
        ax.text(center_x, -0.2, "Ductile Toe", ha='center', fontsize=9)

    # ED Bars
    if ed_type == 'Internal':
        ax.plot([center_x - 0.2, center_x - 0.2], [0, 1.0], 'r-', lw=2)
        ax.plot([center_x + 0.2, center_x + 0.2], [0, 1.0], 'r-', lw=2)
        ax.text(center_x - 0.2, 1.1, "Internal ED", ha='center', fontsize=9, color='r')
    else: # External
        ax.add_patch(plt.Rectangle((center_x - width/2 - 0.4, 1.0), 0.4, 0.2, color='#bbb'))
        ax.add_patch(plt.Rectangle((center_x + width/2, 1.0), 0.4, 0.2, color='#bbb'))
        ax.plot([center_x - width/2 - 0.2, center_x - width/2 - 0.2], [0, 1.1], 'r-', lw=2)
        ax.plot([center_x + width/2 + 0.2, center_x + width/2 + 0.2], [0, 1.1], 'r-', lw=2)
        ax.text(center_x - width/2 - 0.2, 1.3, "External ED", ha='center', fontsize=9, color='r')
    
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 4)
    return fig

def plot_backbone_curve(df):
    """
    Plots the predicted backbone curve.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(df['Drift'], df['BaseShear'], 'b-', marker='o', label='Predicted Backbone')
    
    ax.set_title('Predicted Cyclic Backbone Curve', fontsize=16)
    ax.set_xlabel('Drift (%)', fontsize=12)
    ax.set_ylabel('Base Shear (kN)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    
    return fig

def create_summary_html(inputs, config, df):
    
    style = """
    <style>
        .summary-table {
            width: 100%;
            border-collapse: collapse;
            font-family: 'sans serif';
        }
        .summary-table th, .summary-table td {
            text-align: left;
            padding: 6px;
            border-bottom: 1px solid #ddd;
        }
        .summary-table th {
            background-color: #f4f4f4;
            font-weight: 600;
        }
        .summary-table .label {
            font-weight: 500;
            color: #333;
        }
        .summary-table .value {
            font-weight: 400;
            color: #111;
        }
        .summary-table .header {
            font-size: 1.1em;
            font-weight: 700;
            color: #000;
            background-color: #eee;
        }
    </style>
    """

    table_html = f"""
    <table class="summary-table">
        <tr><td colspan="2" class="header">Input Parameters</td></tr>
        <tr><td class="label"><i>f<sub>c</sub></i> (Concrete Strength)</td><td class="value">{inputs['fc']:.2f} MPa</td></tr>
        <tr><td class="label"><i>B</i> (Pier Dimension)</td><td class="value">{inputs['B']:.2f} m</td></tr>
        <tr><td class="label"><i>&eta;</i> (Aspect Ratio)</td><td class="value">{inputs['eta']:.2f}</td></tr>
        <tr><td class="label"><i>A<sub>t</sub></i> (Tendon Area)</td><td class="value">{inputs['At']:.2f} cm²</td></tr>
        <tr><td class="label"><i>&rho;<sub>b</sub></i> (ED Bar Ratio)</td><td class="value">{inputs['rho_b']:.2f} %</td></tr>
        <tr><td class="label"><i>H<sub>b</sub></i> (ED Bar Height)</td><td class="value">{inputs['Hb']:.2f} m</td></tr>
        <tr><td class="label"><i>f<sub>yb</sub></i> (ED Yield Strength)</td><td class="value">{inputs['fyb']:.2f} MPa</td></tr>
        <tr><td class="label"><i>&rho;<sub>w</sub></i> (Axial Load Ratio)</td><td class="value">{inputs['rho_w']:.3f}</td></tr>
        <tr><td class="label"><i>&rho;<sub>t</sub></i> (Post-tension Ratio)</td><td class="value">{inputs['rho_t']:.2f}</td></tr>
    </table>
    """

    return style, table_html

st.set_page_config(page_title="CBC Prediction Platform", layout="wide")

st.title("Automated Platform for CBC Prediction of SCPT Piers")

tab_tune, tab_results = st.tabs(["Platform tuning", "Results"])

# --- Tab 1: Platform tuning ---
with tab_tune:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Key Design Parameters")
        
        inputs = {
            'fc': st.number_input(label="Concrete Compressive Strength, $f_c$ (MPa)", value=49.0, min_value=20.0, max_value=100.0, step=1.0),
            'B': st.number_input(label="Pier Dimension, $B$ (m)", value=0.50, min_value=0.1, max_value=5.0, step=0.05),
            'eta': st.number_input(label="Aspect Ratio, $\eta$", value=3.4, min_value=2.0, max_value=10.0, step=0.1),
            'At': st.number_input(label="PT Tendon Area, $A_t$ (cm²)", value=10.7, min_value=1.0, max_value=50.0, step=0.1),
            'rho_b': st.number_input(label="ED Bar Ratio, $\rho_b$ (%)", value=5.3, min_value=0.0, max_value=10.0, step=0.1),
            'Hb': st.number_input(label="ED Bar Height, $H_b$ (m)", value=0.17, min_value=0.0, max_value=1.0, step=0.01),
            'fyb': st.number_input(label="ED Yield Strength, $f_{yb}$ (MPa)", value=420.0, min_value=200.0, max_value=600.0, step=10.0),
            'rho_w': st.number_input(label="Axial Load Ratio, $\rho_w$", value=0.045, min_value=0.0, max_value=0.5, step=0.005, format="%.3f"),
            'rho_t': st.number_input(label="Post-tensioning Ratio, $\rho_t$", value=0.32, min_value=0.0, max_value=1.0, step=0.01)
        }

    with col2:
        st.subheader("Configuration")
        
        config = {
            'ed_type': st.selectbox("ED Bar Type (Fig. 3b)", ["Internal", "External"]),
            'segmentation': st.selectbox("Segmentation (Fig. 3c)", ["Monolithic", "Segmental"]),
            'toe': st.selectbox("Rocking Toe (Fig. 3d)", ["Ductile (Plain)", "Strengthened (Rigid)"]),
            'section': st.selectbox("Cross-Section (Fig. 3e)", ["Circular", "Quadrilateral"])
        }
        
        st.subheader("Selected Configuration Schematic")
        fig_config = plot_configuration(config['ed_type'], config['segmentation'], config['toe'], config['section'])
        st.pyplot(fig_config)

        run_button = st.button("Run Prediction", type="primary", use_container_width=True)

if run_button:
    st.session_state.inputs = inputs
    st.session_state.config = config
    st.session_state.prediction_run = True

with tab_results:
    if not st.session_state.get('prediction_run', False):
        st.info("Click 'Run Prediction' on the 'Platform tuning' tab to see results.")
    else:
        st.subheader("Prediction Results")
        
        inputs = st.session_state.inputs
        config = st.session_state.config
        
        with st.spinner("Running prediction..."):
            results_df = predict_backbone(inputs, config)
            st.session_state.results_df = results_df 
        
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Summary of Inputs & Outputs")
            
            style, table_html = create_summary_html(inputs, config, results_df)
            st.markdown(style, unsafe_allow_html=True)
            st.markdown(table_html, unsafe_allow_html=True)
            
        with col2:
            st.subheader("Predicted Cyclic Backbone Curve")
            fig_curve = plot_backbone_curve(results_df)
            st.pyplot(fig_curve)
            
            st.subheader("Download Results")
            
            csv_data = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Data (CSV)",
                data=csv_data,
                file_name="predicted_backbone_data.csv",
                mime="text/csv",
                use_container_width=True
            )

            pdf_buffer = io.BytesIO()
            fig_curve.savefig(pdf_buffer, format="pdf", bbox_inches='tight')
            pdf_data = pdf_buffer.getvalue()
            
            st.download_button(
                label="Download Plot (PDF)",
                data=pdf_data,
                file_name="predicted_backbone_plot.pdf",
                mime="application/pdf",
                use_container_width=True
            )







