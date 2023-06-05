from chatGPTMidJourneyPrompt.mjPrompt import PromptGenerator

# supported authorization methods: via email and password, via token, via api key
config = {
  "email": "your_email",
  "password": "your_password",
  # or
  "session_token": "your_session_token",
  # or
  "api_key": "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",
}

promptGenerator = PromptGenerator(config)

# prompt = promptGenerator.V4("早晨，一位老人坐在河边钓鱼，周围环境是绿水青山")
# print(prompt)
# prompt = promptGenerator.V4("any text")
# prompt = promptGenerator.niji("any text")
# prompt = promptGenerator.testp("any text")

# or advanced usage if needed
promptConfig = {
"model": "artistic",
"type": "avatar",
#"renderer": "octane",
#"content": "landscape",
#"aspect_ratio": "9:16",
#"color": "red",
"url": "example image url",
}

prompt = promptGenerator.V5("早晨，一位老人坐在河边钓鱼，周围环境是绿水青山", config=promptConfig, words=50)
print(prompt)