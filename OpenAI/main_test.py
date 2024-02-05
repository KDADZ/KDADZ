from OpenAI.Question_generator import generate_and_extract_trivia_details

while  True: 
    choice = input("Enter any key to continue, or Q to quit")
    if choice == 'q':
        break
    generate_and_extract_trivia_details("science")
