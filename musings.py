#!/usr/bin/env python3

import argparse
import decouple
import os
import random
import textwrap

import openai

openai.api_key = decouple.config("OPENAI_API_KEY")

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instruction", "-i", default="Reflect on")
    parser.add_argument("--max-tokens", "-x", type=int, default=128)
    parser.add_argument("--model", "-m",default="text-davinci-003")
    parser.add_argument("--prompt", "-p", type=str)
    parser.add_argument("--prompts-file", "-f", type=str, default="$HOME/Sync/noticeboard-reading/desiderata.txt")
    parser.add_argument("--temperature", "--temp", "-t", type=float, default=0.5)
    return vars(parser.parse_args())

def musing(model: str, temperature: float, max_tokens: int, prompts_file: str, prompt: str, instruction: str):
    prompt_text = prompt or (random.choice(
        [line
         for line in (line.strip()
                      for line in open(os.path.expandvars(prompts_file),
                                       encoding='utf-8').readlines())
         if line]))
    response = openai.Completion.create(
        model=model,
        prompt="{} this: {}".format(instruction, prompt_text),
        temperature=temperature,
        max_tokens=max_tokens,
    )
    print(textwrap.fill ("A reflection on: " + prompt_text, initial_indent=''))
    print()
    print(textwrap.fill(response['choices'][0]['text'].strip(), initial_indent=''))

if __name__ == "__main__":
    musing(**get_args())
