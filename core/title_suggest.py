import openai

openai.api_key = "your_openai_api_key"

def suggest_titles(content):
    prompt = f"Suggest 3 creative blog post titles for the following content:\n\n{content}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    titles = response.choices[0].message["content"].split("\n")
    return [title.strip("-• ") for title in titles if title.strip()]
