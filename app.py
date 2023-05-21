from functools import partial
import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps as mongo_dumps
import asyncio
import openai

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["phone_call_summaries"]
collection = db["summaries"]

openai.api_key = os.environ.get('OPEN_API_KEY')

async def fetch_summary(model, transcript, prompt, is_internal):
    completion_prompt = prompt.format(transcript)
    prompt_type = "internal" if is_internal else "external"
    print(f"Starting fetch_summary for {prompt_type} prompt")
    result = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": completion_prompt}],
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7
    )
    print(f"Completed fetch_summary for {prompt_type} prompt: {prompt}")
    return result.choices[0].message.content

@app.route("/summaries", methods=["POST"])
async def create_summary():
    try:
        data = request.json
        call_transcript = data.get("transcript")

        internal_prompt = "Generate a summary for the following transcript, returning the following information, meant to be used as an internal summary for managers to read: names on the call if present, key points, dates, dollar size, roadblocks, and any other relevant information. Call transcript: {}"
        external_prompt = "Generate a summary for the following transcript, returning the following information, meant to be used as an external summary for customers to read: include first-person language, use the customer name if it exists, a personalized thank you message, and provide a summary of key points from the discussion, including any questions answered. Call transcript: {}"

        internal_summary_task = asyncio.create_task(fetch_summary("gpt-3.5-turbo", call_transcript, internal_prompt, True))
        external_summary_task = asyncio.create_task(fetch_summary("gpt-3.5-turbo", call_transcript, external_prompt, False))

        internal_summary, external_summary = await asyncio.gather(internal_summary_task, external_summary_task)

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
        app.logger.info(f"getting summary for {summary_id}")
        # Convert summary_id to ObjectId
        obj_id = ObjectId(summary_id)

        # Find the summary document with the given ID
        summary = collection.find_one({"_id": obj_id})
        summary["_id"] = str(summary["_id"])

        if summary:
            # Return the summary document as JSON response
            return jsonify(summary), 200
        else:
            return jsonify({"message": "Summary not found"}), 404

    except Exception as e:
        print(e)
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

