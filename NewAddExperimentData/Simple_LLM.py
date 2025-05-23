import os
import xlsxwriter
import pandas as pd
import re
from openai import OpenAI # type: ignore


chose_model = "gpt-4o"


client = OpenAI(
    base_url='XXX',
    api_key='XXXX',
)

def get_content(text):
   
    pattern = r'(<START>.*?<END>)'
    result = re.findall(pattern, text, re.DOTALL)
    
   
    if result:
        return result
    else:
        
        return [text]

def get_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def create_prompt(data):
    prompt = f"""{data}

    Are there any configuration errors in the above configuration?

    Answer format (You MUST follow this):
    Detected errors are written between <START> and <END> tags.
    """
    return prompt

def constraint_method(data):
    
    
    prompt = create_prompt(data)
        
   
    response = client.chat.completions.create(
        model=chose_model,
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": prompt},
        ],

        temperature=0,
    )
        
    
    constraint_response = response.choices[0].message.content
    print(constraint_response)
    
    return get_content(constraint_response)

def main():

    data = []
    
    folder_path = 'XX' # EvaluationFile13.yaml, EvaluationFile16.yaml, TEST4, TEST14

  
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.yaml'):
            file_path = os.path.join(folder_path, file_name)
            print("------------------------------------")
            print(file_path)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            constraint_response = constraint_method(content)
            data = {
                'Model':chose_model,
                'Configuration':file_name, 
                'Final_responses':constraint_response
                }
            print(data)
            


if __name__ == "__main__":
    main()


