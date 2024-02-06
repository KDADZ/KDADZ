import pygame
from test_fetch import get_question

class TriviaRoom:
    def __init__(self, game, category):
        self.game = game
        self.category = category
        self.current_question = None
        self.answers = {}
        self.correct_answer = ""
        self.load_new_question()

    def load_new_question(self):
        # This is a placeholder.
        question_data, wrong_answer, right_answer = get_question(self.category)
        self.current_question = question_data['question']
        self.answers = question_data['answers']
        self.correct_answer = question_data['correct_answer']
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                answer_boxes = self.get_answer_boxes()
                for key, box in answer_boxes.items():
                    if box.collidepoint(mouse_pos):
                        self.process_answer_selection(key)
                        break

    def process_answer_selection(self, selected_key):
        if selected_key == self.correct_answer:
            print("Correct answer selected!")
            self.game.player.add_points(10)
        else:
            print("Incorrect answer selected!")
            self.game.player.lose_points(10)
            
    def get_answer_boxes(self):
        font = pygame.font.Font(None, 36)
        answer_boxes = {}
        for index, (key, answer) in enumerate(self.answers.items()):
            text_surface = font.render(f"{key}: {answer}", True, (255, 255, 255))
            box = text_surface.get_rect(topleft=(100, 150 + index * 50))
            answer_boxes[key] = box
        return answer_boxes
    
    def update(self):
        pass

    def render(self):
        font = pygame.font.Font(None, 36)  # Specify a valid font path if not using the default font
        question_surface = font.render(self.current_question, True, (255, 255, 255))
        self.game.screen.blit(question_surface, (100, 100))
        
        # Render the answers
        for index, (key, answer) in enumerate(self.answers.items()):
            answer_surface = font.render(f"{key}: {answer}", True, (255, 255, 255))
            self.game.screen.blit(answer_surface, (100, 150 + index * 50))
        
        pygame.display.flip()
