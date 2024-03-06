# import hashlib
# import qrcode
# import json

# def generate_unique_code(name, reg_number):
#     raw_unique_code = f"{name}_{reg_number}"
#     hashed_code = hashlib.sha256(raw_unique_code.encode()).hexdigest()

#     print(f"Hashed Code: {hashed_code}")

#     # Generate QR code for the hashed key
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     qr.add_data(hashed_code)
#     qr.make(fit=True)

#     # Create an image from the QR code
#     qr_image = qr.make_image(fill_color="black", back_color="white").resize((300,300))
  

#     # Save the QR code image
#     qr_image.save(f"./qr_codes/{reg_number}.png")

#     return hashed_code

# def save_to_file(name, reg_number, hashed_code):
#     new_data = {
#         "name": name,
#         "reg_number": reg_number,
#         "hashed_code": hashed_code
#     }

#     try:
#         with open("./student_info.json", 'r') as f:
#             data = json.load(f)
#     except FileNotFoundError:
#         # If the file doesn't exist yet, create an empty list
#         data = []

#     data.append(new_data)

#     with open(r"C:\Users\ayush\Desktop\QRscanner\student_info.json",'w') as f:
#         json.dump(data, f, indent=2)


# if __name__ == "__main__":
#     name = input("Enter Name: ")
#     reg_number = input("Enter Registration Number: ")
#     hashed_code = generate_unique_code(name, reg_number)

#     save_to_file(name, reg_number, hashed_code)

#     print(f"Information saved successfully. QR Code generated for hashed key: {hashed_code}")

import hashlib
import qrcode
import json
import pandas as pd

def generate_unique_codes(names, reg_numbers):
    hashed_codes = []

    for name, reg_number in zip(names, reg_numbers):
        raw_unique_code = f"{name}_{reg_number}"
        hashed_code = hashlib.sha256(raw_unique_code.encode()).hexdigest()
        hashed_codes.append(hashed_code)

        print(f"Hashed Code for {name}: {hashed_code}")

        # Generate QR code for the hashed key
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(hashed_code)
        qr.make(fit=True)

        # Create an image from the QR code
        qr_image = qr.make_image(fill_color="black", back_color="white").resize((300, 300))

        # Save the QR code image
        qr_image.save(f"./qr_codes/{reg_number}.png")

    return hashed_codes

def save_to_file(names, reg_numbers, hashed_codes, filenames):
    data = []

    for name, reg_number, hashed_code, filename in zip(names, reg_numbers, hashed_codes, filenames):
        data.append({
            "name": name,
            "reg_number": reg_number,
            "hashed_code": hashed_code,
            "filename": f"{filename}.png"
        })

    with open(r"C:\Users\ayush\Desktop\QRscanner\student_info.json", 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # Provide separate lists for names and registration numbers
    # names = ['Jay Johri']
    # reg_numbers = ['22BAC10020']
    
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
    

    hashed_codes = generate_unique_codes(names, filenames)
    save_to_file(names, reg_numbers, hashed_codes, filenames)

    print("Information saved successfully. QR Codes generated.")

