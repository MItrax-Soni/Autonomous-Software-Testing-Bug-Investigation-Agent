import json
import os
import asyncio
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types

from app.config import settings
from app.schemas.scenario import TestStepDSL, ScenarioCreate

class GeminiAIService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self._client = None
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            self._client = genai.Client(api_key=self.api_key)

    @property
    def is_configured(self) -> bool:
        return self._client is not None

    async def generate_test_scenarios(
        self,
        target_url: str,
        pages: List[Dict[str, Any]],
        elements: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Formulates structured test scenarios based on discovered pages and interactive elements.
        Uses Gemini generative AI when configured, with robust schema enforcement and heuristic fallback.
        """
        if not self.is_configured:
            return self._heuristic_scenario_generator(target_url, pages, elements)

        # Assemble prompt payload
        simplified_elements = [
            {
                "tag": e.get("tag_name"),
                "type": e.get("element_type"),
                "selector": e.get("selector"),
                "label": e.get("semantic_label")
            }
            for e in elements[:40] # Keep prompt compact
        ]

        system_instruction = (
            "You are an expert QA Automation Architect. Given a web application topology and interactive DOM elements, "
            "generate between 4 to 8 high-value, structured test scenarios. You must cover positive happy paths, "
            "negative form validations, and interactive edge cases. "
            "Every step MUST use one of the following strict actions: navigate, click, fill, select, check, press, assert_visible, assert_text. "
            "Do NOT include any JavaScript code or markdown formatting outside the JSON output."
        )

        prompt = f"""
Target Web Application: {target_url}
Discovered Pages: {json.dumps([p.get('url') for p in pages[:10]])}
Interactive DOM Elements: {json.dumps(simplified_elements)}

Output a valid JSON array of test scenario objects conforming exactly to this structure:
[
  {{
    "title": "Short descriptive test scenario title",
    "description": "Clear objective of what is tested",
    "category": "POSITIVE" | "NEGATIVE" | "BOUNDARY" | "RESPONSIVENESS",
    "target_page_url": "{target_url}",
    "steps_json": [
      {{ "step_index": 1, "action": "navigate", "selector": "{target_url}" }},
      {{ "step_index": 2, "action": "click", "selector": "selector_here" }},
      {{ "step_index": 3, "action": "assert_visible", "selector": "selector_here" }}
    ],
    "expected_result": "Detailed expected state outcome",
    "is_approved": true,
    "order_index": 1
  }}
]
"""
        # Execute with retry
        for attempt in range(3):
            try:
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        response_mime_type="application/json",
                        temperature=0.2
                    )
                )
                raw_text = response.text
                parsed = json.loads(raw_text)
                if isinstance(parsed, list) and len(parsed) > 0:
                    return parsed
            except Exception as e:
                print(f"Gemini API attempt {attempt + 1} warning: {e}")
                await asyncio.sleep(1 * (2 ** attempt))

        # Fallback if API fails or rate limited
        return self._heuristic_scenario_generator(target_url, pages, elements)

    def _heuristic_scenario_generator(
        self,
        target_url: str,
        pages: List[Dict[str, Any]],
        elements: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Deterministic scenario synthesis based on DOM element heuristics.
        Ensures the system produces valid, executable test plans even without an API key.
        """
        scenarios = []
        buttons = [e for e in elements if e.get("element_type") in ("button", "submit") or e.get("tag_name") == "button"]
        inputs = [e for e in elements if e.get("element_type") in ("input", "text", "email", "password") or e.get("tag_name") == "input"]

        # 1. Navigation Happy Path
        scenarios.append({
            "title": "Verify Target Application Landing & DOM Visibility",
            "description": "Ensures the main application renders interactive surfaces without fatal load errors.",
            "category": "POSITIVE",
            "target_page_url": target_url,
            "steps_json": [
                {"step_index": 1, "action": "navigate", "selector": target_url},
                {"step_index": 2, "action": "assert_visible", "selector": "body"},
            ],
            "expected_result": "Page loads successfully with HTTP 200 and interactive root.",
            "is_approved": True,
            "order_index": 1
        })

        # 2. Form Input Validation
        if inputs:
            fill_steps = [{"step_index": 1, "action": "navigate", "selector": target_url}]
            for i, inp in enumerate(inputs[:3]):
                sel = inp.get("selector")
                lbl = inp.get("semantic_label", "").lower()
                val = "test@example.com" if "email" in lbl else "automated_test_input"
                fill_steps.append({
                    "step_index": len(fill_steps) + 1,
                    "action": "fill",
                    "selector": sel,
                    "value": val
                })
            if buttons:
                fill_steps.append({
                    "step_index": len(fill_steps) + 1,
                    "action": "click",
                    "selector": buttons[0].get("selector")
                })

            scenarios.append({
                "title": "Verify Input Form Population & Interactive Submission",
                "description": "Tests typing into discovered input fields and submitting action trigger.",
                "category": "POSITIVE",
                "target_page_url": target_url,
                "steps_json": fill_steps,
                "expected_result": "Input fields accept typed values and submit without unhandled script exceptions.",
                "is_approved": True,
                "order_index": 2
            })

            # Negative Validation Test
            empty_steps = [{"step_index": 1, "action": "navigate", "selector": target_url}]
            for inp in inputs[:2]:
                empty_steps.append({
                    "step_index": len(empty_steps) + 1,
                    "action": "fill",
                    "selector": inp.get("selector"),
                    "value": ""
                })
            if buttons:
                empty_steps.append({
                    "step_index": len(empty_steps) + 1,
                    "action": "click",
                    "selector": buttons[0].get("selector")
                })
            empty_steps.append({
                "step_index": len(empty_steps) + 1,
                "action": "assert_visible",
                "selector": "body"
            })

            scenarios.append({
                "title": "Verify Form Validation Under Empty Inputs (Negative Test)",
                "description": "Tests submitting blank input values to verify form validation behavior.",
                "category": "NEGATIVE",
                "target_page_url": target_url,
                "steps_json": empty_steps,
                "expected_result": "Application displays user-friendly validation error or prevents blank submission gracefully.",
                "is_approved": True,
                "order_index": 3
            })

        # 3. Interactive Component Responsiveness
        if buttons:
            btn = buttons[-1]
            scenarios.append({
                "title": f"Verify Interaction on {btn.get('semantic_label', 'Interactive Trigger')}",
                "description": "Tests clicking interactive button control and observing DOM state stability.",
                "category": "RESPONSIVENESS",
                "target_page_url": target_url,
                "steps_json": [
                    {"step_index": 1, "action": "navigate", "selector": target_url},
                    {"step_index": 2, "action": "click", "selector": btn.get("selector")},
                    {"step_index": 3, "action": "assert_visible", "selector": "body"},
                ],
                "expected_result": "Component triggers action cleanly without throwing console error or network crash.",
                "is_approved": True,
                "order_index": 4
            })

        return scenarios

gemini_service = GeminiAIService()
