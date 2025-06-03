from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Setup SambaNova's OpenAI-compatible client
client = openai.OpenAI(
    api_key="90478a3c-f4bc-4665-8055-f11e951fbbfb",  # Replace with your actual key
    base_url="https://api.sambanova.ai/v1",
)

def get_recipe_from_sambanova(user_input):
    try:
        response = client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates detailed recipes from user-provided ingredients."},
                {"role": "user", "content": f"Generate a recipe using these ingredients: {user_input}"}
            ],
            temperature=0.3,
            top_p=0.9
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error from SambaNova API: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    ingredients_input = request.form.get('ingredients', '').strip().lower()
    if not ingredients_input:
        return render_template('result.html', ingredients="No ingredients provided.", recipe_name="", instructions=["Please enter some ingredients."])

    ai_recipe = get_recipe_from_sambanova(ingredients_input)

    return render_template('result.html',
                           ingredients=ingredients_input,
                           recipe_name="Generated Recipe",
                           instructions=[ai_recipe])

if __name__ == '__main__':
    app.run(debug=True)
