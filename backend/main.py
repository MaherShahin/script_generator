from flask import Flask, request, jsonify

from backend.gpt.gpt_client import GPTClient
from backend.gpt.planner import Planner
from backend.models.shell_script_plan import ScriptPlan
from backend.models.shell_script import ShellScript
from backend.utils.shell_script_validator import ScriptValidator
from backend.gpt.shell_script_generator import ShellScriptGenerator

app = Flask(__name__)

gpt_client = GPTClient()
planner = Planner(gpt_client)
script_validator = ScriptValidator()
shell_script_generator = ShellScriptGenerator(gpt_client)


@app.route("/clarification", methods=["POST"])
def clarification():
    script_plan_data = request.json
    script_plan = ScriptPlan(script_plan_data["problem"], script_plan_data["acceptance_criteria"], script_plan_data["constraints"])
    clarification_text, messages = planner.create_plan_prompt(script_plan, None)
    return jsonify({"clarification_text": clarification_text, "messages": messages})


@app.route("/execute_planning", methods=["POST"])
def execute_planning():
    user_feedback = request.json["user_feedback"]
    clarification_text = request.json["clarification_text"]
    messages = request.json["messages"]
    plans, messages = planner.execute_planning(user_feedback, clarification_text, messages)
    displayed_plans = planner.get_displayed_plans(plans)
    return jsonify({"displayed_plans": displayed_plans, "messages": messages})


@app.route("/generate_shell_script", methods=["POST"])
def generate_shell_script():
    choice = request.json["choice"]
    messages = request.json["messages"]
    shell_code = shell_script_generator.generate_shell_script(choice, messages)
    return jsonify({"shell_code": shell_code})


@app.route("/validate_and_save", methods=["POST"])
def validate_and_save():
    shell_code = request.json["shell_code"]
    if script_validator.validate(shell_code):
        shell_script = ShellScript(shell_code)
        shell_script.sanitize()
        shell_script.save()
        return jsonify({"status": "success", "message": "The shell script has been saved to generated_scripts/script.sh"})
    else:
        return jsonify({"status": "error", "message": "The generated shell script did not pass validation. Please try another plan or edit the existing one."})


if __name__ == "__main__":
    app.run()
