#================================#
# CS-391: Assignment 1
# Brendan Sting
# Kettering University
#================================#

from openai import OpenAI
import config as config

client = OpenAI(api_key=config.OPENAI_API_KEY)

# For GPT 3.5 Turbo, the endpoint is ChatCompletion
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_format={"type": "json_object"},
    # Conversation as a list of messages.
    messages=[
        {"role": "system", "content": "You will be provided a movie and your task is to create a news headline as a review for this movie, in the style of Siskel and Ebert. Then, Convert the user's query in a JSON object."},
        {
            "role": "user",
            "content": "Indiana Jones",
        },
        {
            "role": "assistant",
            "content": "Indiana Jones: The Movie That Had Me Rolling Through The Times",
        },
        {
            "role": "user", 
            "content": "A Star Is Born (1954)",
        },
        {
            "role": "assistant",
            "content":"A Star Is Born From 1954: The First Movie For Adults That I Really Liked",
        },
        {
            "role": "user",
            "content": "Bonnie and Clyde - 1967"
        },
        {
            "role": "assistant",
            "content":"Bonnie and Clyde From 1967: The First Great Movie I Ever Reviewed",
        },
        {
            "role": "user",
            "content": "My favorite movie is Dumbo"
        },
        {
            "role": "assistant",
            "content":"Dumbo: The Journey Of A Big-Eared Elephant",
        },
        {
            "role": "user",
            "content": "No, that is not right. The style of Siskel and Ebert is supposed to be sharp and witty. Please give a new headline for the film Dumbo. "
        },
        {
            "role": "assistant",
            "content":"Dumbo: The Movie That Made Me Hate Humans And Love Elephants",
        },
        {
            "role": "user",
            "content": "My favorite movie is Spiderman"
        },
    ]
)

print(response.choices[0].message.content)