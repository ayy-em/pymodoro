from PIL import Image, ImageDraw


def create_image():
    # Generate an image for the tray icon
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.rectangle(
            (width // 2, 0, width, height // 2),
            fill=(255, 0, 0))
    dc.rectangle(
            (0, height // 2, width // 2, height),
            fill=(255, 0, 0))
    return image


def get_image():
    relative_path = "assets/timer-icon.png"
    try:
        # file_obj = open(relative_path, "rb")  # Open the file in binary mode
        img = Image.open(relative_path)
        return img
    except FileNotFoundError:
        print(f"File {relative_path} not found.")
        return None
