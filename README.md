# Shell Script Generator
The Shell Script Generator is a Python command-line tool that generates shell scripts using GPT language models. This tool was created by Maher to help overcome his inexperience with shell scripts and provide a quicker and more efficient way to create shell scripts without having to scour through pages of StackOverflow.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- You have installed Python 3.x on your local machine.
- You have access to an OpenAI API key.

## Setup
To set up the project, follow these steps:
```git clone https://github.com/MaherShahin/script_generator/```
```cd shell-script-generator```
```python3 -m venv venv```
```source venv/bin/activate```
```pip install -r requirements.txt```

Set up the .env file with your OpenAI API key:
OPENAI_API_KEY=your-api-key-here

## Usage
To run the chatbot, execute the main.py file:
python main.py

You should see the chatbot start up and prompt you for input. Enter a message and press Enter to receive a response from the GPT-3.5 Turbo model.

## prompts.json
The prompts.json file contains the prompts for the GPT language model. The templates in this file can be modified to suit the needs of the user. The file is structured as a dictionary with four keys, each representing a different type of prompt.

The first key, "clarification," contains a template that prompts the user to provide more details about a problem they are facing. It asks for information about the problem, the constraints, and the acceptance criteria.

The second key, "plan," contains a template that asks the user to provide three possible plans of action based on the problem, acceptance criteria, and constraints they have provided.

The third key, "generation," contains a template that asks the user to select one of the plans provided in response to the "plan" prompt.

The fourth key, "edit," contains a template that asks the user to edit a plan they have previously provided, along with feedback on the plan.

Users can modify the templates in this file to suit their specific needs. They can also add new keys to the file to create additional prompts. To use the modified prompts, the user should ensure that the "prompts.json" file is updated and located in the root directory of the project.

## Planner Class
The Planner class is responsible for generating a plan for the shell script based on the user input and preferences. The constructor takes two parameters, template_manager and gpt_client, which are used to load the prompts and communicate with the OpenAI API, respectively.

The execute_planning method generates a plan prompt by calling the create_plan_prompt method, which fills in the template with the user input and preferences. The plan prompt is then sent to the OpenAI API via the gpt_client object to generate suggested plans.

The choose_plan method allows the user to select one of the generated plans, request more plans, or edit a plan. If the user selects to edit a plan, the edit template is loaded and the user is prompted to enter feedback for the selected plan. The updated plan is then returned to be displayed to the user.

The display_plans method displays the generated plans to the user, and the create_plan_prompt method fills in the variables in the plan template with the user input and preferences to create the plan prompt.

This architecture allows for customization by enabling the developer to add or remove templates, change the variables in the templates, or change the logic in the choose_plan method to provide a different user experience.

## Basic Flow:

1. The user is prompted to describe their problem, acceptance criteria, and any constraints they have. This information is used to create a ScriptPlan object.
2. The Planner class generates a prompt for clarifying the user's input and sends it to the GPT-4 language model via the GPTClient class. The response is displayed to the user.
3. The user is prompted to provide any additional information or feedback.
4. The Planner class generates a plan for the shell script based on the user's input and feedback. The plans are displayed to the user.
5. The user selects a plan, and the Planner class generates a prompt for generating the shell script. The prompt includes the selected plan and any feedback the user provided.
6. The GPT-4 language model generates the shell script code based on the prompt.
7. The ShellScript class validates the generated code using the ScriptValidator class. If the code passes validation, it is saved to a file in the generated_scripts directory. If it fails validation, the user is prompted to select another plan or edit the existing plan.

# Uhhh, but why not just use the ChatGPT UI...?
The traditional chatbot UI can be frustrating and time-consuming for users, especially when dealing with complex tasks that require a lot of information and input. Deciding which piece of information is necessary and understanding what the model needs is not very clear. Therefore a planning level is introduced to allow the model itself to see which extra context or info is needed. Another planning level is there in order to flesh out the requirements by the user to have a better idea and generate more accurately the script needed.

Additionally, chatbot interfaces may not provide a structured way to gather input and organize it into a coherent plan. Users may need to manually extract and organize the information themselves, which can be time-consuming and prone to error. This can also lead to a lack of consistency across plans generated by different users, making it difficult to compare and evaluate the effectiveness of the generated plans.

By breaking the user input into structured levels and formalizing the planning process, the Shell Script Generator can improve the efficiency and accuracy of plan generation. The prompts.json file and template manager provide a clear and consistent structure for gathering input, while the planner and script_plan modules use this input to generate a detailed plan for the shell script. This structure helps ensure that all necessary information is collected and organized in a logical way, reducing the risk of errors and inconsistencies in the final output.

Overall, the Shell Script Generator provides a more efficient and user-friendly way to generate shell scripts using GPT language models. By formalizing the planning process and breaking the input into structured levels, the tool can improve the accuracy and consistency of the generated plans, while also reducing the frustration and time required for users to provide input.
