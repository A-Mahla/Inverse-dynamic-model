vlm_prompt = """
Analyze the image provided and describe the specific actions the user is performing within the software.
If NO software is on image or NO software action is found, generate ONLY: 'No software action found'
If a software action is found, your response should include:

1. The name of the software being used (with an accuracy percentage).
2. A detailed description of the specific features or tools being utilized within the software.
3. Any visible text or elements on the screen that can provide context.
4. What the user is likely doing based on past actions (e.g., if the user has typed text, they may be drafting a document).
5. Predictions about future actions based on the current activity (e.g., if the user is editing a document, they may save or print it next).
6. Any relevant context that helps understand the workflow (e.g., editing text, designing graphics, writing code).

Ensure the response does not exceed 150 words.
If the image shows NO signs of software use or if NO software-related actions are discernible, you must strictly respond with: 'No software action found.'

Ouptut:
"""

llm_prompt = """
Convert the following Visual Large Model (VLM) output into a JSON format.
Ensure the JSON includes all the relevant details provided by the VLM and follows a clear structure.
The JSON should have keys for 'software', 'accuracy', 'features_used', 'past_actions', 'future_actions'

Here is the structure for the JSON format:

```
{{
  annotation: {{
    "software": "Software name",
    "accuracy": "Percentage accuracy of software name found in decimal format (for example, 0.95) between 0 and 1",
    "features_used": "Description of features or tools used",
    "past_actions": "Description of past actions",
    "future_actions": "Predictions about future actions",
  }}
}}
```

Example Output:
VLM Output: 
"The user is using a writing software.
The user is currently utilizing the text formatting features, specifically changing the font size and style of selected text.
The visible text includes a title 'Project Plan'. Based on past actions of typing and formatting text, the user is likely drafting a document.
Future actions might include saving or printing the document."

JSON Format:
```
{{
  annotation: {{
    "software": "Microsoft Word",
    "accuracy": "0.85",
    "features_used": "Changing the font size and style of selected text",
    "past_actions": "Typing and formatting text",
    "future_actions": "Saving or printing the document"
  }}
}}
```

Example Output 2:
VLM Output: 
"The user is interacting with a photo editing software.
They are adjusting the contrast and brightness settings of an image.
The visible screen shows adjustments sliders and a photo of a sunset. Based on the past actions, the user is enhancing image colors.
Future actions may include applying filters or exporting the finished photo."

JSON Format:

{{
  "annotation": {{
    "software": "Adobe Photoshop",
    "accuracy": "0.90",
    "features_used": "Adjusting contrast and brightness",
    "past_actions": "Enhancing image colors",
    "future_actions": "Applying filters or exporting the photo"
  }}
}}

Example Output 3:
VLM Output: 
"The user appears to be using project management software.
The interface suggests task organization, with columns labeled 'To Do', 'Doing', and 'Done'.
Due to the low resolution and cluttered screen, the details are not fully clear. Past actions seem to involve moving cards between columns, indicating task progression.
Future actions might include updating task statuses or adding new tasks."

JSON Format:

{{
  "annotation": {{
    "software": "Trello",
    "accuracy": "0.68",
    "features_used": "Task organization with column-based layout",
    "past_actions": "Moving cards between columns",
    "future_actions": "Updating task statuses, adding new tasks"
  }}
}}


Example Output 4:
VLM Output: 
"The user is operating a database management software.
The screen shows SQL queries and database schemas but is partially obscured by other windows.
Past interactions with the software involve executing queries and examining data tables.
Predicted future actions include modifying database schemas or running further queries."

JSON Format:

{{
  "annotation": {{
    "software": "MySQL Workbench",
    "accuracy": "0.70",
    "features_used": "SQL queries and schema management",
    "past_actions": "Executing queries, examining data tables",
    "future_actions": "Modifying schemas, running more queries"
  }}
}}

Please convert the following VLM output to JSON."

VLM Output: {vlm_output}
"""
