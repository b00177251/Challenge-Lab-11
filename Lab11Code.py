import string
from base64 import b64decode

# Read the intercepted ciphertext from a file
# Read the intercepted ciphertext from a file
file_path = 'intercepted.txt'


with open(file_path, 'r') as file:
    intercepted_text = file.read().strip()

# Decryption functions
def decrypt_step1(encoded_text):
    # Reverse substitution cipher
    original = "mlkjihgfedcbaMLKJIHGFEDCBAzyxwvutsrqponZYXWVUTSRQPON"
    substitution = "zyxwvutsrqponZYXWVUTSRQPONmlkjihgfedcbaMLKJIHGFEDCBA"
    table = str.maketrans(substitution, original)
    return encoded_text.translate(table)

def decrypt_step2(encoded_text):
    # Decode Base64
    return b64decode(encoded_text).decode()

def decrypt_step3(encoded_text):
    # Reverse Caesar cipher with a shift of 4
    shift = 4
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(shifted_alphabet, alphabet)
    return encoded_text.translate(table)

# Mapping step numbers to decryption functions
decryption_steps = {
    '1': decrypt_step1,
    '2': decrypt_step2,
    '3': decrypt_step3
}

def iterative_decrypt(ciphertext):
    # Track the sequence of steps for debugging
    steps_taken = []
    message = ciphertext

    # Continue until no numeric step prefix is found
    while message and message[0].isdigit():
        step_num = message[0] # Extract the step number
        steps_taken.append(step_num)
        message = message[1:] # Remove step number
        try:
            # Dynamically call the decryption function for this step
            decrypt_func = decryption_steps[step_num]
            message = decrypt_func(message)
        except KeyError:
            raise ValueError(f"Unknown decryption step: {step_num}")

    return message, steps_taken

# Main decryption process
try:
    plaintext, steps = iterative_decrypt(intercepted_text)
    print("Decrypted Message:", plaintext)
    print("Decryption Steps Taken:", " -> ".join(steps))
except Exception as e:
    print("An error occurred during decryption:", e)