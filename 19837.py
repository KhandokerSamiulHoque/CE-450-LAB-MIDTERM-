import RPi.GPIO as GPIO
import time

SDI_PIN_1 = 13
RCLK_PIN_1 = 12
SRCLK_PIN_1 = 31

SDI_PIN_2 = 18
RCLK_PIN_2 = 15
SRCLK_PIN_2 = 35

alpha_codes = [0x77, 0x7C, 0x58, 0x5E, 0x79, 0x71, 0x6F, 0x74, 0x06, 0x0E, 0x70, 0x38, 0x37, 0x54, 0x5C, 0x73,
             0x67, 0x50, 0x6D, 0x78, 0x1C, 0x62, 0x7E, 0x76, 0x72, 0x5B]

def print_message():
    print('Program is running...')
    print('Please press Ctrl+C to end the program...')

def setup_gpio():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SDI_PIN_1, GPIO.OUT)
    GPIO.setup(RCLK_PIN_1, GPIO.OUT)
    GPIO.setup(SRCLK_PIN_1, GPIO.OUT)
    GPIO.setup(SDI_PIN_2, GPIO.OUT)
    GPIO.setup(RCLK_PIN_2, GPIO.OUT)
    GPIO.setup(SRCLK_PIN_2, GPIO.OUT)

    GPIO.output(SDI_PIN_1, GPIO.LOW)
    GPIO.output(RCLK_PIN_1, GPIO.LOW)
    GPIO.output(SRCLK_PIN_1, GPIO.LOW)
    GPIO.output(SDI_PIN_2, GPIO.LOW)
    GPIO.output(RCLK_PIN_2, GPIO.LOW)
    GPIO.output(SRCLK_PIN_2, GPIO.LOW)

def shift_out(dat, sdi, rclk, srclk):
    for bit in range(0, 8):
        GPIO.output(sdi, 0x80 & (dat << bit))
        GPIO.output(srclk, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(srclk, GPIO.LOW)
    GPIO.output(rclk, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(rclk, GPIO.LOW)

def split_into_pairs(sentence_text):
    string_in_pair = []

    for i in range(1, len(sentence_text)):
        pair = (sentence_text[i-1], sentence_text[i])
        string_in_pair.append(pair)

    return string_in_pair

def display_message(msg_to_display):
    text_pairs = split_into_pairs(msg_to_display)
    while True:
        for pair in text_pairs:
            char1 = pair[0]
            char2 = pair[1]

            if char1.isalpha():
                char_index = ord(char1.upper()) - ord('A')
                if 0 <= char_index < len(alpha_codes):
                    shift_out(alpha_codes[char_index], SDI_PIN_1, RCLK_PIN_1, SRCLK_PIN_1)
            elif char1.isdigit():
                char_index = int(char1)
                if 0 <= char_index < len(alpha_codes):
                    shift_out(alpha_codes[char_index], SDI_PIN_1, RCLK_PIN_1, SRCLK_PIN_1)
            else:
                shift_out(0x00, SDI_PIN_1, RCLK_PIN_1, SRCLK_PIN_1)

            if char2.isalpha():
                char_index = ord(char2.upper()) - ord('A')
                if 0 <= char_index < len(alpha_codes):
                    shift_out(alpha_codes[char_index], SDI_PIN_2, RCLK_PIN_2, SRCLK_PIN_2)
            elif char2.isdigit():
                char_index = int(char2)
                if 0 <= char_index < len(alpha_codes):
                    shift_out(alpha_codes[char_index], SDI_PIN_2, RCLK_PIN_2, SRCLK_PIN_2)

            time.sleep(1)

def cleanup():
    GPIO.cleanup()

if __name__ == '__main__':
    print_message()
    setup_gpio()
    try:
        display_message('hiyoudidgoodjob')
    except KeyboardInterrupt:
        cleanup()