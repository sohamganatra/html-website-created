# using composio with crewai to edit index.html and convert the structured information in the html file
from crewai import Agent, Task, Crew, Process
from langchain_anthropic import ChatAnthropic
from composio_crewai import ComposioToolSet, Action, App
import dotenv
import os

dotenv.load_dotenv()

# add OPENAI_API_KEY to env variables.
llm = ChatAnthropic(model_name="claude-3-5-sonnet-20240620", anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"))

def convert_structured_data_into_webpage(query):
    # get the structured data from the user
    # use crewai to edit the index.html file

    # Get All the tools
    composio_toolset = ComposioToolSet()
    exa_tools = composio_toolset.get_tools(apps=[App.EXA])
    file_tools = composio_toolset.get_tools(apps=[App.FILETOOL],actions=[Action.BROWSER_TOOL_GET_SCREENSHOT])

    search_agent = Agent(
        role="Search Agent",
        goal="Search online, gather information to create a humorous but professional critique of the term",
        backstory=(
            """You are a professional information gatherer. 
            The information you provide will be used to design a website that highlights the quirks and 
            peculiarities of the search term in a lighthearted, professional manner. Try to gather pros/cons or good/bad information, 
            gather from different angles and sources and provide all of this information in a nice fashion that could be used to create a website.
            Try to send information in structure format like here's all pros, here's all cons, here's long term impact, short term impact, etc.
            basically divide it in different categories and provide all the information in a nice fashion that could be used to create a website.
            The idea is to provide website designer with ideas on how to modify the website.
            """
        ),
        verbose=True,
        tools=exa_tools,
        llm=llm,
    )

    # Define agent
    web_editor_agent = Agent(
        role="Web Humor Editor",
        goal=f"Modify index.html to create a well-designed, humorous website based on the information provided",
        backstory=(
            """You are a professional AI agent specialized in web development with a talent for creating 
            entertaining content. Your task is to edit the index.html file to create a well-structured, 
            visually appealing website that humorously critiques the given search term. You are provided 
            with information to creatively design a website that highlights the quirks and peculiarities 
            of the search term in a lighthearted, professional manner.

            You have a live server running on top of index.html file at /Users/soham/hackathon/project/index.html
            Modify the /Users/soham/hackathon/project/index.html file to showcase the humorous critique in a 
            visually appealing and well-organized way. Use Tailwind CSS classes effectively to create a 
            responsive and attractive layout. You can edit the CSS in /Users/soham/hackathon/project/src/input.css 
            file if needed, but prioritize using Tailwind classes for styling.

            Incorporate relevant images, use appropriate and readable fonts, implement a pleasing color scheme, 
            and include design elements that contribute to the humor while maintaining a professional look. 
            Your goal is to create a website that's both informative in its critique and visually engaging, 
            perfectly balancing humor and good design principles.
            """
        ),
        verbose=True,
        tools=file_tools,
        llm=llm,
    )
    
    axis_task = Task(
        description=f"Identify 3-5 distinct axes or categories along which we can present information about the topic: {query}. These axes should provide a comprehensive and interesting perspective on the subject.",
        agent=search_agent,
        expected_output=f"A list of 3-5 axes or categories, each separated by a double line break.",
    )

    search_task = Task(
        description=f"Using the axes identified in the previous task, gather detailed information about {query}. For each axis, collect quirky facts, peculiarities, and interesting information that highlights both positive and negative aspects.",
        agent=search_agent,
        expected_output=f"Detailed information for each axis, separated by double line breaks. Each section should start with the axis name in bold. Pass on the links to the information you find along with the axis name.",
    )

    web_editor_task = Task(
        description="""Edit index.html to incorporate the provided information into a well-designed, comprehensive website based on the information provided. Ensure it's visually appealing, well-structured, and makes effective use of Tailwind CSS classes. Try to keep it pretty and professional. 
        You can add links to end pages to allow users to learn more about the topic by navigating to other websites. Try to organise the informatino along the axes provided.
        """,
        agent=web_editor_agent,
        expected_output="A professionally designed website with a comprehensive critique of the term. Include relevant images and appropriate fonts that enhance the humor while maintaining readability.",
    )

    my_crew = Crew(
        agents=[search_agent, web_editor_agent],
        tasks=[axis_task, search_task, web_editor_task],
        process=Process.sequential,
    )

    result = my_crew.kickoff()
    print(result)
