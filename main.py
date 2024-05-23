from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import json
import os
from faster_whisper import WhisperModel

app = FastAPI()

def transcribe_audio(audio_file_path):
    model_size = "large-v3"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_file_path, beam_size=10)

    transcribed_segments = []
    for segment in segments:
        transcribed_segments.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text
        })

    result = {
        "language": info.language,
        "language_probability": info.language_probability,
        "transcribed_segments": transcribed_segments
    }

    return result
    
def extract_text_with_numbers_up_to_hundred(Audio_STT_data):
    #text_string = ' '.join(segment['text'] for segment in Audio_STT_data['transcribed_segments'])
    #text_parts = [segment["text"] for segment in transcribed_segments]
    #text_string = " ".join(text_parts)
    
    # Convert number words to numbers
    number_mapping = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
        "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10", "eleven": "11",
        "twelve": "12", "thirteen": "13", "fourteen": "14", "fifteen": "15", "sixteen": "16",
        "seventeen": "17", "eighteen": "18", "nineteen": "19", "twenty": "20", "thirty": "30",
        "forty": "40", "fifty": "50", "sixty": "60", "seventy": "70", "eighty": "80",
        "ninety": "90", "hundred": "100"
    }
    
    for word, number in number_mapping.items():
        text_string = Audio_STT_data.replace(word, number)
    
    return text_string


# property #

import json

def extract_info(user_input):
    json_files = [
        '/home/rben10/Maitri_Feb_24/API_TEXT/Extracted_Json_data/extracted_property_data.json',
        '/home/rben10/Maitri_Feb_24/API_TEXT/Extracted_Json_data/extracted_unit_type_data.json',
        '/home/rben10/Maitri_Feb_24/API_TEXT/Extracted_Json_data/extracted_units_data.json',
        '/home/rben10/Maitri_Feb_24/API_TEXT/Extracted_Json_data/extracted_tasks_data.json',
        '/home/rben10/Maitri_Feb_24/API_TEXT/Json_data/unit_issues_data.json',
        '/home/rben10/Maitri_Feb_24/API_TEXT/Json_data/team_data.json',
        '/home/rben10/Maitri_Feb_24/API_TEXT/Json_data/task_check_list_data.json',
        '/home/rben10/Maitri_Feb_24/API_TEXT/Json_data/task_templates_data.json'
    ]

    matching_keywords_with_keys = {}

    for file_path in json_files:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, str) and value.lower() in user_input.lower():
                            matching_keywords_with_keys[key] = value

    matching_keywords_dict = matching_keywords_with_keys
    unit_name_found = matching_keywords_dict.get("unit_name", None)

    units_file = '/home/rben10/Maitri_Feb_24/API_TEXT/Extracted_Json_data/extracted_units_data.json'

    property_name = None
    unit_type = None
    unit_name_to_find = unit_name_found

    with open(units_file, 'r') as json_file:
        units_data = json.load(json_file)
        for unit in units_data:
            if 'unit_name' in unit and unit['unit_name'] == unit_name_to_find:
                if 'unit_type' in unit and 'unit_type_name' in unit['unit_type']:
                    unit_type = unit['unit_type']['unit_type_name']
                if 'property' in unit and 'property_name' in unit['property']:
                    property_name = unit['property']['property_name']
                break

    output_dict_section_1_info = {
        'unit_name': unit_name_to_find,
        'property_name': property_name,
        'unit_type': unit_type
    }

    if property_name is not None and unit_type is not None:
        return output_dict_section_1_info
    else:
        return {"error": f"Unit '{unit_name_to_find}' not found or missing property/unit type information"}

# TASK #########

def classify_task(user_input):
    user_input_lower = user_input.lower()
    maintenance_keywords = ['maintenance', 'repair', 'fix', 'service', 'replace', 'adjust', 'update', 'not working', 'notfunctional', 'broken']
    housekeeping_keywords = ['clean', 'cleaning', 'tidy', 'tidying', 'organize', 'organizing', 'sanitize', 'sanitizing']
    inspection_keywords = ['inspect', 'inspection']
    high_priority_keywords = ['urgent', 'high priority']
    medium_priority_keywords = ['medium priority']

    task_type = None
    task_priority = 'medium'  # Default priority if not specified

    for keyword in maintenance_keywords:
        if keyword in user_input_lower:
            task_type = 'maintenance'
            break
    
    for keyword in housekeeping_keywords:
        if keyword in user_input_lower:
            task_type = 'housekeeping/cleaning'
            break
    
    for keyword in inspection_keywords:
        if keyword in user_input_lower:
            task_type = 'inspection'
            break

    for keyword in high_priority_keywords:
        if keyword in user_input_lower:
            task_priority = 'Urgent'
            break
    
    for keyword in medium_priority_keywords:
        if keyword in user_input_lower:
            task_priority = 'medium'
            break

    if task_type is None:
        return {
            "error": "Task type not specified. Please specify the task type (maintenance/housekeeping/inspection)."
        }

    # Construct the task title and description
    task_title = task_type
    task_description = user_input

    return {
        "task_type": task_type,
        "task_priority": task_priority,
        "task_title": task_title,
        "task_description": task_description
    }




def classify_task_type(user_input):
    user_input_lower = user_input.lower()
    maintenance_keywords = ['maintenance', 'repair', 'fix', 'service', 'replace', 'adjust', 'update', 'not working', 'notfunctional', 'broken']
    housekeeping_keywords = ['clean', 'cleaning', 'tidy', 'tidying', 'organize', 'organizing', 'sanitize', 'sanitizing']
    inspection_keywords = ['inspect', 'inspection']

    for keyword in maintenance_keywords:
        if keyword in user_input_lower:
            return 'maintenance'
    
    for keyword in housekeeping_keywords:
        if keyword in user_input_lower:
            return 'housekeeping/cleaning'
    
    for keyword in inspection_keywords:
        if keyword in user_input_lower:
            return 'inspection'

        # Ask the user for clarification if the task type is not clear
    task_type = input("Please specify the task type (maintenance/housekeeping/inspection): ").lower()
    return task_type

def classify_task_priority(user_input):
    user_input_lower = user_input.lower()
    high_priority_keywords = ['urgent', 'high priority']
    medium_priority_keywords = ['medium priority']

    for keyword in high_priority_keywords:
        if keyword in user_input_lower:
            return 'Urgent'
    
    for keyword in medium_priority_keywords:
        if keyword in user_input_lower:
            return 'medium'

    # Default to medium priority if no urgency is specified
    return 'medium'

    task_type = classify_task_type(user_input)
    task_priority = classify_task_priority(user_input)

    # Integrate your previous function here to extract information from JSON files
    #extracted_info = extract_info_from_json(user_input)

    # Construct the task title and description
    task_title = task_type
    task_description = user_input

    return {
        "task_type": task_type,
        "task_priority": task_priority,
        "task_title": task_title,
        "task_description": task_description
    }

# RATE, TIME ESTIMATE ##


def extract_rate_info(user_input):
    # Convert sentence to lowercase for case-insensitive matching
    user_input_lower = user_input.lower()

    # Split the sentence into words
    words = user_input_lower.split()

    # Initialize a list to store the next ten words after the target words
    def extract_next_ten_words(sentence, target_words):
        next_words = []
        for i, word in enumerate(sentence):
            if word in target_words:
                next_words.extend(sentence[i:i + 10])  # Get the next 10 words including the target word
                break  # Stop searching after finding the target word
        return next_words

    target_rate_words = ['rate', 'cost', 'price']
    target_time_words = ['time', 'duration', 'estimated','estimate']

    next_rate_words = extract_next_ten_words(words, target_rate_words)
    next_time_words = extract_next_ten_words(words, target_time_words)

    def extract_rate_from_input(input_words):
        rate = None
        currency_unit = None
        for i, word in enumerate(input_words):
            if word in ['dollars', 'rupees', 'usd'] and i > 0 and input_words[i - 1].isdigit():
                rate = int(input_words[i - 1])
                currency_unit = word
                break
        return rate, currency_unit

    def extract_time_estimated_with_unit(input_words, time_units):
        time_estimated = None
        time_unit = None
        for i, word in enumerate(input_words):
            if word.isdigit() and i < len(input_words) - 1 and input_words[i + 1] in time_units:
                time_estimated = int(word)
                time_unit = input_words[i + 1]
                break
        return time_estimated, time_unit

    rate, currency_unit = extract_rate_from_input(next_rate_words)
    time_estimated, time_unit = extract_time_estimated_with_unit(next_time_words, ['sec', 'second', 'min', 'minute', 'hour', 'hr'])

    if rate is None or currency_unit is None:
        return {
            "error": "Rate or currency unit not found in the input."
        }
    
    if time_estimated is None or time_unit is None:
        return {
            "error": "Time estimated or time unit not found in the input."
        }

    return {
        "rate": rate,
        "currency_unit": currency_unit,
        "time_estimated": time_estimated,
        "time_unit": time_unit
    }

### Date to complete task

from datetime import datetime, timedelta

def parse_date(user_input):
    # Define tuples of similar words for each type of date mention
    today_words = ('today', 'this day')
    tomorrow_words = ('tomorrow', 'tom', 'tmrw')
    end_of_month_words = ('end of month', 'end of the month', 'end of the current month')
    end_of_week_words = ('end of week', 'end of this week', 'end of the week', 'end of the current week')
    next_month_words = ('next month', 'next month\'s')
    next_week_words = ('next week', 'next week\'s')

    # Map keywords to their corresponding date offsets
    date_mappings = {
        today_words: 0,
        tomorrow_words: 1,
        end_of_month_words: (datetime.now().replace(day=1, month=datetime.now().month+1) - timedelta(days=1)).date(),
        end_of_week_words: (datetime.now().replace(hour=23, minute=59, second=59) + timedelta(days=(6 - datetime.now().weekday()))).date(),
        next_month_words: (datetime.now().replace(day=1, month=datetime.now().month+1)).date(),
        next_week_words: (datetime.now().replace(hour=0, minute=0, second=0) + timedelta(days=(7 - datetime.now().weekday()))).date()
    }

    # Check for specific date mentions in the sentence
    for keywords, offset in date_mappings.items():
        for keyword in keywords:
            if keyword in user_input.lower():
                if isinstance(offset, int):
                    return {"due_date": (datetime.now() + timedelta(days=offset)).date(), "due_time": "10am (default)"}
                else:
                    return {"due_date": offset}
    
    return {"error": "No specific date mentioned."}




@app.post("/extract_and_transcribe/")
async def extract_and_transcribe(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Transcribe the audio file
    transcription_result = transcribe_audio(file_path)

    # Delete the temporary file
    os.remove(file_path)

    # Combine all transcribed text segments into a single string
    transcribed_text = ' '.join(segment['text'] for segment in transcription_result['transcribed_segments'])


    Text_from_audio = extract_text_with_numbers_up_to_hundred(transcribed_text)




    # Property 

    property_info = extract_info(Text_from_audio)
    print(property_info)

    task_info = classify_task(Text_from_audio)
    print(task_info)

        # Rate , Time estimate
 
    extracted_rate_info = extract_rate_info(Text_from_audio)
    print(extracted_rate_info)

    # Date

    parsed_date = parse_date(Text_from_audio)
    print(parsed_date)

    #     # task 
    # task_priority_info = classify_task_priority(Text_from_audio)
    # task_type_info = classify_task_type(Text_from_audio)
    # print(task_priority_info)
    # print(task_type_info)
    # task_title = task_type_info
    # task_description = Text_from_audio

    return {

        'Property_info': property_info,
        'Task_info': task_info,
        "Extracted_Rate_time_estimate_info": extracted_rate_info,
        'Date to complete Task':parsed_date


    }



    

    
    ###### TASK ###
    
