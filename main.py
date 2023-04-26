from gpt_client import GPTClient
from planner import Planner
from script_plan import ScriptPlan
from shell_script import ShellScript
from script_validator import ScriptValidator
from template_manager import TemplateManager
import os

def main():
    template_manager = TemplateManager()
    gpt_client = GPTClient()
    planner = Planner(template_manager, gpt_client)

    # Problem Initialization
    problem = input("Please describe your problem: ")
    acceptance_criteria = input("What is your acceptance criteria? ")
    constraints = input("Please provide any constraints you have: ")

    script_plan = ScriptPlan(problem, acceptance_criteria, constraints)
    
    # GPT Step 1 - Clarification by Model
    clarification_prompt = planner.create_plan_prompt(script_plan,None)
    clarification_response = gpt_client.query_gpt(clarification_prompt)
    clarification_text = clarification_response["choices"][0]["message"]["content"]

    if not clarification_response:
        return
    print("GPT-4: ", clarification_text)

    # User Feedback 
    user_feedback = input("Please provide any additional information or feedback: ")

    script_validator = ScriptValidator()

    # GPT Step 2 - Planning by Model
    plans, messages = planner.execute_planning(script_plan, user_feedback, clarification_text)
    if not plans:
        print("No initial plans were generated.")
        return

    planner.display_plans(plans)

    # Plan Selection
    chosen_plan, choice = planner.choose_plan(plans, messages)
    if not chosen_plan:
        print("No plan was chosen.")
        return

    # Shell Generation
    shell_code = planner.generate_shell_script( choice, messages)
    if not shell_code:
        print("Failed to generate the shell script.")
        return

    shell_script = ShellScript(shell_code)
    print(shell_script.code)
    # if script_validator.validate(shell_script.code):
    #     shell_script.sanitize()
    #     shell_script.save()
    #     print("\nThe shell script has been saved to generated_scripts/script.sh")

    # else:
    #     print("The generated shell script did not pass validation. Please try another plan or edit the existing one.")

if __name__ == "__main__":
    main()