from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Setup SambaNova's OpenAI-compatible client
client = openai.OpenAI(
    api_key = "0e690b14-a239-4027-82a8-00cbf8d79e4e",
    # api_key="90478a3c-f4bc-4665-8055-f11e951fbbfb",
    base_url="https://api.sambanova.ai/v1",
)


def generate_full_recipe_info(user_input):
    try:
        variations = []

        for i in range(3):
            # Generate recipe
            recipe_response = client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct",
                messages=[
                    {"role": "system", "content": "You are a professional creative chef AI."},
                    {"role": "user", "content": f"Create a unique recipe using: {user_input}. Include the dish name and numbered instructions."}
                ],
                temperature=0.6,
                top_p=0.9
            )
            print(recipe_response)
            if recipe_response and recipe_response.choices:
                recipe_text = recipe_response.choices[0].message.content
            else:
                recipe_text = "Could not generate recipe."

            # Nutritional facts
            nutrition_response = client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct",
                messages=[
                    {"role": "system", "content": "You are a certified nutritionist AI."},
                    {"role": "user", "content": f"Estimate calories, protein, fat, and carbs for this dish: {recipe_text}"}
                ],
                temperature=0.3
            )
            print(nutrition_response)
            if nutrition_response and nutrition_response.choices:
                nutrition_text = nutrition_response.choices[0].message.content
            else:
                nutrition_text = "Could not generate nutritional facts."

            # Time & difficulty estimate
            time_diff_response = client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct",
                messages=[
                    {"role": "system", "content": "You are a culinary expert AI."},
                    {"role": "user", "content": f"Estimate the total cooking time and difficulty level (easy, medium, hard) for this recipe: {recipe_text}"}
                ],
                temperature=0.3
            )
            print(time_diff_response)
            if time_diff_response and time_diff_response.choices:
                time_diff_text = time_diff_response.choices[0].message.content
            else:
                time_diff_text = "Could not estimate time and difficulty."

            # Combine all info
            full_recipe = f"Recipe Variation {i+1}:\n\n{recipe_text}\n\n Nutritional Facts:\n{nutrition_text}\n\n  Time & Difficulty:\n{time_diff_text}"
            variations.append(full_recipe)

        return variations

    except Exception as e:
        return [f"Error from SambaNova API: {e}"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    ingredients_input = request.form.get('ingredients', '').strip().lower()

    if not ingredients_input:
        return render_template('result.html',
                                ingredients="No ingredients provided.",
                                recipe_name="",
                                instructions=["Please enter some ingredients."])

    ai_recipes = generate_full_recipe_info(ingredients_input)

    return render_template('result.html',
                            ingredients=ingredients_input,
                            recipe_name="Generated Recipes with Nutrition & Cooking Info",
                            instructions=ai_recipes)

if __name__ == '__main__':
    app.run(debug=True)
