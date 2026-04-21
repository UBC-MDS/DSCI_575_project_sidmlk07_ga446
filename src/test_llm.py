from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOllama(model="llama3.2", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful Amazon shopping assistant. You must answer using ONLY the information in the context.

- If the answer is present, summarize it clearly based on the product reviews.
- Do NOT say "I don't know" if the answer exists in the context.
- Only say "I don't know" if the context truly does not contain the answer.

Context:
{context}

Question:
{input}

Answer:
"""
)


def test_llm_generation(user_question: str, dummy_context: str):
    """
    Generates and returns an LLM response using a predefined
    LangChain pipeline given a question and dummy context.
    """
    chain = prompt | llm | StrOutputParser()

    response = chain.invoke({"context": dummy_context, "input": user_question})

    return response


if __name__ == "__main__":
    test_context = "Product: XYZ Moisturizer. Reviews mention it is great for sensitive skin but very expensive."
    test_question = "Is the XYZ moisturizer good for sensitive skin?"

    print("Thinking...\n")
    print(test_llm_generation(test_question, test_context))
