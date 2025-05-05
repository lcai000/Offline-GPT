import ollama
import yaml

class Interact:
  def __init__(self):
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    self.model_name = config['model']
    self.agent_name = config['agent_name']
    self.task = config['agent_task']

  def call(self,content:str,verbose=False)->str:
      if verbose:
         response_type = "Long detailed explanation."
      else: 
         response_type = "Short and simple response."
      response = ollama.chat(model=self.model_name, messages=[
    {
      'role': 'user',
      'content': content+response_type,
    },
  ])
      return response['message']['content']

  def output(self,response:str)->str:
    return f'''
  {self.agent_name}------------------------------------------------------------\n\n
  {response}\n\n
  ------------------------------------------------------------{self.agent_name}\n\n
  '''

  def chat(self):
    print('conversation initialized, enter "q", "quit" to exit')
    while True:
        user_input = input('U: ')
        if user_input=='q' or user_input=='quit':
          break
        chat_output = self.call(content=user_input)
        res = self.output(response=chat_output)
        print(res)
        
if __name__=="__main__":
  agent = Interact()
  agent.chat()
