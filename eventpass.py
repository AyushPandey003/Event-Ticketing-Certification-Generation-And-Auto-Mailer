from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd

def coupons(names: list, certificate: str, font_path: str, qr_folder: str):
    # Create a folder named "certificates" if it doesn't exist
    output_folder = "certificates"
    os.makedirs(output_folder, exist_ok=True)

    for name in names:
        text_y_position = 500
        text_x_position = 1650
        img = Image.open(certificate, mode='r')
        image_width = img.width
        image_height = img.height
        draw = ImageDraw.Draw(img)

        # Load the font using ImageFont.truetype
        font = ImageFont.truetype(font_path, 40)

        # Use textsize method from the ImageDraw object to get text size
        text_width = draw.textlength(name, font=font)
        text_height = draw.textlength(name, font=font)
        text_color = (255, 189, 51)

        draw.text(
            (text_x_position, text_y_position),
            name,
            font=font,
            fill=text_color
        )

        # Specify the full path to the QR code image
        qr_code_path = os.path.join(qr_folder, f"{name}.png")

        # Load QR code image and paste it onto the certificate
        qr_img = Image.open(qr_code_path)
        img.paste(qr_img, (1600, 125))  # You can adjust the position as needed

        # Save the certificate in the "certificates" folder
        certificate_path = os.path.join(output_folder, f"{name}_certificate.png")
        img.save(certificate_path)

# Driver Code
if __name__ == "__main__":
    
    raw_data=pd.read_csv(r"student_info.csv")
    
    name1=raw_data['Name of Member 1']
    reg1=raw_data['Registration Number of Member 1 (if in team)']
    name2=raw_data['Name of Member 2 (If in Team)']
    reg2=raw_data['Registration Number of Member 2 (If in Team) ']
    
    names=[]
    reg_numbers=[]
    filenames=[]
    
    for i in range(len(name1)):
        if(pd.isnull(name2[i])):
            names.append(name1[i])
            reg_numbers.append(reg1[i])
            filenames.append(reg1[i])
        else:
            names.append(name1[i]+" + "+name2[i])
            reg_numbers.append(reg1[i]+" + "+reg2[i])
            filenames.append(reg1[i])
    print(names)
    print(reg_numbers)
    
    # Use the full path to your font file or choose a system font
    FONT = r"C:\Windows\Fonts\Georgia.ttf"  # Replace with the name of a system font or provide the full path to your font file

    # Specify the full path to your certificate PNG file
    CERTIFICATE = "INAUGRAL EVENT LINPACK CLUB (3).png"

    # Specify the folder where QR code images are located
    QR_FOLDER = "qr_codes"

    coupons(filenames, CERTIFICATE, FONT, QR_FOLDER)

