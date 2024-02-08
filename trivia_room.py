import pygame
import sys
from OpenAI.Question_generator import generate_and_extract_trivia_details
import random
from gamestate import GameState

class TriviaGame:
    def __init__(self, category, game = None, screen=None):
        self.game = game
        self.category = category
        self.screen = screen
        self.points = 0
        self.current_question = None
        self.answers = {}
        self.correct_answer = ""
        self.background = pygame.image.load('assets/img/Trivia-Room.webp')
        self.background = pygame.transform.scale(self.background, (800, 600))
        self.question_count = 0
        self.max_questions = 3
        self.load_new_question()

    def load_new_question(self):
        trivia_object = generate_and_extract_trivia_details(self.category)
        question_details = trivia_object['question1']

        self.current_question = question_details['Question']

        # Directly use the right and wrong answers, assuming wrong answers have numerical prefixes
        right_answer = question_details['Right Answer']
        wrong_answers = [answer.split('. ')[1] if '. ' in answer else answer for answer in question_details['Wrong Answers']]

        all_answers = [right_answer] + wrong_answers

        # Shuffle the combined list of answers to randomize their order
        random.shuffle(all_answers)

        # Map the shuffled answers to the answer options (a, b, c, d)
        self.answers = {chr(97 + i): answer for i, answer in enumerate(all_answers)}

        # Identify the correct answer's key based on its position after shuffling
        self.correct_answer = [key for key, value in self.answers.items() if value == right_answer][0]


    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            # Check if adding the next word would exceed the max width
            test_line = current_line + word + ' '
            text_surface = font.render(test_line, True, (255, 255, 255))
            if text_surface.get_width() > max_width:
                lines.append(current_line)  # Add current line to lines list
                current_line = word + ' '  # Start a new line with the current word
            else:
                current_line = test_line
        lines.append(current_line)  # Add the last line
        return lines

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.process_answer_selection(event.pos)

    def process_answer_selection(self, mouse_pos):
        font = pygame.font.Font(None, 24)  # Match the font size with render_answers
        answer_boxes = self.get_answer_boxes(font)
        for key, box in answer_boxes.items():
            if box.collidepoint(mouse_pos):
                if key == self.correct_answer:
                    print("Correct answer selected!")
                    self.points += 10
                else:
                    print("Incorrect answer selected!")
                    self.points -= 10

                self.question_count += 1  # Increment the question count here
                
                if self.question_count >= self.max_questions:
                    if self.game:
                        self.game.transition_state(GameState.MID_LEVEL)
                    return

                self.load_new_question()

    def get_answer_boxes(self, font):
        screen_width = self.screen.get_width()
        answer_width_total = sum([font.size(f"{key.upper()}: {answer}")[0] for key, answer in self.answers.items()]) + (len(self.answers) - 1) * 20  # 20 pixels spacing
        starting_x = (screen_width - answer_width_total) // 2

        y = self.screen.get_height() - 60  # Y position for answers, adjusted for bottom
        answer_boxes = {}
    
        x = starting_x
        for key, answer in sorted(self.answers.items()):
            answer_text = f"{key.upper()}: {answer}"
            text_width, text_height = font.size(answer_text)
            # Create a rect for each answer
            answer_boxes[key] = pygame.Rect(x, y, text_width, text_height)
            x += text_width + 20  # Move x for the next answer, adding spacing

        return answer_boxes

    def render_question(self, font):
        # First, wrap the text as before
        wrapped_text = self.wrap_text(self.current_question, font, 700)  # Adjust width as needed
        y_start = 50  # Starting y position for the question, adjust as needed
        padding = 10  # Padding around the text
        
        # Calculate the height of the background based on the number of lines and font size
        background_height = len(wrapped_text) * (font.get_height() + padding) + padding
        
        # Draw the background rectangle slightly wider than the text for padding
        pygame.draw.rect(self.screen, (0, 0, 0), (40, y_start - padding, 720, background_height))
        
        # Render each line of the question text
        y = y_start
        for line in wrapped_text:
            question_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(question_surface, (50, y))
            y += font.get_height() + padding

    def render_answers(self, font):
        screen_width = self.screen.get_width()
        answer_width_total = sum([font.size(f"{key.upper()}: {answer}")[0] for key, answer in self.answers.items()]) + (len(self.answers) - 1) * 20  # 20 pixels spacing
        starting_x = (screen_width - answer_width_total) // 2

        y = self.screen.get_height() - 60  # Adjust so answers are at the bottom, consider font size and padding
        x = starting_x

        for key, answer in sorted(self.answers.items()):
            answer_text = f"{key.upper()}: {answer}"
            answer_surface = font.render(answer_text, True, (255, 255, 255))
            self.screen.blit(answer_surface, (x, y))
            x += answer_surface.get_width() + 20  # Add spacing between answers

    def process_answer_selection(self, mouse_pos):
        font = pygame.font.Font(None, 36)  
        answer_boxes = self.get_answer_boxes(font)
        for key, box in answer_boxes.items():
            if box.collidepoint(mouse_pos):
                if key == self.correct_answer:
                    print("Correct answer selected!")
                    self.points += 10
                else:
                    damage = 1
                    self.game.player.take_damage(damage)
                    print("Incorrect answer selected!")
                    self.points -= 10

                self.question_count += 1  
                
                if self.question_count >= self.max_questions:
                    if self.game is not None:
                        self.game.transition_state(GameState.MID_LEVEL) 
                    else:
                        print("Would transition to MidLevel state here.")  
                    return  

                self.load_new_question()

    def render(self):
        self.screen.blit(self.background, (0, 0))  # Draw the background image
        
        font = pygame.font.Font(None, 36)  # Adjust the font size as needed
        
        self.render_question(font)  # Draw the question with its background
        self.render_answers(font)  # Draw the answers horizontally at the bottom

        
    def update(self):
        pass
