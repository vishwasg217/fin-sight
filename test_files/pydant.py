def calculate_metrics(data):
    # Extracting values from the data
    grossProfit = float(data["grossProfit"])
    totalRevenue = float(data["totalRevenue"])
    operatingIncome = float(data["operatingIncome"])
    costOfRevenue = float(data["costOfRevenue"])
    costofGoodsAndServicesSold = float(data["costofGoodsAndServicesSold"])
    sellingGeneralAndAdministrative = float(data["sellingGeneralAndAdministrative"])
    ebit = float(data["ebit"])
    interestAndDebtExpense = float(data["interestAndDebtExpense"])

    # Calculating metrics
    gross_profit_margin = grossProfit / totalRevenue
    operating_profit_margin = operatingIncome / totalRevenue
    net_profit_margin = float(data["netIncome"]) / totalRevenue
    cost_efficiency = totalRevenue / (costOfRevenue + costofGoodsAndServicesSold)
    sg_and_a_efficiency = totalRevenue / sellingGeneralAndAdministrative
    interest_coverage_ratio = ebit / interestAndDebtExpense

    # Returning the results
    return {
        "gross_profit_margin": gross_profit_margin,
        "operating_profit_margin": operating_profit_margin,
        "net_profit_margin": net_profit_margin,
        "cost_efficiency": cost_efficiency,
        "sg_and_a_efficiency": sg_and_a_efficiency,
        "interest_coverage_ratio": interest_coverage_ratio
    }

# Example usage:
data = {
    "fiscalDateEnding": "2022-12-31",
    "reportedCurrency": "USD",
    "grossProfit": "32687000000",
    "totalRevenue": "60530000000",
    "costOfRevenue": "27842000000",
    "costofGoodsAndServicesSold": "385000000",
    "operatingIncome": "6408000000",
    "sellingGeneralAndAdministrative": "18609000000",
    "researchAndDevelopment": "6567000000",
    "operatingExpenses": "26279000000",
    "investmentIncomeNet": "None",
    "netInterestIncome": "-1216000000",
    "interestIncome": "162000000",
    "interestExpense": "1216000000",
    "nonInterestIncome": "365000000",
    "otherNonOperatingIncome": "443000000",
    "depreciation": "2407000000",
    "depreciationAndAmortization": "2395000000",
    "incomeBeforeTax": "1013000000",
    "incomeTaxExpense": "-626000000",
    "interestAndDebtExpense": "1216000000",
    "netIncomeFromContinuingOperations": "1783000000",
    "comprehensiveIncomeNetOfTax": "8134000000",
    "ebit": "2229000000",
    "ebitda": "4624000000",
    "netIncome": "1639000000"
}

print(calculate_metrics(data))
