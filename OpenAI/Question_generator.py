from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

category = ""
last_five_questions = []
trivia_object = {}

def generate_and_extract_trivia_details(category):
    
    global last_five_questions 
    global trivia_object
    
    max_attempts = 5
    questions_added = 0
    
    while questions_added < 1 and len(trivia_object) < 2:
        for _ in range(max_attempts):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"Generate a trivia question about {category} and return the question, the right answer, and three wrong answers. Ensure the wrong answers are formatted like this example: Wrong Answers: \n1. Chevrolet\n2. Toyota\n3. Honda. also, make sure the question asked does not match any in {last_five_questions}"}
                    ]
                )
                
                # Extract trivia details from the response
                content = response.choices[0].message.content
                question = ""
                right_answer = ""
                wrong_answers = []
                trivia_object = {}
                
                
                sections = content.split('\n\n')
                for section in sections:
                  
                    if section.startswith("Question:"):
                        question = section.replace("Question:", "").strip()
                        
                    elif section.startswith("Right Answer:"):
                        right_answer = section.replace("Right Answer:", "").strip()
                        
                    elif section.startswith("Wrong Answers:"):
                        wrong_answers_lines = section.replace("Wrong Answers:", "").strip().split('\n')
                        wrong_answers = [line.strip() for line in wrong_answers_lines]

                    
                    
                # Check if the generated question is in the last five questions
                if question not in last_five_questions:
                    last_five_questions.append(question)
                    
                    if len(last_five_questions) > 5:
                        last_five_questions.pop(0)
                        
                    
                    # Dynamically generate the key based on the number of existing entries
                    key = f"question{len(trivia_object) + 1}"
                    trivia_object[key] = {"Question": question, "Right Answer": right_answer, "Wrong Answers": wrong_answers}
                    
                    questions_added += 1

                   

                    # Assuming you want to break the loop after successfully adding a non-repeated question
                    break
                

            except Exception as e:
                print(f"An error occurred: {e}")
                return trivia_object
            
            if questions_added >= 5 or len(trivia_object) >= 5:
                break

    print("trivia object", trivia_object)
    return trivia_object



# question, right_answer, wrong_answers = generate_and_extract_trivia_details(category)
# res_trivia_object = generate_and_extract_trivia_details(category)
# print("res trivia object" , res_trivia_object)
# print("Question:", question)
# print("Right Answer:", right_answer)
# print("Wrong Answers:", ', '.join(wrong_answers))
# print("last five",last_five_questions)




# add state to insure last five questions arent reasked

# Rewrite to soley get what i need with one category, then work towards persistence