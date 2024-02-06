import pygame
from test_fetch import get_question
from OpenAI.Question_generator import generate_and_extract_trivia_details
import random

pygame.init()

class TriviaGame:
    def __init__(self, category):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.category = category
        self.points = 0  # Player points
        self.current_question = None
        self.answers = {}
        self.correct_answer = ""
        self.load_new_question()

    def load_new_question(self):
        trivia_object = generate_and_extract_trivia_details(self.category)
        question_details = trivia_object['question1']  # Accessing the nested dictionary for question1
    
        self.current_question = question_details['Question']
    
        # Combine right and wrong answers into a single list
        all_answers = question_details['Wrong Answers'] + [question_details['Right Answer']]
    
        # Remove numbering from wrong answers if necessary (e.g., '1. Brain' becomes 'Brain')
        all_answers = [answer if answer == question_details['Right Answer'] else answer[3:] for answer in all_answers]
    
        # Shuffle the combined list of answers to randomize their order
        random.shuffle(all_answers)
    
        # Map the shuffled answers to the answer options (a, b, c, d)
        self.answers = {chr(97 + i): answer for i, answer in enumerate(all_answers)}
    
        # Identify the correct answer's key based on its position after shuffling
        self.correct_answer = [key for key, value in self.answers.items() if value == question_details['Right Answer']][0]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.process_answer_selection(event.pos)

    def process_answer_selection(self, mouse_pos):
        answer_boxes = self.get_answer_boxes()
        for key, box in answer_boxes.items():
            if box.collidepoint(mouse_pos):
                if key == self.correct_answer:
                    print("Correct answer selected!")
                    self.points += 10
                else:
                    print("Incorrect answer selected!")
                    self.points -= 10
                self.load_new_question()  # Load new question after an answer is selected
                break

    def get_answer_boxes(self):
        font = pygame.font.Font(None, 36)
        answer_boxes = {}
        for index, (key, answer) in enumerate(self.answers.items()):
            text_surface = font.render(f"{key}: {answer}", True, (255, 255, 255))
            box = text_surface.get_rect(topleft=(100, 150 + index * 50))
            answer_boxes[key] = box
        return answer_boxes

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear the screen
        font = pygame.font.Font(None, 36)
        question_surface = font.render(self.current_question, True, (255, 255, 255))
        self.screen.blit(question_surface, (100, 100))
        
        for index, (key, answer) in enumerate(self.answers.items()):
            answer_surface = font.render(f"{key}: {answer}", True, (255, 255, 255))
            self.screen.blit(answer_surface, (100, 150 + index * 50))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.render()
            self.clock.tick(60)

if __name__ == "__main__":
    category = "general knowledge"  # Example category
    game = TriviaGame(category)
    game.run()
    
