import json

# loading the memory (knowledge base)
def load_knowledge_base():
    
    """Load all the FAQs from the JSON file. """
    
    with open("knowledge_base.json", "r") as file:
        return json.load(file)
    
# searching for the best relevent answer
def find_best_answer(user_question):
    
    """Find the most relevant answer using keyword matching."""
    
    knowledge = load_knowledge_base()
    user_question = user_question.lower()
    for item in knowledge:
        if any(word in item["question"].lower() for word in user_question.split()):
            return item["answer"]
    return None
































# main function
if __name__ == "__main__":

    question = input("Ask something: ")
    answer = find_best_answer(question)

    if answer:
        print(answer)
    else:
        print("Sorry, I couldn't find an answer.")