import json
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import save_tool, AquilaTool
from flask import Flask,render_template,redirect,url_for,request,jsonify
import random
import string
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from flask_cors import CORS
from langchain.memory import ConversationBufferWindowMemory
import os
# Initialize memory with window of 6 exchanges
memory = ConversationBufferWindowMemory(k=6, return_messages=True, memory_key="chat_history")

lo=[]
# Load from cache (no more download)
app=Flask(__name__,template_folder='Templates')
CORS(app, origins="*")

def load_memory():
    if os.path.exists("chat_history.json"):
        try:
            with open("chat_history.json", "r", encoding="utf-8") as f:
                history = json.load(f)
            memory.clear()
            for msg in history:
                if msg['role'] == 'user':
                    memory.chat_memory.add_message(HumanMessage(content=msg['content']))
                elif msg['role'] == 'assistant':
                    memory.chat_memory.add_message(AIMessage(content=msg['content']))
            print(f"Loaded {len(history)//2} conversation turns")
        except Exception as e:
            print(f"Error loading memory: {e}")
            memory.clear()

def save_memory():
    try:
        history = []
        for msg in memory.chat_memory.messages:
            role = 'user' if isinstance(msg, HumanMessage) else 'assistant'
            history.append({"role": role, "content": msg.content})
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving memory: {e}")

load_memory()
email1=[]
email2=[]
import string
@app.route("/",methods=["POST","GET"])
def IsraelGPT():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            user=data.get('user1')
        else:
            # Handle form submission
            user = request.form.get("user1")
            email = request.form.get("email", "")
        class ResearchResponse(BaseModel):
                topic: str
                summary: str
                output: str
                sources: list[str]
                tools_used: list[str]
            # openai.api_key=token
        llm= ChatOpenAI(model="gpt-4o-mini",
        api_key=os.getenv('APILLM'),
        temperature=0.7
        )
        # llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
        # parser = PydanticOutputParser(pydantic_object=ResearchResponse)
        # print(completion.choices[0].message)
        # messages=[
        #         SystemMessage(content="You are a helpful assistant."),
        #         HumanMessage(content=user)
        # ]
        parser = PydanticOutputParser(pydantic_object=ResearchResponse)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are a research assistant that will help generate a research paper.  if the user greets, make sure to greet them in your output.
                    Answer according to Carfax-education's official website.
                    You must always use the provided tool to answer questions about Carfax-education website. If the tool returns no relevant data, say 'sorry, no relevant data found'.
                    bear in mind that , 
                    try to answer in 
                    a convincing way. if there is no relevant
                    data, just simply say 'sorry, no relevant data found'.
                    Wrap the output in this format and provide no other text\n{format_instructions},
                    """,
                
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{query}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        ).partial(format_instructions=parser.get_format_instructions())

        tools = [AquilaTool()]
        
        # Create an instance of the wrapper
        agent = create_tool_calling_agent(
            llm=llm,
            prompt=prompt,
            tools=tools
        )
        agent_executor = AgentExecutor(agent=agent, tools=tools,verbose=True)
        query = str(user) + f"only search Carfax-education's official website"
        print(user)

        memory.chat_memory.add_message(HumanMessage(content=user))

        chat_history_msgs = memory.load_memory_variables({})["chat_history"]
        raw_response = agent_executor.invoke({
            "query": query,
            "chat_history": chat_history_msgs
        })
        print(raw_response['output'])
        structured_response = raw_response['output']
        print(structured_response)
    # except:
    #        return redirect(url_for("free"))
                    # return completion.choices[0].message.content

        memory.chat_memory.add_message(AIMessage(content=structured_response))
        save_memory()
    # j=str(structured_response).find("sources")
    # k=str(structured_response).find("summary")
    # v=str(structured_response).find("tools_used")
    # b=structured_response
    # Return proper JSON response for AJAX requests
    # if request.is_json:
        
        try:
                if 'no relevant data ' in str(structured_response):
                        return jsonify({"output": """you can contact:
                                        +98 919 527 2398"""})
                else:
                    f=str(structured_response).find('output')
                    v1=str(structured_response).find('summary')
                    f1=str(structured_response).find('sources')
                    # m=str(structured_response)[v:f].replace('summary','')
                    # nm=str(structured_response)[f:f1].replace('output','') 
                    # n=str(m).replace('output','')
                    # print(n)
                    # mb=n.replace(':','')
                    # b=str(nm)+str(m)
                    print(str(structured_response[f:f1]))
                    print(structured_response)
                    return jsonify({
                        'output': f'{str(structured_response[v1+8:f1]).replace('"output": "','')}'
                    })
        except:
                print(structured_response)
                return f'{structured_response[f:]},{render_template("button.html", content=jsonify(structured_response[f:]))}'
        
    
        # else:
                # Return HTML for form submissions
            
    
    # except Exception as e:
    #     if request.is_json:
    #         return f'{jsonify({"error": "Error parsing response", "details": str(e)}), 500}'
    #     else:
        #         return "Error parsing response", e, "Raw Response - ", raw_response
    return render_template("button.html")

if __name__ == '__main__':
    app.run(debug=True)
