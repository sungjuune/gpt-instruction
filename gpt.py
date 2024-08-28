from openai import OpenAI
import json
import argparse
from tqdm import tqdm


def GPT(instruction):
    instruction_str = '\n'.join(instruction)

    response = CLIENT.chat.completions.create(
    model="gpt-4o",
    messages=[
    {"role":"system","content":SYSTEM_CONTENT},
    {"role":"user","content":instruction_str}
    ]
    )
    result = response.choices[0].message.content
    return result


def main(args):
    global CLIENT, SYSTEM_CONTENT
    CLIENT = OpenAI(api_key = "")
    SYSTEM_CONTENT = \
"""
From now on, you will be my helpful assistant on paraphrasing the\
language instruction for a navigation robot.\
Preserving the context and the goal of the given instruction,\
paraphrase the sentences using new vocabularies, new phrases, and new tone of voice, \
as if the instructions are given by another human user. \
Please do not generate any reply for this content prompt, and just generate the paraphrased instructions.
"""
    with open(f"./REVERIE_{args.split}_original.json", 'r') as file:
        instructions = json.load(file)

    dict_ = {}
    for key in tqdm(instructions):
        instruction_list = instructions[key]
        result = GPT(instruction_list).split('\n')
        dict_[key] = result

    with open(f"./REVERIE_{args.split}_new.json", "w") as json_file:
        json.dump(dict_, json_file)        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--split', type=str)
    args = parser.parse_args()
    main(args)