from flask import Flask, jsonify
from routes import create_summary, get_summary, delete_summary

app = Flask(__name__)

# TODO Add typing throughout app
# This file defines Flask routes. The functions called are defined in seperate modules to promote better code organization and maintainability (this applies throughout app).
# Note: Ensure proper configuration of the MongoDB connection and OpenAI API key for correct API functionality when you want to run this.

@app.route("/summaries", methods=["POST"])
async def create_summary_route():
    try:
        return await create_summary(app)
    except Exception as e:
        error_message = str(e)
        return jsonify({"message": "An error occurred", "error": error_message}), 500

@app.route("/summaries/<summary_id>", methods=["GET"])
def get_summary_route(summary_id):
    try:
        return get_summary(app, summary_id)
    except Exception as e:
        error_message = str(e)
        return jsonify({"message": "An error occurred", "error": error_message}), 500

@app.route("/summaries/<summary_id>", methods=["DELETE"])
def delete_summary_route(summary_id):
    try:
        return delete_summary(app, summary_id)
    except Exception as e:
        error_message = str(e)
        return jsonify({"message": "An error occurred", "error": error_message}), 500

if __name__ == "__main__":
    app.run()