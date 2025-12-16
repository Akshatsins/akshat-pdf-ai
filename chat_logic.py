import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

def ask_document(doc_text, user_question):
    """
    Sends the document text + user question to Groq and gets an answer.
    """
    
   
    llm = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0,
        api_key=os.environ.get("GROQ_API_KEY") 
    )
    
    
    system_prompt = """
    You are a helpful AI assistant.
    Answer the user's question strictly based on the provided text below.
    If the answer is not in the text, say "I cannot find that information in the document."
    
    DOCUMENT TEXT:
    {context}
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    
    chain = prompt | llm
    
    
    response = chain.invoke({
        "context": doc_text,
        "question": user_question
    })
    
    return response.content