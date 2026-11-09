from langchain_core.messages import HumanMessage
from utils.llm_factory import get_llm

class CoordinatorAgent:
    def __init__(self):
        self.llm = get_llm()

    def decide_agents(self, contract_text):
        prompt = f"""
        Contract:
        {contract_text}
        """

        response = self.llm.invoke(
            [HumanMessage(content=prompt)]
        )
        return response.content
