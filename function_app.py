import azure.functions as func
import logging
from prediction import make_prediction

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    tenure = req.params.get("tenure")
    monthly = req.params.get("MonthlyCharges")
    techsupport = req.params.get("TechSupport_yes")
    phoneservice = req.params.get("PhoneService_yes")
    contract_one_year = req.params.get("Contract_one_year")
    contract_two_year = req.params.get("Contract_two_year")
    internet_fiber = req.params.get("InternetService_fiber_optic")
    internet_no = req.params.get("InternetService_no")

    if all([tenure, monthly, techsupport, phoneservice, contract_one_year, contract_two_year, internet_fiber, internet_no]):
        tenure = int(tenure)
        monthly = float(monthly)
        techsupport = int(techsupport)
        phoneservice = int(phoneservice)
        contract_one_year = int(contract_one_year)
        contract_two_year = int(contract_two_year)
        internet_fiber = int(internet_fiber)
        internet_no = int(internet_no)

        result = make_prediction(
            tenure=tenure,
            MonthlyCharges=monthly,
            TechSupport_yes=techsupport,
            PhoneService_yes=phoneservice,
            Contract_one_year=contract_one_year,
            Contract_two_year=contract_two_year,
            InternetService_fiber_optic=internet_fiber,
            InternetService_no=internet_no,
        )

        return func.HttpResponse(str(result), status_code=200)

    return func.HttpResponse(
        "Please provide: tenure, MonthlyCharges, TechSupport_yes, PhoneService_yes, Contract_one_year, Contract_two_year, InternetService_fiber_optic, InternetService_no",
        status_code=400,
    )
