import pygame



# allows quitting during visualization to avoid staying stuck
def handle_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

# used for resizing window in main file
def update_layout(height, width, cols):
    cell_size = height // cols
    scale = height / 600
    scaled_ui_width = int(200 * scale)
    button_x = width - scaled_ui_width + 5
    return cell_size, button_x, scale

