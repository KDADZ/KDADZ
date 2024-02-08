import pygame
import sys
from OpenAI.Question_generator import generate_and_extract_trivia_details
import random
from gamestate import GameState

class TriviaGame:
    def __init__(self, category, game=None, screen=None):
        self.game = game
        self.category = category
        self.screen = screen
        self.points = 0
        self.current_question = None
        self.answers = {}
        self.correct_answer = ""
        self.background = pygame.image.load('assets/img/Trivia-Room.webp')
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.correct_sound = pygame.mixer.Sound('assets/sounds/correct.wav')
        self.incorrect_sound = pygame.mixer.Sound('assets/sounds/wrong.wav')
        self.question_count = 0
        self.max_questions = 3
        self.hovered_answer = None
        self.selection_result = None
        self.load_new_question()

    def load_new_question(self):
        valid_question = False
        while not valid_question:
            trivia_object = generate_and_extract_trivia_details(self.category)
            question_details = trivia_object.get('question1', {})
            self.current_question = question_details.get('Question', '')
            right_answer = question_details.get('Right Answer', '')
            wrong_answers = [answer.split('. ')[1] if '. ' in answer else answer for answer in question_details.get('Wrong Answers', [])]
            all_answers = [right_answer] + wrong_answers if right_answer and wrong_answers else []
            random.shuffle(all_answers)
            self.answers = {chr(97 + i): answer for i, answer in enumerate(all_answers) if answer}
            self.correct_answer = [key for key, value in self.answers.items() if value == right_answer][0]
            if self.current_question and len(all_answers) >= 4:
                valid_question = True
            else:
                self.selection_result = None


    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            text_surface = font.render(test_line, True, (255, 255, 255))
            if text_surface.get_width() > max_width:
                lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line
        lines.append(current_line)
        return lines

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_answer = None
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                for key, box in self.get_answer_boxes(pygame.font.Font(None, 36)).items():
                    if box.collidepoint(mouse_pos):
                        self.hovered_answer = key
                        break
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.process_answer_selection(mouse_pos)
                
    def get_answer_boxes(self, font):
        # Define positions for a 2x2 grid layout
        positions = [(135, 250), (445, 250), (135, 350), (445, 350)]  # Adjust as needed
        answer_boxes = {}
        for i, key in enumerate(sorted(self.answers.keys())):
            answer = self.answers[key]
            x, y = positions[i]
            box = pygame.Rect(x, y, 200, 50)  # Adjust box size as needed
            answer_boxes[key] = box
        return answer_boxes

    def render_question(self, font):
        
        wrapped_text = self.wrap_text(self.current_question, font, 700)
        y_start = 100  # Adjust the start position as needed
        padding = 20  # Increase padding for the dialog box effect
        
        # Calculate the total height of the wrapped text
        text_height_total = sum(font.get_height() for _ in wrapped_text) + padding * 2
        dialog_box_rect = pygame.Rect(50, y_start, 700, text_height_total)  # Define dialog box dimensions
        
        # Draw the dialog box
        pygame.draw.rect(self.screen, (0, 0, 0), dialog_box_rect)  # Dialog box background
        pygame.draw.rect(self.screen, (255, 255, 255), dialog_box_rect, 2)  # Dialog box border
        
        y = y_start + padding / 2  # Start drawing text inside the dialog box
        for line in wrapped_text:
            question_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(question_surface, (dialog_box_rect.x + padding / 2, y))
            y += font.get_height()


    def render_answers(self, font):
        answer_boxes = self.get_answer_boxes(font)
        for key, box in answer_boxes.items():
            color = (100, 100, 255) if key == self.hovered_answer else (0, 0, 0)
            pygame.draw.rect(self.screen, color, box)  # Fill color based on hover
            pygame.draw.rect(self.screen, (255, 255, 255), box, 2)  # Border
            answer_text = f"{key.upper()}: {self.answers[key]}"
            answer_surface = font.render(answer_text, True, (255, 255, 255))
            self.screen.blit(answer_surface, (box.x + 10, box.y + 5))

        if self.selection_result:
            feedback_text = "Correct!" if self.selection_result == 'correct' else "Incorrect..."
            feedback_color = (0, 255, 0) if self.selection_result == 'correct' else (255, 0, 0)
            feedback_surface = font.render(feedback_text, True, feedback_color)
            feedback_rect = feedback_surface.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() - 30))
            pygame.draw.rect(self.screen, (0, 0, 0), feedback_rect.inflate(20, 10))
            self.screen.blit(feedback_surface, feedback_rect)

    def render_feedback(self, font):
        feedback_text = "Correct!" if self.selection_result == 'correct' else "Incorrect..."
        feedback_color = (0, 255, 0) if self.selection_result == 'correct' else (255, 0, 0)
        feedback_surface = font.render(feedback_text, True, feedback_color)
        feedback_rect = feedback_surface.get_rect(center=(self.screen.get_width() / 2, 250))  # Adjust position as needed
        
        # Calculate background box dimensions based on text size
        bg_rect = feedback_rect.inflate(20, 10)  # Inflate rect for padding
        pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)  # Draw background box
        self.screen.blit(feedback_surface, feedback_rect)
        pygame.display.update()  # Ensure the feedback is shown immediately


    def process_answer_selection(self, mouse_pos):
        font = pygame.font.Font(None, 36)
        answer_boxes = self.get_answer_boxes(font)
        for key, box in answer_boxes.items():
            if box.collidepoint(mouse_pos):
                if key == self.correct_answer:
                    print("Correct answer selected!")
                    self.selection_result = 'correct'
                    self.correct_sound.play()
                    self.points += 100
                    self.game.player.add_points(self.points)
                    self.game.player.add_money(int(self.points / 2))

                else:
                    print("Incorrect answer selected!")
                    self.selection_result = 'incorrect'
                    self.incorrect_sound.play()
                    self.game.player.take_damage(1)

                self.render_feedback(font)
                pygame.time.delay(2000)
                    
                self.question_count += 1
                
                if self.question_count >= self.max_questions:
                    if self.game is not None:
                        self.question_count = 0
                        self.selection_result = None
                        self.game.current_level += 1
                        self.game.transition_state(GameState.MID_LEVEL)
                    return
                else:
                    self.load_new_question()
                    self.selection_result = None

    def render(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Adjust alpha for the dim effect
        self.screen.blit(overlay, (0, 0))
        
        # Then draw the background, question, and answers
        self.screen.blit(self.background, (0, 0))
        font = pygame.font.Font(None, 36)
        self.render_question(font)
        self.render_answers(font)

    def update(self):
        pass
