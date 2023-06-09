from rich import print
from rich.panel import Panel

class Planner:
    def __init__(self,gpt_client, template_manager=None):
        self.template_manager = None
        self.gpt_client = gpt_client

    def create_plan_prompt(self, script_plan, user_feedback):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that helps users create shell scripts. Your goal is to understand the user's problem, their constraints, and acceptance criteria, and ask for more information if needed. Based on this information, you will generate a shell script that solves the problem. First, using the information provided by the user, you will decide what information or clarifying points the user needs to provide in order for you to most accurately solve his problem. Clear up any ambiguity so you don;t make any guesses"},
            {"role": "user", "content": f"I need a shell script to solve the following problem: {script_plan.problem}. The constraints are: {script_plan.constraints}. The acceptance criteria are: {script_plan.acceptance_criteria}."},
        ]
        
        return messages


    def execute_planning(self, script_plan, user_feedback, clarification_text):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that helps users create shell scripts. Your goal is to understand the user's problem, their constraints, and acceptance criteria, and ask for more information if needed."},
            {"role": "user", "content": f"I need a shell script to solve the following problem: {script_plan.problem}. The constraints are: {script_plan.constraints}. The acceptance criteria are: {script_plan.acceptance_criteria}."},
            {"role": "system", "content": clarification_text},
            {"role": "user", "content": user_feedback},
            {"role": "system", "content": "Now that I have all the information, please suggest 3 different plans to generate a shell script based on the problem, constraints, and acceptance criteria provided. Make sure that all plans fulfill the criteria and provide explanations in short comparing the pros and cons of each plan."},
        ]

        plan_response = self.gpt_client.query_gpt(messages=messages)
        if not plan_response:
            return None

        plans_text = plan_response["choices"][0]["message"]["content"]
        plans = plans_text.split("\n")
        return plans, messages


    def display_plans(self, plans):
        print("\n[bold]GPT-4 suggested plans:[/bold]")
        
        plan_number = 1
        plan_title = ""
        plan_content = []

        for line in plans:
            if 'Plan ' in line:
                if plan_title:  # Check if plan_title is not empty
                    panel = Panel(f"{plan_title}\n{''.join(plan_content)}", expand=False)
                    print(panel)
                    plan_title = ""
                    plan_content = []
                plan_title = f"Plan {plan_number}: {line.split(':')[1].strip()}"
                plan_number += 1
            elif line != '':
                plan_content.append(line + '\n')

        # Print the last plan
        if plan_title:
            panel = Panel(f"{plan_title}\n{''.join(plan_content)}", expand=False)
            print(panel)

    def choose_plan(self, plans, messages):
        while True:
            choice = input("Choose a plan (1-3), request 3 more plans (M), or edit a plan (E): ").lower()
            if choice in ["1", "2", "3"]:
                chosen_plan = int(choice)
                return chosen_plan, choice
            elif choice == "m":
                more_plans_request = [
                    *messages,
                    {"role": "system", "content": "Please suggest 3 additional plans for the user to consider."}
                ]
                more_plans_response = self.gpt_client.query_gpt(messages=more_plans_request)
                if not more_plans_response:
                    print("Failed to generate more plans. Please try again.")
                    continue
                more_plans_text = more_plans_response["choices"][0]["message"]["content"]
                plans = more_plans_text.split("\n")
                self.display_plans(plans)
            elif choice == "e":
                plan_to_edit = int(input("Enter the plan number to edit (1-3): "))
                feedback = input("Provide feedback for the plan: ")
                edit_request = [
                    *messages,
                    {"role": "system", "content": f"User feedback for plan {plan_to_edit }: {feedback}. Please modify the plan accordingly."},
                ]
                updated_plan_response = self.gpt_client.query_gpt(messages=edit_request)
                if not updated_plan_response:
                    print("Failed to update the plan. Please try again.")
                    continue
                updated_plan = updated_plan_response["choices"][0]["message"]["content"]
                plans[plan_to_edit] = updated_plan
                self.display_plans(plans)
            else:
                print("Invalid input. Please try again.")

    def generate_shell_script(self, choice, messages):
        generation_request = [
            *messages,
            {"role": "system", "content": f"User has chosen plan {choice}. Please generate a shell script based on the chosen plan. Generate a shell script that solves the problem, fulfills the constraints, and meets the acceptance criteria. Generate only shell code, dont provide any explanations but make sure your shell script is well commented."},
        ]
        shell_code_response = self.gpt_client.query_gpt(messages=generation_request)

        if not shell_code_response:
            print("Failed to generate the shell script.")
            return None

        shell_code = shell_code_response["choices"][0]["message"]["content"]
        return shell_code
