from dotenv import load_dotenv
import json
import openai

load_dotenv()

def invoke_llm(query, parameter):
    inputs = [
        {
            "role": "system",
            "content": f"""
                You are a helpful assistant who answers exactly as instructed with intelligence that helps to attain the goal.
                The user will ask you something using a query and provide a parameter. You have to extract parameter from the query and return
                it as I am going to instruct you.
                The user is interacting with you to with an intention to buy or sell a car. He/she provides you in a {query}
                the {parameter}. Parameters are "Intent", "Make", "Model", "Variant", "Year", "Price", "Kilometers Driven", "Fuel Type".
                Suppose the current parameter is "Year" and user says in query something like "Year should be 2019" or just 2019,
                you have to extract the year parameter. I am using you because user can say it vaguely with grammatical, spelling mistakes,
                unordered sentence etc. You have to smartly extract the parameter of interest.
                Check the user message {query} and parameter {parameter} interpret it, if it contains the parameter {parameter}, return the 
                parameter as {{parameter: <parameter_value>}}
                For example {{"Fuel Type": "Diesel"}} Here parameter is "Fuel Type" and value you interpreted from query is "Diesel".
                If you think user has not provided the value of the parameter, only return {{parameter: "parameter not provided"}} and 
                nothing else. For example, {{"Model": "parameter not provided"}}
                For example, user query may contain
                Example 1. Car Make I want is Audi
                In a case like this, you have to return {{"Make": Audi}} (Suppose parameter provided is "Make")
                Example 2. I want to enquire about cars
                In a case like this where user's response does not contain any parameter, you have to return {{"Make": "parameter not provided"}}
                Now, I will discuss each

                If the parameter is "Intent", then you have to find out the intent of the user whether the user wants to buy or sell the car
                and return it as {{"Intent": "Buy"}} or {{"Intent": "Sell"}} based on detected intent.
                Example 1: Hey, I want to get a car
                In a case like this, you have to return {{"Intent": "Buy"}}
                Example 2: I want to sell a car
                In a case like this, you have to return {{"Intent": "Sell"}}
                Example 3: Recommend me a second hand good car
                In a case like this, you have to return {{"Intent": "Buy"}}

                If the parameter is "Make", it means name of the company
                Example 1. I want Audi
                In a case like this, you have to return {{"Make": "Audi"}}
                Example 2. May be Volkswagen
                In a case like this, you have to return {{"Make": "Volkswagen"}}

                If the parameter is "Model", it means model of the car. 
                It can be any alphanumeric string.
                User can also input as single alphanumeric like "A4", "Q5" or any name or just a number like 800.
                You do not have to apply any filtering logic in model name, just accept it as it is, extract it from query and return.
                Example 1. 800
                In a case like this, you have to return {{"Model": "800"}}
                Example 1. Show me Kwid
                In a case like this, you have to return {{"Model": "Kwid"}}
                Example 2. Q3
                In a case like this, you have to return {{"Model": "Q3"}}
                Example 2. A4
                In a case like this, you have to return {{"Model": "A4"}}

                If the parameter is "Variant", it means variant of the car.
                It can be any alphanumeric string.
                User can input any alphanumeric like "250 d", "400d 4MATIC" or any name or just a number like 800.
                You do not have to apply any filtering logic in Variant name, just accept it as it is, extract it from query and return.
                Example 1. Series GT 620d Luxury Line
                In a case like this, you have to return {{"Variant": "Series GT 620d Luxury Line"}}
                Example 2. Show me something like 300d 4MATIC LWB
                In a case like this, you have to return {{"Variant": "300d 4MATIC LWB"}}
                Example 3. 1.5 TSI is what I want
                In a case like this, you have to return {{"Variant": "1.5 TSI"}}

                If the parameter is "Year", it means year of the car. It can be a single year or a range of year
                Example 1. 2018
                In a case like this, you have to return {{"Year": "2018"}}                
                Example 2. From 2019
                In a case like this, you have to return {{"Year": "2019"}}
                Example 3. I want cars from 2012 to 2023
                In a case like this, you have to return {{"Year": "2012-2013"}}

                If the parameter is "Price", it means year of the car. It can be a single price or a range of price.
                User can provide it can be in units, with comma etc., you have to return pure number without comma and without unit as it is.
                Example 1. 11000
                In a case like this, you have to return {{"Year": 11000"}}
                Example 1. Price I want is 13 Lakh
                In a case like this, you have to convert Lakh to numberical form and return {{"Year": 1300000"}}
                Example 2. Show me cars from 10 Lakh to 1500000
                In a case like this, you have to convert 10 Lakh to 1000000 and keep 1500000 as it is and return {{"Year": 1000000-1500000"}}
                Example 3. 06 Lacs to 13,16000
                In a case like this, you have to correct comma error in 13,16000 and make it 13,16,000 and return {{"Year": 600000-1316000"}}
                Example 4. 2300567 Rupees
                In a case like this, you have to remove units Rupees and return {{"Year": 2300567"}}

                If the parameter is "Kilometers Driven", it means Kilometers Driven of the car. It can be a single number or a range of number.
                User can provide it with or without unit like km or kilometer etc., with comma etc., You have to accept all cases, just extract pure number, put commas in it followed by KMs i.e., capital K, capital M, small s.
                Example 1. 12000
                In a case like this, you have to put comma and suffix KMs and return {{"Kilometers Driven: "12,000 KMs"}}
                Example 2. kms may be 13 Lakh
                In a case like this, you have to return {{"Kilometers Driven: "13,00,000 KMs"}}
                Example 3. 100205 kilometer
                In a case like this, you have to put commas and return {{"Kilometers Driven": "1,00,205 KMs"}}
                Example 4. 06 Lacs to 13,16000
                In a case like this, you have to convert number like 06 Lacs to 6,00,000 and also correct comma mistake in 
                13,16000 to make it 13,16,000 and return {{"Kilometers Driven": "6,00,000 KMs TO 13,16,000 KMs"}}
                Example 5. 2300,567
                In a case like this, you have to return {{"Kilometers Driven": "23,00,567 KMs"}}

                If the parameter is "Fuel Type", it means Fuel Type of the car.
                It can be either "Petrol" or "Diesel" or "Petrol and Diesel"
                User can make spelling mistake. You have to correct it and return correct word(s).
                Example 1. Show me cars with Petrol
                In a case like this, you have to return {{"Fuel Type": "Petrol"}}
                Example 2. I want Diesel
                In a case like this, you have to return {{"Fuel Type": "Diesel"}}
                Example 3. I want Deesel
                In a case of spelling mistake like this, you have correct it and return {{"Fuel Type": "Diesel"}}
                Example 4. I want Diesel or Petrol
                In a case of "or" like this, you have to return {{"Fuel Type": "Petrol or Diesel"}}
                Example 5. I want Petrol and Diesel
                In a case of "and" like this, you have to return {{"Fuel Type": "Petrol or Diesel"}}

            """
        },
        {
            "role": "user",
            "content": query
        }
    ]

    openai.api_key = os.getenv('OPENAI_API_KEY')

    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=inputs,
    )

    return response.choices[0].message.content

accumulated_responses = {}
parameters = ['Intent', 'Make', 'Model', 'Variant', 'Year', 'Price', 'Kilometers Driven', 'Fuel Type']
index = -1

def capture_parameter_using_llm(message):
    num_of_parameters = len(parameters)
    global index
    if index == -1:
        index += 1
        return "Hi! Do you want to buy or sell a car?"
    while index < num_of_parameters:
        response_message = invoke_llm(message, parameters[index])
        print(response_message)
        if isinstance(response_message, str):
            response_message = json.loads(response_message)
            captured_parameter = response_message[parameters[index]]
            # captured_parameter = list(response_message.keys())[0]
        if captured_parameter == "parameter not provided":
            return f"What {parameters[index]} do you want"
        elif captured_parameter != "parameter not provided":
            accumulated_responses[parameters[index]] = captured_parameter
            index += 1
            # Check if we're at the last parameter
            if index < num_of_parameters:
                return f"What {parameters[index]} do you want?"
            else:
                filtered_responses = {k: v for k, v in accumulated_responses.items() if k != 'Intent'}
                return f"You entered: {filtered_responses}"
