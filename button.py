class Button:
    def __init__(self, text, pos, font, base_color, hovering_color):
        self.text = text
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.current_color = base_color
        self.rendered_text = self.font.render(self.text, True, self.current_color)
        self.rect = self.rendered_text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        # Render text with the current color
        self.rendered_text = self.font.render(self.text, True, self.current_color)
        # Draw the text on the screen
        screen.blit(self.rendered_text, self.rect)

    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            return True
        return False

    def change_color(self, position):
        # Change the color when hovering over the button
        if self.rect.collidepoint(position):
            self.current_color = self.hovering_color
        else:
            self.current_color = self.base_color