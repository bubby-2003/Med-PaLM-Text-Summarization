from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set the OpenAI API key
openai.api_key = "Your OPENAI API KEY"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text', '')
    length = data.get('length', 'medium')
    specialty = data.get('specialty', '').strip()
    style = data.get('style', 'conversational')

    if not text:
        return jsonify({"error": "Empty text"}), 400

    # Trim text for short summaries
    if length == 'short' and len(text.split()) > 100:
        text = " ".join(text.split()[:100]) + "..."

    # Build the prompt with specialty handling
    if specialty:
        prompt = f"Summarize this {specialty} medical information: {text}"
    else:
        prompt = f"Summarize this medical information: {text}"
    
    if style == 'conversational':
        prompt += " Summarize in simple, conversational language."
    elif style == 'technical':
        prompt += " Summarize using technical language."

    # Define max_tokens based on length
    if length == 'short':
        max_tokens = 100  # Increased token limit for short summaries
    elif length == 'medium':
        max_tokens = 150
    else:
        max_tokens = 300

    try:
        # Request to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7  # Adjust temperature for creativity
        )
        # Extract summary
        raw_summary = response.choices[0].message['content'].strip()

        # Post-process to ensure complete sentences within the required range
        sentences = raw_summary.split(". ")
        final_summary = ""
        total_tokens = 0
        token_limit = max_tokens // 4  # Approximate word count based on token count

        for sentence in sentences:
            sentence_token_count = len(sentence.split())
            if total_tokens + sentence_token_count <= token_limit:
                final_summary += sentence.strip() + ". "
                total_tokens += sentence_token_count
            else:
                break

        final_summary = final_summary.strip()

        return jsonify({"summary": final_summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
