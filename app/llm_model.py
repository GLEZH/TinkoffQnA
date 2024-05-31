from langchain.llms import OpenAI


def generate_answer(question, system_prompt, sources):
    # Concatenate sources text
    context = " ".join([source.text for source in sources])
    prompt = f"{system_prompt}\n\nContext: {context}\n\nQuestion: {question}\nAnswer:"

    llm = OpenAI(model_name='gpt-4')  # Replace with actual model
    response = llm(prompt)

    return response
