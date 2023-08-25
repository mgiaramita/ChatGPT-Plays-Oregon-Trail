import argparse
import configparser
import openai
import os
import pexpect
import time


MODEL = "gpt-3.5-turbo"
EXIT_STR = "EXIT"


PROC_READ_MAX = 1000000
PROC_READ_TIMEOUT = 5
PROC_RSP_WAIT = 1.5


LOGO = """
   ____ _           _    ____ ____ _____                
  / ___| |__   __ _| |_ / ___|  _ \_   _|               
 | |   | '_ \ / _` | __| |  _| |_) || |                 
 | |___| | | | (_| | |_| |_| |  __/ | |                 
  \____|_| |_|\__,_|\__|\____|_|    |_|                 
 |  _ \| | __ _ _   _ ___                               
 | |_) | |/ _` | | | / __|                              
 |  __/| | (_| | |_| \__ \                              
 |_|__ |_|\__,_|\__, |___/           _____          _ _ 
  / _ \ _ __ ___|___/_  ___  _ __   |_   _| __ __ _(_) |
 | | | | '__/ _ \/ _` |/ _ \| '_ \    | || '__/ _` | | |
 | |_| | | |  __/ (_| | (_) | | | |   | || | | (_| | | |
  \___/|_|  \___|\__, |\___/|_| |_|   |_||_|  \__,_|_|_|
                 |___/                                  
"""

tokens_input = 0
tokens_output = 0


def print_tokens():
    print(f"Tokens In: {tokens_input}, Tokens Out: {tokens_output}\n")


def gen_chat_rsp(message, message_history, role="user", model=MODEL):
    global tokens_input, tokens_output

    # Generate response to message + history
    message_history.append({"role": role, "content": f"{message}"})
    try:
        completion = openai.ChatCompletion.create(model=model, messages=message_history)
        reply = completion.choices[0].message.content

        # Keep track of usage ($$$)
        tokens_input = completion.usage.prompt_tokens
        tokens_output = completion.usage.completion_tokens
    except Exception as e:
        # Response failed, give default (error) response
        reply = "An Error occurred. Please try again."

    # Update message history
    message_history.append({"role": "assistant", "content": f"{reply}"})

    return reply


def chatgpt_ot_loop(command, model, moderate=True):
    message_history = [
        {
            "role": "user",
            "content": "You are a user playing Oregon Train, the 1978 text based version if the game to be exact. You will receive the output of the game and will make a decision on what move to make next. If the prompt asks for an amount give a whole number response. Most prompts will let you know what the choices are and what decisions can be made. DO NOT respond in full sentences or like talking to a person, your responses should be in the form on commands to play Oregon Trail.",
        },
        {"role": "assistant", "content": "OK"},
    ]

    ot_proc = pexpect.spawn(command, echo=False)
    print("ChatGPT and Oregon Trail are ready to begin.")

    try:
        while True:
            # Allow user to moderate
            if moderate:
                userin = input("\nUSER: Type EXIT to stop. Enter to continue.\n> ")
                if userin == EXIT_STR:
                    break

            # Ensure OT has responded and then read all the current output
            time.sleep(PROC_RSP_WAIT)
            ot_output = ot_proc.read_nonblocking(
                size=PROC_READ_MAX, timeout=PROC_READ_TIMEOUT
            ).decode("utf-8")
            print(f"\n{ot_output}")

            # Send Oregon Trail prompt to ChatGPT
            rsp = gen_chat_rsp(ot_output, message_history, model=model)
            print(f"> {rsp}")
            print_tokens()

            # Send ChatGPT generated command to Oregon Trail
            ot_proc.sendline(rsp)
    except Exception as e:
        print("\nTERMINATE CONDITION HIT")

    ot_proc.terminate(force=True)


def main():
    # Load dev key, init openai
    config = configparser.ConfigParser()
    config.read("config.ini")
    openai.api_key = config["DEFAULT"]["API_KEY"]

    # Set up and read command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", default=MODEL)
    parser.add_argument("-U", "--UNLEASHED", action="store_true", default=False)
    args = parser.parse_args()
    print(f"M: {args.model}")

    if args.UNLEASHED:
        print(
            "WARNING: This mode will let the AI play until the program terminates. Be ready to stop or kill the this process as necessary!"
        )
        userin = input("\nUSER: Press ENTER to let ChatGPT play in UNLEASHED mode.\n> ")

    print(LOGO)
    chatgpt_ot_loop(config["DEFAULT"]["CMD"], args.model, not args.UNLEASHED)


if __name__ == "__main__":
    main()
