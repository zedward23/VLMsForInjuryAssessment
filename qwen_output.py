# Author: Luying Zhang
# Date: 11/06/2024
# Description: This is a script to call Qwen model and generate labels for each image.

# Refer to the document for workspace information: https://www.alibabacloud.com/help/en/model-studio/developer-reference/model-calling-in-sub-workspace    
import dashscope
from dashscope import MultiModalConversation
from create_dataset import label_class_human_value_list, dict_summary_sentences
import csv
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



def qwen_review(image, prompts):
    """
    Simple single round multimodal conversation call.
    """
    
    # Write the tokens into a csv file

    for prompt in prompts:
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": image},
                    {"text": prompt}
                ]
            }
        ]
        responses = MultiModalConversation.call(model='qwen-vl-max',
                                            messages=messages,
                                            stream=False)
            
        # print the last text response
        print(responses['output']['choices'][0]['message']['content'][0]['text'])

        input_tokens = responses["usage"]["input_tokens"]
        output_tokens = responses["usage"]["output_tokens"]
        image_tokens = responses["usage"]["image_tokens"] # 1230
        print("input_tokens: ", input_tokens, "output_tokens: ", output_tokens, "image_tokens: ", image_tokens)


def get_prompts():
    '''
    Get prompts from create_dataset.py
    '''
    label_class = ["trauma_head", "trauma_torso", "trauma_lower_ext", "trauma_upper_ext", "alertness_ocular", "severe_hemorrhage"]
    prompts = []
    for label in label_class:
        prompts.extend(label_class_human_value_list[label])
    for label in label_class:
        prompts.append(dict_summary_sentences[label])
    # print(len(prompts)) # 36
    return prompts

if __name__ == '__main__':
    image = "https://github.com/luyingz06/VLMsForInjuryAssessment/blob/main/images/1726253101436713875.png?raw=true"
    prompts = get_prompts()
    qwen_review(image, prompts)
    print(price('D:\\UPenn\\24Fall\\VLM\\VLMsForInjuryAssessment\\max_tokens.csv', 'qwen-vl-max'))