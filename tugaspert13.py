from PIL import Image

# Function to hide text within an image
def hide_text(image_path, text_to_hide, output_image_path):
    # Open the image
    image = Image.open(image_path)
    # Convert the image to RGB (if it's not already)
    image = image.convert("RGB")

    # Convert text to binary
    binary = ''.join(format(ord(char), '08b') for char in text_to_hide)

    # Add null terminator to indicate end of message
    binary += '1111111111111110'

    print("Binary representation of text to hide:", binary)

    if len(binary) > image.width * image.height * 3:
        raise ValueError("Text too long to hide in the image")

    data_index = 0
    for x in range(image.width):
        for y in range(image.height):
            # Get the pixel RGB value
            pixel = list(image.getpixel((x, y)))

            # Modify the least significant bit (LSB) of each color component
            for i in range(3):
                if data_index < len(binary):
                    pixel[i] = pixel[i] & ~1 | int(binary[data_index])
                    data_index += 1

            # Save modified pixel back to the image
            image.putpixel((x, y), tuple(pixel))

            # Check if message has been fully hidden
            if data_index >= len(binary):
                break

    # Save the modified image as PNG format
    image_rgb = image.convert("RGB")
    image_rgb.save(output_image_path, format="PNG")

    # Return the output image path
    return output_image_path

# Example usage
image_path = "image.png"
output_image_path = "image_with_hidden_text.png"
text_to_hide = "Hello, this is a secret message!"
output_image_path = hide_text(image_path, text_to_hide, output_image_path)

# Function to extract text from an image
def extract_text(image_path):
    # Open the image
    image = Image.open(image_path)
    # Convert the image to RGB (if it's not already)
    image = image.convert("RGB")

    binary = ""
    for x in range(image.width):
        for y in range(image.height):
            # Get the pixel RGB value
            pixel = image.getpixel((x, y))

            # Extract LSB from each color component
            for i in range(3):
                binary += str(pixel[i] & 1)

    # Split binary data into characters until the null terminator is encountered
    text = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        if byte == '1111111111111110':
            break
        text += chr(int(byte, 2))

    print("Extracted text:", text)

    return text


extracted_text = extract_text(output_image_path)
print("Extracted text:", extracted_text)
