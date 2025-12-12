import azure.functions as func
import logging
from prediction import make_prediction

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    tenure = req.params.get('tenure')
    monthly = req.params.get('monthly')
    techsupport = req.params.get('techsupport')

    if tenure and monthly and techsupport:
        tenure = int(tenure)
        monthly = float(monthly)
        techsupport = int(techsupport)

        result = make_prediction(
            tenure=tenure,
            MonthlyCharges=monthly,
            TechSupport_yes=techsupport
        )

        return func.HttpResponse(str(result))

    return func.HttpResponse(
        "Please provide tenure, monthly, and techsupport parameters.",
        status_code=400
    )
