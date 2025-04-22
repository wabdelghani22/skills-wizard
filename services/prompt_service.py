class PromptService:
    def __init__(self):
        pass

    def get_prompt_template(self, code: str) -> str:
        from db import crud
        return crud.get_prompt_by_code(code)

    def render_prompt(self, template: str, context: dict) -> str:
        from jinja2 import Template
        return Template(template).render(**context)
