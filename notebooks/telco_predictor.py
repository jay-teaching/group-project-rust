import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    mo.md("""
    # Telco Customer Churn Predictor

    This notebook loads the trained logistic regression model and allows you to make predictions on new customer data.
    """)
    return (mo,)


@app.cell
def _():
    from pathlib import Path
    import joblib
    import pandas as pd
    return Path, joblib, pd


@app.cell
def _(Path):
    MODEL_PATH = Path("models/telco_logistic_regression.joblib")
    return (MODEL_PATH,)


@app.cell
def _(MODEL_PATH, joblib, mo):
    # Load the trained model and scaler
    try:
        model_data = joblib.load(MODEL_PATH)
        model = model_data["model"]
        scaler = model_data["scaler"]
        mo.md(f"✅ Model loaded successfully from `{MODEL_PATH}`")
    except FileNotFoundError:
        mo.md(f"❌ Model not found at `{MODEL_PATH}`. Please train the model first using telco_marimo.py")
    return model, scaler


@app.cell
def _(mo):
    mo.md("""
    ## Enter Customer Information

    Provide the customer details below to predict churn probability.
    """)
    return


@app.cell
def _(mo):
    # Input fields for customer data
    tenure = mo.ui.slider(start=0, stop=72, value=12, label="Tenure (months)")
    monthly_charges = mo.ui.slider(start=18.0, stop=120.0, value=70.0, step=0.5, label="Monthly Charges ($)")

    tech_support = mo.ui.dropdown(
        options={"No": 0, "Yes": 1},
        value="No",
        label="Tech Support"
    )

    phone_service = mo.ui.dropdown(
        options={"No": 0, "Yes": 1},
        value="Yes",
        label="Phone Service"
    )

    contract_type = mo.ui.dropdown(
        options={"Month-to-month": "month", "One year": "one", "Two year": "two"},
        value="Month-to-month",
        label="Contract Type"
    )

    internet_service = mo.ui.dropdown(
        options={"DSL": "dsl", "Fiber optic": "fiber", "No": "no"},
        value="Fiber optic",
        label="Internet Service"
    )

    return (
        contract_type,
        internet_service,
        monthly_charges,
        phone_service,
        tech_support,
        tenure,
    )


@app.cell
def _(
    contract_type,
    internet_service,
    mo,
    monthly_charges,
    phone_service,
    tech_support,
    tenure,
):
    mo.vstack([
        tenure,
        monthly_charges,
        tech_support,
        phone_service,
        contract_type,
        internet_service
    ])
    return


@app.cell
def _(
    contract_type,
    internet_service,
    monthly_charges,
    pd,
    phone_service,
    tech_support,
    tenure,
):
    # Prepare input data for prediction
    customer_data = {
        "tenure": tenure.value,
        "MonthlyCharges": monthly_charges.value,
        "TechSupport_yes": tech_support.value,
        "PhoneService_yes": phone_service.value,
        "Contract_one_year": 1 if contract_type.value == "one" else 0,
        "Contract_two_year": 1 if contract_type.value == "two" else 0,
        "InternetService_fiber_optic": 1 if internet_service.value == "fiber" else 0,
        "InternetService_no": 1 if internet_service.value == "no" else 0,
    }

    input_df = pd.DataFrame([customer_data])
    return (input_df,)


@app.cell
def _(input_df, mo, model, scaler):
    # Make prediction
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)[0, 1]

    churn_status = "WILL CHURN" if prediction == 1 else "WILL NOT CHURN"
    risk_level = "High" if probability > 0.7 else "Medium" if probability > 0.4 else "Low"

    mo.md(f"""
    ## Prediction Results

    - **Prediction**: {churn_status}
    - **Churn Probability**: {probability:.2%}
    - **Risk Level**: {risk_level}
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ### Customer Feature Values
    """)
    return


@app.cell
def _(input_df):
    input_df
    return


if __name__ == "__main__":
    app.run()
