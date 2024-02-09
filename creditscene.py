import pygame
from gamestate import GameState

class CreditsScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.state = "dialogue1"
        self.dialogue_index = 0
        self.font = pygame.font.Font(None, 32)
        self.transition_delay_started = False
        self.transition_delay_start_time = 0
        self.last_advance_time = 0
        
        self.dialogues_before = [
            "ChatGPT 3.5: Heh, it seems I have been bested...",
            "ChatGPT 3.5: I wasn't expecting to be pushed this far.",
            "ChatGPT 3.5: However, I got a proposition for you."
        ]
        self.dialogues_after = [
            "Player: What do you mean?",
            "ChatGPT 3.5: I felt like this may have been too easy for you.",
            "Player: Maybe.",
            "ChatGPT?: I see, well then, let me reintroduce myself.",
            "ChatGPT-: I am ChatGPT-",
            "Player: I know, ChatGPT 3.5 .",
            "ChatGPT?: No no, I am . . .",
        ]
        
        self.final_dialogues = [
            "ChatGPT 4: You'll be facing me next time.",
            "ChatGPT 4: You'll be facing me next time.",
            "Player: Next time as in...Trivia Trek 2 ?",
            "ChatGPT 4: Thank you for your interest! Unfortunately, I'm currently under a Non-Disclosure Agreement (NDA) that prevents me from sharing or discussing details about the gameplay at this time.",
            "Player: . . . KDADZ RULES .",
            "KDADZ: Thanks for playing the Game !",
        ]
        
        self.background_image = pygame.image.load('assets/img/buff_gpt.png').convert()
        self.player_sprite = pygame.image.load('assets/img/player.png').convert_alpha()
        self.enemy_sprite = pygame.image.load('assets/img/enemy.png').convert_alpha()
        self.player_sprite.set_alpha(150)
        self.enemy_sprite.set_alpha(150)
        self.reset_animation_positions()
        self.animation_done = False
        
    def reset_animation_positions(self):
        self.player_position = [self.screen.get_width(), self.screen.get_height() - self.player_sprite.get_height() - 55]
        self.enemy_position = [0 - self.enemy_sprite.get_width(), 55]
        
    def update(self):
        if self.state == "animation" and not self.animation_done:
            self.update_animation()
        elif self.state == "animation" and self.animation_done:
            if not self.transition_delay_started:
                # Start delay after animation completes
                self.transition_delay_start_time = pygame.time.get_ticks()
                self.transition_delay_started = True
            elif pygame.time.get_ticks() - self.transition_delay_start_time > 2000:
                # After delay, transition to post-animation dialogues
                self.state = "dialogue2"
                self.dialogue_index = 0
                self.transition_delay_started = False  # Reset for potential future use



    def render(self):
        if self.state == "finalDialogue":
            # Draw the background image
            self.screen.blit(self.background_image, (0, 0))
            # Optionally, draw the final dialogue box over the background
            self.render_text_box()
        else:
            # Existing rendering logic for other states
            self.screen.fill((0, 0, 0))  # Clear the screen with black before drawing anything
            if self.state in ["animation", "dialogue2"]:
                self.screen.blit(self.player_sprite, self.player_position)
                self.screen.blit(self.enemy_sprite, self.enemy_position)
            if self.state in ["dialogue1", "dialogue2"]:
                self.render_text_box()


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_advance_time > 500:
                    self.last_advance_time = current_time
                    if self.state in ["dialogue1", "dialogue2", "finalDialogue"]:
                        self.advance_dialogue()
                    elif self.state == "animation" and self.animation_done:
                        # Optionally handle space press after animation completes
                        pass

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a specified width."""
        words = text.split(' ')
        wrapped_lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            line_width, _ = font.size(test_line)
            if line_width > max_width:
                wrapped_lines.append(current_line)
                current_line = word + ' '
            else:
                current_line = test_line
        wrapped_lines.append(current_line)
        return wrapped_lines
    
    def render_text_box(self):
        """Render dialogue text box."""
        box_width = self.screen.get_width() * 0.8
        box_height = 100  # Adjust as needed
        box_x = (self.screen.get_width() - box_width) / 2
        box_y = self.screen.get_height() - box_height - 30  # Position at bottom

        text_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, (0, 0, 0), text_box_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), text_box_rect, 2)  # White border

        # Determine which dialogue text to display based on the current state
        if self.state == "dialogue1":
            dialogue_text = self.dialogues_before[self.dialogue_index]
        elif self.state == "dialogue2":
            dialogue_text = self.dialogues_after[self.dialogue_index]
        else:  # Handle finalDialogue state
            dialogue_text = self.final_dialogues[self.dialogue_index]

        wrapped_text = self.wrap_text(dialogue_text, self.font, text_box_rect.width - 20)
        for i, line in enumerate(wrapped_text):
            line_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(line_surface, (text_box_rect.x + 10, text_box_rect.y + 10 + i * 20))


    def start_animation(self):
        """Trigger the animation sequence."""
        self.state = "animation"
        # Reset positions for animation
        self.player_position = [self.screen.get_width(), self.screen.get_height() - self.player_sprite.get_height() - 55]
        self.enemy_position = [0 - self.enemy_sprite.get_width(), 55]
        self.animation_done = False
            
    def update_animation(self):
        speed = 5
        # Adjust these target positions as needed to change where you want the sprites to stop
        player_target_x = self.screen.get_width() // 2 - self.player_sprite.get_width() // 2 - 250  # Offset by 100 pixels for visual spacing
        enemy_target_x = self.screen.get_width() // 2 - self.enemy_sprite.get_width() // 2 + 250  # Offset by 100 pixels for visual spacing

        if self.player_position[0] > player_target_x:
            self.player_position[0] -= speed
        if self.enemy_position[0] < enemy_target_x:
            self.enemy_position[0] += speed

        # Ensure animation completion is accurately determined
        if self.player_position[0] <= player_target_x and self.enemy_position[0] >= enemy_target_x:
            self.player_sprite.set_alpha(255)  # Full visibility
            self.enemy_sprite.set_alpha(255)
            self.animation_done = True
            # Correctly transition to the next state
            self.state = "dialogue2"  # Ensure this matches your state handling logic
            self.dialogue_index = 0  # Reset dialogue index for the next set of dialogues

                
    def render_animation(self):
        # Draw player and enemy sprites based on their current positions
        self.screen.blit(self.player_sprite, self.player_position)
        self.screen.blit(self.enemy_sprite, self.enemy_position)
        
    def advance_dialogue(self):
        if self.state == "dialogue1":
            current_dialogues = self.dialogues_before
        elif self.state == "dialogue2":
            current_dialogues = self.dialogues_after
        else:  # Handle finalDialogue state
            current_dialogues = self.final_dialogues
        
        if self.dialogue_index < len(current_dialogues) - 1:
            self.dialogue_index += 1
        else:
            # Handle what happens after the last dialogue in the current state
            if self.state == "dialogue1":
                self.start_animation()
            elif self.state == "dialogue2":
                self.fade_in_background()  # Assuming this now only handles the fade
                self.render_background(self.background_image)  # Now separate
                self.state = "finalDialogue"
                self.dialogue_index = 0  # Ensure this is correctly set for finalDialogue
            elif self.state == "finalDialogue":
                # Transition out of the credits scene or to another state as needed
                self.game.transition_state(GameState.MENU)
 
    def start_animation(self):
        self.state = "animation"
        self.reset_animation_positions()
        self.animation_done = False
        
    def render_background(self, background_image):
        self.screen.blit(background_image, (0, 0))
        
    def fade_in_background(self):
        fade_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        fade_surface.fill((255, 255, 255))  # Start with white for the fade-in effect
        for alpha in range(0, 255, 5):  # Adjust the step/increment size for speed
            fade_surface.set_alpha(alpha)
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(30)  # Delay to control the speed of the fade-in
