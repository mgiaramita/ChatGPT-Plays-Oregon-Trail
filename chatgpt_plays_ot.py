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


def chatgpt_ot_loop(command, model):
    message_history = [
        {
            "role": "user",
            "content": "You are a user playing Oregon Train, the 1978 tezt based version if the game to be exact. You will receive the output of the game and will make a decision on what move to make next. If the prompt asks for an amount give a whole number response. Most prompts will let you know what the choices are and what decisions can be made. DO NOT respond in full sentences or like talking to a person, your responses should be in the form on commands to play Oregon Trail."
        },
        {"role": "assistant", "content": "OK"},
    ]

    ot_proc = pexpect.spawn(command)
    print("ChatGPT and Oregon Trail are ready to begin.")

    while True:
        # Allow user to moderate
        userin = input("\nUSER: Type EXIT to stop. Enter to continue.\n> ")
        if userin == EXIT_STR:
            break

        # Ensure OT has responded and then read all the current output
        time.sleep(PROC_RSP_WAIT)
        ot_output = ot_proc.read_nonblocking(
            size=PROC_READ_MAX, timeout=PROC_READ_TIMEOUT
        ).decode("utf-8")
        print(f"\n{ot_output}")

        # Send Zork prompt to ChatGPT
        rsp = gen_chat_rsp(ot_output, message_history, model=model)
        print(f"> {rsp}")
        print_tokens()

        # Send ChatGPT generated command to Zork
        ot_proc.sendline(rsp)

    zork_proc.terminate(force=True)


def main():
    # Load dev key, init openai
    config = configparser.ConfigParser()
    config.read("config.ini")
    openai.api_key = config["DEFAULT"]["API_KEY"]

    # Set up and read command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", default=MODEL)
    args = parser.parse_args()
    print(f"M: {args.model}")

    print(LOGO)
    chatgpt_ot_loop(config["DEFAULT"]["CMD"], args.model)


if __name__ == "__main__":
    main()
