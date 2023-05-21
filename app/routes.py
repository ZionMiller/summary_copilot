from flask import jsonify, request
from bson.objectid import ObjectId
from bson.errors import InvalidId
from mongodb import collection
from helpers import fetch_summary
import asyncio

# Aysnc func responsible for creating summaries based on a given call transcript in a concurrent manor.
# retrieves and validates json, defines internal & external prompts, provides logs, creates tasks to assist with async
# We insert this into our MongoDB collection and log an ID to make it easier to fetch
async def create_summary(app):
    try:
        data = request.json
        call_transcript = data.get("transcript")

        if call_transcript is None or call_transcript.strip() == "":
            return jsonify({"message": "Transcript can't be empty, please add your transcript in"}), 400

        internal_prompt = "Generate a summary for the following transcript, returning the following information, meant to be used as an internal summary for managers to read: names on the call if present, key points, dates, dollar size, roadblocks, and any other relevant information. Call transcript: {}"
        external_prompt = "Generate a summary for the following transcript, returning the following information, meant to be used as an external summary for customers to read: include first-person language, use the customer name if it exists, a personalized thank you message, and provide a summary of key points from the discussion, including any questions answered. Call transcript: {}"

        app.logger.info("Starting internal & external summary creation")
        app.logger.info(f"Call transcript....")

        internal_summary_task = asyncio.create_task(fetch_summary("gpt-3.5-turbo", call_transcript, internal_prompt, True))
        external_summary_task = asyncio.create_task(fetch_summary("gpt-3.5-turbo", call_transcript, external_prompt, False))

        internal_summary, external_summary = await asyncio.gather(internal_summary_task, external_summary_task)

        summary_data = {
            "internal_summary": internal_summary,
            "external_summary": external_summary
        }
        result = collection.insert_one(summary_data)
        summary_id = str(result.inserted_id)

        app.logger.info(f"Summary created successfully with ID: {summary_id}")
        return jsonify({"message": "Summary created successfully", "id": summary_id}), 201

    except ValueError as ve:
        app.logger.error(f"Invalid request data: {str(ve)}")
        return jsonify({"message": "Invalid request data", "error": str(ve)}), 400

    except Exception as e:
        app.logger.exception(f"An error occurred while creating summary: {str(e)}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

def get_summary(app, summary_id):
    try:
        app.logger.info(f"Getting summary for {summary_id}")

        # Convert summary_id to ObjectId
        obj_id = ObjectId(summary_id)

        # Need to supress, use cmd + click to read more here. I also gained insight on this from 
        # the following thread https://stackoverflow.com/questions/9694460/difference-between-id-and-id-fields-in-mongodb
        summary = collection.find_one({"_id": obj_id})

        if summary:
            summary["_id"] = str(summary["_id"])
            return jsonify(summary), 200
        else:
            return jsonify({"message": "Summary not found"}), 404

    except InvalidId:
        return jsonify({"message": "Invalid summary ID"}), 400

    except Exception as e:
        app.logger.error(f"Error retrieving summary: {str(e)}")
        return jsonify({"message": "Error retrieving summary", "error": str(e)}), 500

def delete_summary(app, summary_id):
    try:
        app.logger.info(f"Deleting summary with ID: {summary_id}")

        obj_id = ObjectId(summary_id)

        # See get notes
        result = collection.delete_one({"_id": obj_id})

        if result.deleted_count == 1:
            app.logger.info(f"Summary with ID {summary_id} deleted successfully")
            return jsonify({"message": f"Summary with ID {summary_id}"}), 200
        else:
            app.logger.warning(f"Summary with ID {summary_id} not found")
            return jsonify({"message": f"Summary with ID {summary_id} not found"}), 404

    except InvalidId:
        app.logger.error(f"Invalid summary ID: {summary_id}")
        return jsonify({"message": f"{summary_id} is an Invalid summary ID"}), 400

    except Exception as e:
        app.logger.error(f"Error deleting summary: {str(e)}")
        return jsonify({"message": "Error deleting summary", "error": str(e)}), 500