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

    problem = input("Please describe your problem: ")
    acceptance_criteria = input("What is your acceptance criteria? ")
    constraints = input("Please provide any constraints you have: ")

    script_plan = ScriptPlan(problem, acceptance_criteria, constraints)

    clarification_template = template_manager.load_template("clarification")
    clarification_prompt = clarification_template.format(problem=script_plan.problem, acceptance_criteria=script_plan.acceptance_criteria, constraints=script_plan.constraints)
    clarification_response = gpt_client.query_gpt(clarification_prompt)
    if not clarification_response:
        return
    print("GPT-4: ", clarification_response)

    user_feedback = input("Please provide any additional information or feedback: ")

    script_validator = ScriptValidator()

    initial_plans, plan_prompt = planner.execute_planning(script_plan, user_feedback)
    if not initial_plans:
        print("No initial plans were generated.")
        return

    plans = initial_plans.split("\n")
    planner.display_plans(plans)

    chosen_plan, choice = planner.choose_plan(plans, plan_prompt)
    if not chosen_plan:
        print("No plan was chosen.")
        return

    generation_template = template_manager.load_template("generation")
    if not generation_template:
        print("Failed to load the generation template.")
        return
    generation_prompt = generation_template.format(plan_prompt=plan_prompt, choice=choice)
    shell_code = gpt_client.query_gpt(generation_prompt)
    if not shell_code:
        print("Failed to generate the shell script.")
        return

    shell_script = ShellScript(shell_code)

    if script_validator.validate(shell_script.code):
        shell_script.sanitize()
        shell_script.save()
        print("\nThe shell script has been saved to generated_scripts/script.sh")

    else:
        print("The generated shell script did not pass validation. Please try another plan or edit the existing one.")

if __name__ == "__main__":
    main()