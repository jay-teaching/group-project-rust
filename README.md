# Telco Churn Predictions (Group Rust)

## Authors
- Alessandra Marchetti
- Annamária-Réka Vass
- Tsung-Han Tsai
- Antonios Skoufis

## Project Summary

This project aims to build, evaluate and deploy a machine learning based churn-prediction model to help the company predict the customer churn and take measures in retaining the clients.

## The System Architecture

- **Machine Learning Model**

    - A **simple logistics regression model** trained on historical customer data.
    - Taking **6 parameters** inputs to perform churn probability calculation.

- **Frontend (User Interface)**:

    - Using **Marimo Notebook** to build a reactive, interactive UI 
    - Providing a user-friendly dashboard for stakeholders to input customer features.
    - Deployed in 2 approaches (**Azure Container Apps** and **Azure Virtual Machine**)

- **Backend API**

    - Built by **Azure Functions** to act as the bridge between the UI and the ML model. 
    - Handling HTTP requests, performs input validation, and triggers the ML model.



## Machine Learning Model

The model utilized `scikit-learn` to build a simple logistic regression model.

The model uses the following features:
- `tenure`: Number of months the customer has stayed with the company.
- `MonthlyCharges`: The amount charged to the customer monthly.
- `TechSupport_yes`: Binary indicator of whether the customer has tech support.
- `PhoneService_yes`: Binary indicator of whether the customer has subscribed to the Phone Service.
- `Contract_one year`: Indicator of whether the customer signed a one year contract.
- `Contract_two year`: Indicator of whether the customer signed a two year contract.
- `InternetService_fiber optic`: Binary indicator of whether the customer uses fiber optic internet service.
- `InternetService_no`: Binary indicator of whether the customer uses any internet service at all.

## The Frontend - Marimo Notebook

We used **Marimo Notebook** to allow users interacting with the model predictions by changing the parameters' input. 

User will be able to interaction with the parameters via:

- **Sliders**: `Tenure (months)` and `Monthly Charges ($)` 

- **Dropdown Lists**: Binary and categorical input such as `Tech Support`, `Phone Service`, `Contract Type` and `Internet Service`

Upon changing the input, the user will be able to see the changes in:

- **Prediction Result**
- **Churn Probability**
- **Risk Level**. 

In addition, the parameter input table will also be visible.

## The Frontend - Deployment

The frontend is deployed in 2 separate approaches, **Azure Container Apps** and **Azure Virtual Machine**.

1. **Azure Container Apps (container-based deployment)**

    The primary frontend deployment, which runs a Docker image, built and published through **GitHub Actions**.

    - **Container Image**: The frontend is packaged as a Docker image and published to **GitHub Container Registry (GHCR)**.

    - **Image Repository**: ghcr.io/jay-teaching/group-project-rust/frontend

    - **Tag used**: main

    - **Azure Container App Detail**:

        - **Container App name**: rustpredict-frontend
        - **Resource group**: DSMT
        - **Region**: Switzerland North
        - **Workload profile**: Consumption

    - **Public URL (Container App)**: 

        https://rustpredict-frontend.whitepebble-83aa8a23.switzerlandnorth.azurecontainerapps.io

2. **Azure Virtual Machine**

    In addition to the container-based deployment, the frontend was also deployed on a **Linux Virtual Machine** to demonstrate a traditional infrastructure-based setup.
    
    It uses Docker in detached mode with a restart policy (unless-stopped), ensuring it remains available independently of user sessions and automatically restarts after reboots.

    - **Virtual Machine Details**:

        - **VM name**: rustpredict-vm
        - **Operating system**: Ubuntu 24.04 LTS
        - **VM size**: Standard B2ats v2 (2 vCPUs, 1 GiB RAM)
        - **Resource group**: DSMT
        - **Region**: Switzerland North

    - **Public IP address / URL**: 
    
        http://51.107.3.230/

## Backend API

The machine learning prediction API was deployed using **Azure Functions** with a **Flex Consumption** plan to ensure scalability and cost efficiency.

- Service Details

    This setup allows the API to automatically scale based on demand while incurring minimal cost when idle.

	- **Service type**: Azure Functions (HTTP-triggered)
	- **Function App name**: rustpredict
	- **Region**: Switzerland North
	- **Operating system**: Linux
	- **Plan type**: Flex Consumption (serverless, scale-to-zero)

- API Endpoint

    The prediction API is exposed via an HTTP endpoint

    The function uses **function-level authentication (AuthLevel.FUNCTION)**.

    A function key is required to access the endpoint and is not included in this repository for security reasons.

- Example Request

    GET /api/http_trigger?tenure=12&MonthlyCharges=70

    &TechSupport_yes=1&PhoneService_yes=1

    &Contract_one_year=0&Contract_two_year=1

    &InternetService_fiber_optic=0&InternetService_no=0


- Input Parameters

    The API expects the full feature set used by the trained logistic regression model. All parameters are passed as query parameters.

    | Parameter Name | Type | Description |
    | :--- | :--- | :--- |
    | **tenure** | `int` | Customer tenure (months) |
    | **MonthlyCharges** | `float` | Monthly charges amount |
    | **TechSupport_yes** | `int (0/1)` | Indicator: Whether the customer has technical support |
    | **PhoneService_yes** | `int (0/1)` | Indicator: Whether the customer has phone service |
    | **Contract_one_year** | `int (0/1)` | Indicator: One-year contract |
    | **Contract_two_year** | `int (0/1)` | Indicator: Two-year contract |
    | **InternetService_fiber_optic** | `int (0/1)` | Indicator: Fiber optic internet service |
    | **InternetService_no** | `int (0/1)` | Indicator: No internet service |

- Response

    The API returns a single numeric value representing the predicted probability of customer churn.

    - **Response type**: text/plain
    - **Status code**: 200 OK (successful prediction)

## CI/CD Pipeline

- Setting up Automated checks while building the Docker Container.

- Creating the docker image and integrating the frontend

## Technology

- Cloud Platform: **Microsoft Azure**


## Previous Instructions

### The model
We recommend looking into additional features and engineering new ones to
improve model performance. There are other possible issues to explore, including
model choice, leakage, and others.

The model is built and trained using `notebooks/telco_marimo.py`. The model is
saved in the `models/` directory, with the scaler and model bundled together
using `joblib`.

An example prediction can be found in `prediction.py`.

### CI Pipeline
There is a CI pipeline set up using GitHub Actions that runs tests
on every push and pull request. The tests are located in the `tests/`
directory and can be run locally using `pytest`.

### Deploying to Serverless
The saved model can deployment to an Azure Function with the following
steps:


1. **In your Codespace**, install the Azure Function extension:
    - Open the Extensions view in the left sidebar.
    - Search for "Azure Functions" and install the extension by Microsoft.

2. **In your Codespace**, create the function:
    - Open the Command Palette (`Ctrl+Shift+P`).
    - Type and select *Azure Functions: Create Function*
         - Do not select the "...in Azure..." command
    - Select the root folder of the project (should be the default).
    - Select *Python* as the language.
    - Select *HTTP trigger* as the template.
    - Provide a name (without spaces or special characters) e.g. predict.
    - Select *FUNCTION* as the authorization level.
    - **Do not** *overwrite* the `.gitignore` file.

3. **In your Codespace**, wait some time for the function to be created. Then:
    - Add azure.functions to your env with `uv add azure-functions`
    - Update the `requirements.txt` file for Azure `uv pip freeze > requirements.txt`
    - Edit the `function_app.py` file
        - Add an import: `from prediction import make_prediction`
        - Replace the line `name = req.params.get('name')`,
        using the same approach to get input data for prediction.
            - You'll need tenure, monthly bill and tech support status.
            - It is up to you how you name these but simple names are best.
            - The variable name (on the left) is internal to the function,
            while the string name (on the right) is what the user will need to provide.
                ```python
                tenure = req.params.get('tenure')
                monthly = req.params.get('monthly')
                techsupport = req.params.get('techsupport')
                ```
        - Remove the entire `if not name:` block. We aren't supporting JSON input here.
        - Call the `make_prediction` function, passing tenure, monthly and techsupport
        as keyword arguments following the column names used by the model:
            ```python
            prediction = make_prediction(
                tenure=tenure,
                MonthlyCharges=monthly,
                TechSupport_yes=techsupport
            )
            ```
        - Change `if name:` to `if tenure and monthly and techsupport:`
        - Change the `f""` response to return the prediction result instead of a name.
    - **Commit and Sync** all your changes!

4. **In the Azure Portal**, create a Azure Function App.
    - Choose *Flex Consumption*.
    - Select your existing **Resource Group**.
    - Choose a unique **name** for your Function App.
    - Set the **Region** to a supported student region (e.g. *Switzerland North*).
    - Choose *Python* *3.12* / *3.13* as the **runtime** stack and **version**.
    - Choose the smallest **instance size** (e.g. *512MB*).
    - If given the option, *disable* **Zone Redundancy**.
    - Use an existing **Storage Account** or create a new one.
    - *Configure* **diagnostic settings** *now*, leaving the default.
    - Leave the *defaults* for OpenAI (disable)
    - Leave the *defaults* for Networking (public enabled, virtual disabled).
    - Leave the *defaults* for Monitoring (enable in a supported region).
    - Enable **Continuous Deployment** and point to your repo, signing in to GitHub.
    - Enable **Basic Authentication**.
    - Leave the *defaults* for Authentication (secrets) and tags (none).
    - Wait until the deployment completes.

5. **In the Codespace**, in **Source Control**, click on the *Pull* icon,
or chose it through the `...` menu.
    - Ensure you have the latest changes from GitHub (a new workflow file)
        - If not, click *Pull* again until you do.
    - Edit the **newly** created workflow file in `.github/workflows/`
    i.e. not the existing `quality.yaml`
        - Find the `Install dependencies` step and add `-t .` to the commmand:
        
            ```yaml
            run: pip install -r requirements.txt -t .
            ```
        - Find the `Deploy to Azure Functions` and add `sku: 'flexconsumption' to the with block:
        
            ```yaml
            ...
            with:
              sku: 'flexconsumption'
              app-name: ...
            ```
    - **Commit and Sync** all your changes!

6. **On your repository on GitHub**, go to the *Actions* tab.
    - Wait for the workflow to complete successfully.

7. **In the Azure Portal**, navigate to your Function App.
    - Select your function from the list.
    - Test the function using the *Test/Run* option in the Function
        - Provide the required parameters (tenure, monthly, techsupport)
        - Run the test and check the output for the prediction result.