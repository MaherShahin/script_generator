from gpt_client import GPTClient
from planner import Planner
from script_plan import ScriptPlan
from shell_script import ShellScript
from script_validator import ScriptValidator

from rich.console import Console
from rich.prompt import Prompt

console = Console()

def main():

    gpt_client = GPTClient()
    planner = Planner(gpt_client)

    # Problem Initialization
    problem = Prompt.ask("Please describe your problem: ")
    acceptance_criteria = Prompt.ask("What is your acceptance criteria? ")
    constraints = Prompt.ask("Please provide any constraints you have: ")

    script_plan = ScriptPlan(problem, acceptance_criteria, constraints)
    
    # GPT Step 1 - Clarification by Model
    clarification_prompt = planner.create_plan_prompt(script_plan,None)
    clarification_response = gpt_client.query_gpt(clarification_prompt)
    clarification_text = clarification_response["choices"][0]["message"]["content"]

    if not clarification_response:
        return
    console.print("[cyan]GPT-4:[/cyan] ", clarification_text)

    # User Feedback 
    user_feedback = Prompt.ask("Please provide any additional information or feedback: ")

    script_validator = ScriptValidator()

    # GPT Step 2 - Planning by Model
    plans, messages = planner.execute_planning(script_plan, user_feedback, clarification_text)
    if not plans:
        console.print("No initial plans were generated.", style="bold red")
        return

    planner.display_plans(plans)

    # Plan Selection
    chosen_plan, choice = planner.choose_plan(plans, messages)
    if not chosen_plan:
        console.print("No plan was chosen.", style="bold red")
        return

    # Shell Generation
    shell_code = planner.generate_shell_script(choice, messages)
    if not shell_code:
        console.print("Failed to generate the shell script.", style="bold red")
        return

    shell_script = ShellScript(shell_code)
    console.print(shell_script.code)
    
    if script_validator.validate(shell_script.code):
        shell_script.sanitize()
        shell_script.save()
        console.print("\nThe shell script has been saved to generated_scripts/script.sh", style="bold green")

    else:
        console.print("The generated shell script did not pass validation. Please try another plan or edit the existing one.", style="bold red")

if __name__ == "__main__":
    main()
