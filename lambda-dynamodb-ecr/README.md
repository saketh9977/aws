# What does it do?
1. Trigger AWS Lambda by passing `ip_address` in event payload
2. Lambda does the following -
    - Sends a GET request to [https://api.country.is/<ip_address>](https://api.country.is/<ip_address>) to get country to which the IP address currently belongs to
    - Stores the ip_address:country mapping in DynamoDB

# Additional notes
Refer `docs/` to know how to -
1. Test Lambda locally
2. Push lambda to AWS cloud: both using ECR and zip archive