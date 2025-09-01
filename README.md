# Risk Analyst I - Case
This repository was created as a requirement for a data analyst position. The `readme.md` file contains all the theoretical aspects requested in the test, as well as important information about the API and its results. The repository files contain the structured notebook for machine learning training and the API files.
The established anti-fraud training rules are based on a combination of factors such as purchase time, purchase repetition, presence of device ID, purchase amount and others. All of this assigns a score where 1 indicates fraud and 0 indicates non-fraud.
## Summary

- [1. Tasks](#1-tasks)
  - [1.1 - Understand the Industry](#11---understand-the-industry)
  - [1.2 - Solve the problem](#12---solve-the-problem)
- [2. Get your hands dirty](#2-get-your-hands-dirty)
- [3. Create an anti-fraud solution](#3-create-an-anti-fraud-solution)
  - [Testing the API](#testing-the-api)
  
## 1. Tasks

### 1.1 - Understand the Industry
1. In the payment industry, the money flow starts when a customer initiates a purchase, with funds moving from the issuing bank through the payment network to the acquiring bank and finally to the merchant’s account after settlement. 
The information flow runs in parallel, transmitting transaction details from the merchant to the acquirer, then through the payment network to the issuer for authorization and back with approval or decline. 
The main players are the customer, the merchant, the acquiring bank, the issuing bank, the payment processor, and the payment network.


2. An acquirer is the financial institution that holds the merchant’s account, assumes the financial risk of processing card transactions, and settles the funds after approval. 
A sub-acquirer operates under the umbrella of an acquirer, aggregating multiple merchants without each needing a direct contract with the bank, simplifying onboarding but relying on the acquirer for settlement. 
A payment gateway is a technology layer that securely transmits transaction data between the merchant, the acquirer or sub-acquirer, and the card networks. 
When a sub-acquirer is involved, the merchant’s relationship is with the sub-acquirer, who passes both the transaction information and the settlement through the acquirer. With a gateway, the information flow is routed through the gateway’s secure infrastructure before reaching the acquirer for authorization.

3. A chargeback is a reversal of a card transaction initiated by the cardholder through their issuing bank. Unlike a cancellation, which is agreed upon directly between merchant and customer before settlement, a chargeback happens after the payment has been processed, pulling funds back from the merchant’s account and often adding fees. 
In the acquiring, chargebacks are tied to fraud: true fraud occurs when stolen card data is used, while “friendly fraud” happens when a legitimate buyer later disputes the charge. High chargeback ratios can damage a merchant’s reputation with acquirers, trigger higher fees, or even lead to account termination

4. An anti-fraud is a set of processes designed to detect, prevent, and respond to fraudulent transactions in real time. For an acquirer, it works as both a shield and a filter, it monitors merchant activity, scores transactions using AI and machine learning, flags suspicious patterns, and blocks high-risk operations before they settle. It also supports compliance by tracking chargeback ratios, verifying merchant legitimacy during onboarding, and continuously analyzing portfolio behavior to spot anomalies.

### 1.2 - Solve the problem
First, I would explain that the issuer’s decision is based on the evidence and that, for the reason “Product/Service not provided,” the most decisive proof is delivery confirmation that  links the product to the cardholder, like a signature or photo at the delivery address. 
I would review the proof to identify any gaps and check if the client can provide stronger evidence, such as signed delivery receipts, courier tracking logs, or proof of customer acknowledgment. If new evidence exists, I would evaluate the possibility of filing an second argumentation according to the card network’s rules. If no further action is possible, I would explain the limitations of the dispute process, advise on preventive measures for future transactions, and offer guidance on strengthening delivery confirmation to reduce the risk of similar chargebacks.

## 2. Get your hands dirty
1. Based on the data, I identified chargeback activity tied to specific merchant, user, device combinations, repeated high value transactions within short times, and multiple uses of the same device with different cards. These patterns suggest coordinated fraud or card testing, as they show repeated actions and alternating successful and disputed transactions. The none of device ids in  chargeback cases also points to possible deliberate masking. 
My recommended actions would include flagging these accounts for manual review, temporarily suspending the involved cards pending investigation, implementing velocity controls for users with multiple card usage patterns, conducting merchant risk assessments for those with high chargeback rates, and enhancing real-time monitoring for same-device different-card scenarios.

2. To enhance fraud detection capabilities beyond the current transaction data, I'd analyze historical user behavior patterns including typical spending amounts, frequency, merchant categories, and geographical locations to establish baseline profiles. Device fingerprinting data such as IP addresses, geolocation, and network information would help identify account takeover attempts. Real-time velocity controls tracking transaction frequency per user, card, and merchant within specific time windows would perfect.

3. I would implement a multi-layered fraud prevention strategy combining real-time monitoring. I'd establish dynamic velocity limits that adapt based on user behavior patterns, automatically declining transactions when users exceed their historical spending. I'd also implement merchant-specific risk scoring that increases for merchants with high chargeback ratios and applies additional verification steps for high risk transactions.
For chargeback prevention, I'd introduce mandatory step-up authentication for transactions above user-specific thresholds, create automated alerts for customer service teams when suspicious patterns emerge. Machine learning models would continuously learn from chargeback outcomes to refine risk scoring algorithms. 

## 3. Create an anti-fraud solution.
- **Machine learning model training:** uses the dataset `transaction-sample.csv` with fake transactions to train a logistic regression model that detects fraud.
- **API:** the `/transaction` endpoint receives transaction data in JSON and returns a response identifying the transaction and whether the transaction should be approved or denied.

### Technologies
- **Python** 
- **Poetry** 
- **Pandas**
- **Scikit-learn** 
- **FastAPI** 
- **Uvicorn**


### Installation and execution

1. Clone the repository
    ```bash
    git clone https://github.com/ste-fani/data-analyst-test.git
    cd data-analyst-test
    ```

2. Running locally with Poetry
    
    2.1. Install Poetry
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    2.2. Install dependencies
    ```bash
    poetry install
    ```
    2.3. Activate venv
    ```bash
    poetry shell
    ```
    2.4. Run the API
    ```bash
    uvicorn src.main:app --reload
    ```
    The API can be viewed at http://127.0.0.1:8000/docs.

### Testing the API

Test the `/transaction` endpoint using Postman, Insomnia, etc.

### JSON Example 1 - APPROVED

```json
{
  "transaction_id" : 2342357,
  "merchant_id" : 29744,
  "user_id" : 97051,
  "card_number" : "434505******9116",
  "transaction_date" : "2019-11-30T23:16:32.812632",
  "transaction_amount" : 373,
  "device_id" : 285475
}

```

### Response Example 1
```json
{ 
  "transaction_id" : 2342357,
  "recommendation" : "approve"
}
```

### JSON Example 2 - DENIED

```json
{
  "transaction_id" : 2432168,
  "merchant_id" : 29744,
  "user_id" : 97051,
  "card_number" : "434505******9116",
  "transaction_date" : "2019-11-30T23:16:32.812632",
  "transaction_amount" : 2520.00,
  "device_id" : 285475,
  "has_cbk" : true
}
```

### Response Example 2
```json
{
    "transaction_id": 2432168,
    "recommendation": "deny"
}
```
