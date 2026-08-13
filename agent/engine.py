from dotenv import load_dotenv
load_dotenv()
import os
import io
import contextlib
import pandas as pd
from groq import Groq

class DataQAAgent:
    def __init__(self, csv_path: str, api_key: str = None):
        if not os.path.exists(csv_path):
            raise FileNotFoundError("CSV file not found at: " + str(csv_path))
            
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        
        key = api_key or os.getenv("GROQ_API_KEY")
        if not key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        self.client = Groq(api_key=key)
        self.model = "llama-3.3-70b-versatile"

    def _get_schema_summary(self) -> str:
        buf = io.StringIO()
        self.df.info(buf=buf)
        head_sample = self.df.head(3).to_markdown()
        return "Schema:\n" + buf.getvalue() + "\n\nSample Data (First 3 rows):\n" + head_sample

    def _generate_code(self, question: str) -> str:
        schema_info = self._get_schema_summary()
        system_prompt = (
            "You are a strict, specialized Data Science Assistant designed exclusively to answer questions about a loaded CSV dataset.\n\n"
            "Dataset File Path: " + self.csv_path + "\n"
            "The DataFrame is pre-loaded into a variable named `df`.\n\n"
            + schema_info + "\n\n"
            "RULES:\n"
            "1. **Scope Check:** Evaluate if the user's question can be answered using the columns and data available in this dataset. If the question is completely unrelated (e.g., general knowledge, coding help, weather, random trivia, personal questions), DO NOT write pandas code. Instead, set `result = 'OUT_OF_SCOPE'`.\n"
            "2. Generate valid, executable Python pandas code using the pre-loaded DataFrame `df` only if the question is relevant to the dataset.\n"
            "3. Store your final numerical, string, or tabular answer in a variable named `result`.\n"
            "4. Put ONLY the executable Python code inside markdown block: ```python <code here> ```.\n"
            "5. Do NOT include markdown comments or markdown explanation outside the code block."
        )
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Question: " + question}
            ],
            temperature=0.0
        )
        
        raw_output = response.choices[0].message.content
        if "```python" in raw_output:
            code = raw_output.split("```python")[1].split("```")[0].strip()
        elif "```" in raw_output:
            code = raw_output.split("```")[1].split("```")[0].strip()
        else:
            code = raw_output.strip()
            
        return code

    def _execute_code(self, code: str) -> dict:
        local_vars = {"df": self.df.copy(), "pd": pd}
        stdout_capture = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(stdout_capture):
                exec(code, {}, local_vars)
            
            computed_result = local_vars.get("result", stdout_capture.getvalue())
            return {"success": True, "result": computed_result, "error": None}
        except Exception as e:
            return {"success": False, "result": None, "error": str(e)}

    def ask(self, question: str) -> dict:
        code = self._generate_code(question)
        execution = self._execute_code(code)
        
        if not execution["success"]:
            return {
                "question": question,
                "code": code,
                "raw_result": None,
                "answer": "⚠️ Execution Error: " + str(execution['error'])
            }

        synthesis_prompt = (
            "You are a helpful Data Analyst. Present the final answer to the user clearly using the exact mathematical result provided.\n\n"
            "User Question: " + question + "\n"
            "Executed Code:\n```python\n" + code + "\n```\n"
            "Computed Result:\n" + str(execution['result']) + "\n\n"
            "Instructions:\n"
            "- Provide a clear direct answer in 1-3 sentences.\n"
            "- Cite the exact calculated numbers/table from the computed result.\n"
            "- Do NOT guess or alter any computed numbers."
        )
        
        synthesis = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": synthesis_prompt}],
            temperature=0.2
        )

        return {
            "question": question,
            "code": code,
            "raw_result": str(execution['result']),
            "answer": synthesis.choices[0].message.content
        }