
#                               '''start '''


from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import requests
import re


# Initialize Ollama LLaMA2 model
llm = OllamaLLM(model="llama3" , temperature=0)


                            # Define prompt to detect intent

prompt = PromptTemplate(
    input_variables=["user_input"],
    template="Identify the intent in the user message: '{user_input}'. and return only either 'GET_ORDER_DETAILS' or 'CANCEL_ORDER' based on the intent."
)

                                # Intent detection function

def detect_intent(user_input):
    llm_chain = prompt | llm
    response = llm_chain.invoke({"user_input": user_input})
    intent = response.strip().upper()
    return intent





                                # Define intent handlers

def handle_get_order_details(order_id):
    url = f"http://localhost:3001/order/{order_id}"
    response = requests.get(url)
    # for data 
    print("Item_name:->", response.json()["data"]["item"])
    print("Status:->", response.json()["data"]["status"])

    return ""

def handle_cancel_order(order_id):
    url = f"http://localhost:3001/order/{order_id}/cancel"
    response = requests.post(url)

    if response.json()["status"] == "success":
        print("Order canceled successfully.")
    else:
        print("Failed to cancel order.")
    res = response.json()
    return res["message"]




def process_user_input(user_input):

    intent = detect_intent(user_input)

    if "GET_ORDER_DETAILS" in intent:
       
        order_id = extract_order_id(user_input)
        return handle_get_order_details(order_id)

    elif "CANCEL_ORDER" in intent :
        order_id = extract_order_id(user_input)
        return handle_cancel_order(order_id)
       
    else:
        return {"message": "Sorry, I couldn't understand the request."}

# Helper function to extract order ID
def extract_order_id(user_input):

    # reg
    # important is that user id is always start  with "OY"
    pattern = r"\bOY\d+\b"
    match = re.search(pattern, user_input)
    
    # Return the matched order ID or None if not found
    return match.group(0) if match else None



if __name__ == "__main__":
    while True:
        # it must contain order id start with "OY"
        user_input = input("User: ")
        result = process_user_input(user_input)
        print("Response:", result)



