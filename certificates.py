from PIL import Image, ImageDraw, ImageFont
import os
import csv

def generate_certificates(names: list, certificate: str, font_path: str):
    for name in names:
        # Adjust text position based on student name position
        # Example: Calculate text_x_position and text_y_position for each student

        img = Image.open(certificate, mode='r')
        draw = ImageDraw.Draw(img)

        # Load the font using ImageFont.truetype
        font = ImageFont.truetype(font_path, 80)

        # Use textsize method from the ImageDraw object to get text size
        text_width = draw.textlength(name, font=font)
        text_height =draw.textlength(name, font=font)
        text_color = (52, 67, 93)

        # Adjust text position based on student name position
        text_x_position = 900
        text_y_position = 860

        draw.text(
            (text_x_position, text_y_position),
            name,
            font=font,
            fill=text_color,stroke_width=2,stroke_fill=(0,0,0)
        )

        # Specify the directory where certificates will be saved
        save_directory = r"certificates2"
        os.makedirs(save_directory, exist_ok=True)
        img.save(os.path.join(save_directory, f"{name}.png"))

# Read student names from CSV file
def read_student_names_from_csv(csv_file):
    student_names = []
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            student_names.append(row['Name of Member 1'])  # Replace with the appropriate column name
            student_names.append(row['Name of Member 2 (If in Team)'])  # Replace with the appropriate column name
    return student_names

if __name__ == "__main__":
    # Specify the full path to your font file
    FONT = r"C:\Windows\Fonts\Georgia.ttf"

    # Specify the full path to your certificate PNG file
    CERTIFICATE = r"event.jpg"

    # Read student names from CSV file (replace with your CSV file path)
    student_names = read_student_names_from_csv('student_info.csv')
    # print(student_names)

    # Generate certificates for each student
    generate_certificates(student_names, CERTIFICATE, FONT)
