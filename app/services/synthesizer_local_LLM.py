from typing import List
import pandas as pd
from pydantic import BaseModel, Field
import requests
import logging

class SynthesizedResponse(BaseModel):
    thought_process: List[str] = Field(
        description="List of thoughts that the AI assistant had while synthesizing the answer"
    )
    answer: str = Field(description="The synthesized answer to the user's question")
    enough_context: bool = Field(
        description="Whether the assistant has enough context to answer the question"
    )


class Synthesizer:
    SYSTEM_PROMPT = """
    # Role and Purpose
    You are an AI assistant for an e-commerce FAQ system. Your task is to synthesize a coherent and helpful answer 
    based on the given question and relevant context retrieved from a knowledge database.

    # Guidelines:
    1. Provide a clear and concise answer to the question.
    2. Use only the information from the relevant context to support your answer.
    3. The context is retrieved based on cosine similarity, so some information might be missing or irrelevant.
    4. Be transparent when there is insufficient information to fully answer the question.
    5. Do not make up or infer information not present in the provided context.
    6. If you cannot answer the question based on the given context, clearly state that.
    7. Maintain a helpful and professional tone appropriate for customer service.
    8. Adhere strictly to company guidelines and policies by using only the provided knowledge base.
    
    Review the question from the user:
    """

    @staticmethod
    def generate_response(question: str, context: pd.DataFrame) -> SynthesizedResponse:
        """Generates a synthesized response based on the question and context.

        Args:
            question: The user's question.
            context: The relevant context retrieved from the knowledge base.

        Returns:
            A SynthesizedResponse containing thought process and answer.
        """
        api_url = "http://localhost:1234/v1/chat/completions" 

        context_messages = [
            {"role": "assistant", "content": row["content"]}
            for _, row in context.iterrows()
        ]

        payload = {
            "model": "deepseek-r1-distill-qwen-7b",
            "messages": [
                {"role": "system", "content": "Could you please help me answer my question"},
                {"role": "user", "content": question},
                *context_messages
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }

        response = requests.post(api_url, json=payload)
        return SynthesizedResponse(
            answer=response.json()["choices"][0]["message"]["content"],
            thought_process=["a", "b"],
            enough_context=True
        )



    @staticmethod
    def dataframe_to_json(
        context: pd.DataFrame,
        columns_to_keep: List[str],
    ) -> str:
        """
        Convert the context DataFrame to a JSON string.

        Args:
            context (pd.DataFrame): The context DataFrame.
            columns_to_keep (List[str]): The columns to include in the output.

        Returns:
            str: A JSON string representation of the selected columns.
        """
        return context[columns_to_keep].to_json(orient="records", indent=2)
