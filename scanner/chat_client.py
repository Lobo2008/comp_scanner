from openai import OpenAI
import base64

class ChatClient:
    def __init__(self, api_key, api_url, model="step-1v-8k", max_tokens=1024, 
                 temperature=0.3, top_p=0.9, frequency_penalty=0.05):
        self.client = OpenAI(
            api_key=api_key,
            base_url=api_url,
        )
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.messages = []
        self.system_prompts = {
            "therapist": "你是一个专业心理师",
            "programmer": "你是一个专业程序员",
            "nutritionist": "你是一个专业的营养师，擅长分析食物成分和营养价值",
            # Add more system prompts as needed
        }
        
    def chat_one_turn(self, prompt_key, user_message_dict):
        # Initialize with system message if starting new conversation
        if not self.messages:
            self.messages.append({
                "role": "system",
                "content": self.system_prompts[prompt_key]
            })
        
        # Handle message with image
        if "image" in user_message_dict:
            # Format message with image in base64
            content = [
                {
                    "type": "text",
                    "text": user_message_dict["content"]
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{user_message_dict['image']}"
                    }
                }
            ]
        else:
            # Regular text-only message
            content = [
                {
                    "type": "text",
                    "text": user_message_dict["content"]
                }
            ]
        
        # Add user message to history
        self.messages.append({
            "role": "user",
            "content": content
        })
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            stop=[],
            stream=False,
            tools=[]
        )
        return response
    
    def add_assistant_message(self, message):
        """Add assistant's response to message history"""
        self.messages.append({
            "role": "assistant",
            "content": message
        })
    
    def clear_history(self):
        """Clear conversation history"""
        self.messages = []
    
    def get_content(self, response):
        """Parse and return just the assistant's message content
        
        Args:
            response: The raw API response object
        
        Returns:
            str: The assistant's message content
        """
        return response.dict()["choices"][0]["message"]["content"]

# Usage example:
if __name__ == "__main__":
    chat_client = ChatClient(
        api_key="",
        api_url="https://api.stepfun.com/v1"
    )
    
    img_path="assets/demo/cola.jpeg"
    img_path="/Users/lobo/Downloads/potatochips.jpg"
    with open(img_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    

    user_message = {
        "content": "请你描述一下图中东西的配料表",
        "image": image_base64
    }
    
    response = chat_client.chat_one_turn("nutritionist", user_message)
    response_content = chat_client.get_content(response)
    print(response_content)
    
    # # Add assistant's response to history
    # chat_client.add_assistant_message(response)
    
