import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import openai
import logging

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["phone_call_summaries"]
collection = db["summaries"]

openai.api_key = os.environ.get('OPEN_API_KEY')

@app.route("/summaries", methods=["POST"])
def create_summary():
    try:
        data = request.json
        call_transcript = data.get("transcript")

        # Define the prompt for generating the combined summary
        prompt = f"Generate two summaries for the following transcript and separate them into internal and external sections using ###SEPARATE### between the two sections. The internal summary should include the names on the call if present, key points, dates, dollar size, roadblocks, and any other relevant information. The external summary should include first-person language, use the customer name if it exists, a personalized thank you message, and provide a summary of key points from the discussion, including any questions answered. Outline the next steps and conclude with a final thank you.\n\n{call_transcript}"

        # Generate the combined summary using OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7,
            n=1,
            stop=None,
        )

        summary = response.choices[0].text.strip()

        # Find the starting index of the internal and external summaries
        start_internal_summary = summary.find("Internal Summary:") + len("Internal Summary:")
        start_external_summary = summary.find("External Summary:") + len("External Summary:")

        # Extract the internal and external summaries
        internal_summary = summary[start_internal_summary: start_external_summary].strip().replace('\n', '')
        external_summary = summary[start_external_summary:].strip().replace('\n', '')

        # Print or use the internal and external summaries as needed
        print("Internal Summary:")
        print(internal_summary)
        print("\nExternal Summary:")
        print(external_summary)

        # Save the summaries in the database or perform any other desired actions
        summary_data = {
            "internal_summary": internal_summary,
            "external_summary": external_summary
        }
        result = collection.insert_one(summary_data)
        summary_id = str(result.inserted_id)

        return jsonify({"message": "Summary created successfully", "id": summary_id}), 201

    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@app.route("/summaries/<summary_id>", methods=["GET"])
def get_summary(summary_id):
    try:
        # Convert summary_id to ObjectId
        obj_id = ObjectId(summary_id)

        # Find the summary document with the given ID
        summary = collection.find_one({"_id": obj_id}, {"_id": 0})

        if summary:
            # Return the summary document as JSON response
            return jsonify(summary), 200
        else:
            return jsonify({"message": "Summary not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error retrieving summary", "error": str(e)}), 500

@app.route("/summaries/<summary_id>", methods=["DELETE"])
def delete_summary(summary_id):
    try:
        # Convert summary_id to ObjectId
        obj_id = ObjectId(summary_id)

        # Delete the document using the converted ObjectId
        result = collection.delete_one({"_id": obj_id})

        if result.deleted_count == 1:
            return jsonify({"message": "Summary deleted successfully"}), 200
        else:
            return jsonify({"message": "Summary not found"}), 404

    except Exception as e:
        return jsonify({"message": "Error deleting summary", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)