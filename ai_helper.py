from openai import OpenAI 
client = OpenAI(api_key = ("")
def generate_study_plan(tasks):
    print(" AI FUNCTION CALLED") 

    if not tasks:
        return "No tasks available. Add some tasks."
    
    task_list = "\n".join([f"{task[1]+"-"+task[2]}" for task in tasks])
    
    print("TASK LIST:",task_list)
    
    prompt = f"Create a simple daily study plan for:\n{task_list}"

    try:
        response = client.Chat.Completions.create(
            model ="gpt-4o-mini",
            messages=[
                {"role":"user",
                 "content":prompt}
            ]
        )

        return response.choices[0].message.content
    
    except Exception as e:
        print("AI ERROR:",e)
        return "AI not working. Check API key."
    