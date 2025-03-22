
def validate_data(data, historic_violations={}):
    errors = []
    remediation_actions = []
    risk_score = 0  # Start with a base risk score
    
    # Validate that Transaction Amount matches the Reported Amount (with 1% deviation for cross-currency transactions)
    if 'Reported_Amount' not in data:
        errors.append("Reported Amount is required")
        remediation_actions.append("Action: Ensure 'Reported_Amount' is provided for comparison.")
        risk_score += 2  # Increase risk score if Reported Amount is missing
    else:
        transaction_amount = data['Transaction_Amount']
        reported_amount = data['Reported_Amount']
        
        # Check for cross-currency transactions (allow up to 1% deviation)
        if 'is_cross_currency' in data and data['is_cross_currency']:
            allowed_deviation = 0.01 * reported_amount
            if abs(transaction_amount - reported_amount) > allowed_deviation:
                errors.append(f"Transaction Amount deviates from Reported Amount by more than 1% (Allowed deviation: {allowed_deviation})")
                remediation_actions.append(f"Action: Review the transaction for cross-currency discrepancy. Adjust the reported amount or validate cross-currency rates.")
                risk_score += 3  # Increase risk score for high deviation in cross-currency transactions
        else:
            # For non cross-currency transactions, amounts must match exactly
            if transaction_amount != reported_amount:
                errors.append("Transaction Amount must match Reported Amount")
                remediation_actions.append(f"Action: Ensure the transaction amount matches the reported amount.")
                risk_score += 2  # Increase risk score for mismatch

    # Validate Account Balance - should never be negative unless marked as overdraft (OD)
    if 'Account_Balance' in data:
        account_balance = data['Account_Balance']
        if account_balance < 0 and ('Account_Flag' not in data or data['Account_Flag'] != 'OD'):
            errors.append("Account Balance cannot be negative unless flagged as overdraft (OD)")
            remediation_actions.append("Action: Investigate negative balance. If it's a valid overdraft, ensure 'Account_Flag' is set to 'OD'.")
            risk_score += 4  # High risk for negative balance without OD flag


    # Validate cross-border transaction limits (for simplicity, assuming a cross-border flag is set)
    if 'is_cross_border' in data and data['is_cross_border']:
        # Example limit check, assume the cross-border limit is $5000 for simplicity
        if data['Transaction_Amount'] > 5000:
            errors.append("Transaction exceeds cross-border transaction limits")
            remediation_actions.append("Action: Cross-border transaction limit exceeded. Ensure the transaction adheres to regulatory limits or obtain necessary approval.")
            risk_score += 5  # Cross-border limit violations increase risk

    # Adjust the risk score based on the customer's historical violations
    if data['Customer_ID'] in historic_violations:
        historic_score = historic_violations[data['Customer_ID']]
        errors.append(f"Customer has {historic_score} previous violations.")
        remediation_actions.append(f"Action: Review the customer's history of violations. Consider manual review.")
        risk_score += historic_score  # Add historic violations to the current risk score

    # Return errors, remediation actions, and the final risk score
    return errors, remediation_actions, risk_score

