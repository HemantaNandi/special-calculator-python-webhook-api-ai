#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    if req.get("result").get("action") == "bank.rates":
        res = makeWebhookResult(req) 
    elif req.get("result").get("action") == "loan.emi":
        #res = loanEmi(req)
        res = calculateFSF(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def loanEmi(req):
    result = req.get("result")
    parameters = result.get("parameters")
    Loan_amount = int(parameters.get("number"))
    Interest_rate = parameters.get("percentage")
    Interest_rate = float(Interest_rate.strip('%'))
    Payment = parameters.get("duration")
    if str(Payment["unit"]) == "mo":
        Payment_period = int(Payment["amount"])
    elif str(Payment["unit"]) == "yr":
        Payment_period = int(Payment["amount"]) * 12
    Interest_rate = float((Interest_rate/100))
    Month_Payment = int((Loan_amount*pow((Interest_rate/12)+1,
                                 (Payment_period))*Interest_rate/12)/(pow(Interest_rate/12+1,
                                 (Payment_period)) - 1))
    speech = "EMI :" + str(Month_Payment)
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "special-calculator-python-webhook-api-ai"
    }
def compoundInterest(req):
    result = req.get("result")
    parameters = result.get("parameters")
    x = int(parameters.get("number"))
    interest = parameters.get("percentage")
    y = float(interest.strip('%'))
    Payment = parameters.get("duration")
    if str(Payment["unit"]) == "mo":
        z = int(Payment["amount"]) / 12
    elif str(Payment["unit"]) == "yr":
        z = int(Payment["amount"])
    #interest = float((interest/100))

    #totalann = int((x*(pow(1 + ((y*.01)/1),z)))-x)
    totalsemi = int((x*(pow(1 + ((y*.01)/2),(z*2))))-x)
    #totalqtr = int((x*(pow(1 + ((y*.01)/4),(z*4))))-x)
    #totalmth = int((x*(pow(1 + ((y*.01)/12),(z*12))))-x)

    #yieldann = float((((x*(pow(1 + ((y*.01)/1),1)))-x)/x)*100)
    yieldsemi = float((((x*(pow(1 + ((y*.01)/2),(2))))-x)/x)*100)
    #yieldqtr = float((((x*(pow(1 + ((y*.01)/4),(4))))-x)/x)*100)
    #yieldmth = float((((x*(pow(1 + ((y*.01)/12),(12))))-x)/x)*100)

    #totalannMaturity = int(x/1+totalann/1)
    totalsemiMaturity = int(x/1+totalsemi/1)
    #totalqtrMaturity = int(x/1+totalqtr/1)
    #totalmthMaturity = int(x/1+totalmth/1)
    speech = "Total Interest :" + str(totalsemi)+"\nYield :"+str(yieldsemi)+"\nMaturity :"+str(totalsemiMaturity)
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "special-calculator-python-webhook-api-ai"
    }
def compoundInterestReverse(req):
	result = req.get("result")
	parameters = result.get("parameters")
	m = int(parameters.get("number"))
	x = 1
	interest = parameters.get("percentage")
	y = float(interest.strip('%'))
	Payment = parameters.get("duration")
	if str(Payment["unit"]) == "mo":
		z = int(Payment["amount"]) / 12
	elif str(Payment["unit"]) == "yr":
		z = int(Payment["amount"])
	totalSemi = float((x*(pow(1 + ((y*.01)/2),(z*2))))-x)
	yieldSemi = float((((x*(pow(1 + ((y*.01)/2),(2))))-x)/x)*100)
	
	totalSemiMaturity = int(m/(x/1+totalSemi/1))
	totalSemi = int(m - totalSemiMaturity)
	speech = "Amount :"+ str(totalSemiMaturity)+"\nYield :"+str(yieldSemi)
	print("Response:")
	print(speech)
	return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "special-calculator-python-webhook-api-ai"
        }
def calculateFSF(req) :
	result = req.get("result")
	parameters = result.get("parameters")
	a = int(parameters.get("number"))
	Interest_rate = parameters.get("percentage")
	b = float(Interest_rate.strip('%'))
	Payment = parameters.get("duration")
	if str(Payment["unit"]) == "mo":
		c = int(Payment["amount"])
	elif str(Payment["unit"]) == "yr":
		c = int(Payment["amount"]) * 12
	i = float((b/100)/12)
	n = int(c*12)
	v = int(1/(1+i))
	z = pow((1+i),n)
	w = pow(v,n)
	
	totala = int((a*((1-w)/i)*(1+i))*z)
	totalamt = int(a*n)
	totalint = int(totala - totalamt)
        speech = "Amount :"+ str(totala)+"\nYield :"+str(totalamt)
	print("Response:")
	print(speech)
	return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "special-calculator-python-webhook-api-ai"
        }

def makeWebhookResult(req):
    #if req.get("result").get("action") != "shipping.cost":
        #return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("bank-name")

    cost = {'Andhra Bank':'6.85%', 'Allahabad Bank':'6.75%', 'Axis Bank':'6.5%', 'Bandhan bank':'7.15%', 'Bank of Maharashtra':'6.50%', 'Bank of Baroda':'6.90%', 'Bank of India':'6.60%', 'Bharatiya Mahila Bank':'7.00%', 'Canara Bank':'6.50%', 'Central Bank of India':'6.60%', 'City Union Bank':'7.10%', 'Corporation Bank':'6.75%', 'Citi Bank':'5.25%', 'DBS Bank':'6.30%', 'Dena Bank':'6.80%', 'Deutsche Bank':'6.00%', 'Dhanalakshmi Bank':'6.60%', 'DHFL Bank':'7.75%', 'Federal Bank':'6.70%', 'HDFC Bank':'5.75% to 6.75%', 'Post Office':'7.10%', 'Indian Overseas Bank':'6.75%', 'ICICI Bank':'6.25% to 6.9%', 'IDBI Bank':'6.65%', 'Indian Bank':'4.75%', 'Indusind Bank':'6.85%', 'J&K Bank':'6.75%', 'Karnataka Bank':'6.50 to 6.90%', 'Karur Vysya Bank':'6.75%', 'Kotak Mahindra Bank':'6.6%', 'Lakshmi Vilas Bank':'7.00%', 'Nainital Bank':'7.90%', 'Oriental Bank of Commerce':'6.85%', 'Punjab National Bank':'6.75%', 'Punjab and Sind Bank':'6.4% to 6.80%', 'Saraswat bank':'6.8%', 'South Indian Bank':'6% to 6.75%', 'State Bank of India':'6.75%', 'Syndicate Bank':'6.50%', 'Tamilnad Mercantile Bank Ltd':'6.90%', 'UCO bank':'6.75%', 'United Bank Of India':'6%', 'Vijaya Bank':'6.50%', 'Yes Bank':'7.10%'}

    speech = "The interest rate of " + zone + " is " + str(cost[zone])
    print("Response:")
    print(speech)
    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        #"contextOut": [],
        "source": "BankRates"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))

    print ("Starting app on port %d" %(port))

    app.run(debug=True, port=port, host='0.0.0.0')
