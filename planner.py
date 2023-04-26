class Planner:
    def __init__(self, template_manager, gpt_client):
        self.template_manager = template_manager
        self.gpt_client = gpt_client

    def create_plan_prompt(self, script_plan, user_feedback):
        plan_template = self.template_manager.load_template("plan")
        if not plan_template:
            return None
        plan_prompt = plan_template.format(**{
            "problem": script_plan.problem,
            "acceptance_criteria": script_plan.acceptance_criteria,
            "constraints": script_plan.constraints,
            "user_feedback": user_feedback
        })
        return plan_prompt

    def execute_planning(self, script_plan, user_feedback):
        plan_prompt = self.create_plan_prompt(script_plan, user_feedback)
        if not plan_prompt:
            return None
        messages = [
            {"role": "system", "text": "You are a helpful assistant."},
            {"role": "user", "text": plan_prompt},
        ]
        plan_response = self.gpt_client.query_gpt(messages=messages)
        if not plan_response:
            return None
        plans = plan_response.split("\n")
        chosen_plan, choice = self.choose_plan(plans, plan_prompt)
        return chosen_plan, choice


    def display_plans(self, plans):
        print("\nGPT-4 suggested plans:")
        for i, plan in enumerate(plans):
            print(f"{i + 1}. {plan}")

    def choose_plan(self, plans, plan_prompt):
        while True:
            choice = input("Choose a plan (1-3), request 3 more plans (M), or edit a plan (E): ").lower()
            if choice in ["1", "2", "3"]:
                chosen_plan = plans[int(choice) - 1]
                return chosen_plan, choice
            elif choice == "m":
                plan_response = self.gpt_client.query_gpt(plan_prompt)
                if not plan_response:
                    print("Failed to generate more plans. Please try again.")
                    continue
                plans = plan_response.split("\n")
                self.display_plans(plans)
            elif choice == "e":
                plan_to_edit = int(input("Enter the plan number to edit (1-3): ")) - 1
                feedback = input("Provide feedback for the plan: ")
                edit_template = self.template_manager.load_template("edit")
                if not edit_template:
                    print("Failed to load the edit template.")
                    continue
                edit_prompt = edit_template.format(plan_prompt=plan_prompt, plan_number=plan_to_edit + 1, feedback=feedback)
                updated_plan = self.gpt_client.query_gpt(edit_prompt)
                if not updated_plan:
                    print("Failed to update the plan. Please try again.")
                    continue
                plans[plan_to_edit] = updated_plan
                self.display_plans(plans)
            else:
                print("Invalid input. Please try again.")
