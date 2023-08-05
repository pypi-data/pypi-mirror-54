import json

def python_json_stringify(value):
    # This is necessary because Monday's API says that it requires a JSON encoded string for JSON values,
    # ala JSON.stringify, which doesn't quite work the same as json.dumps, unfortunately.
    # What it ACTUALLY requires (anything else returns an error) is a JSON encoded, JSON encoded string.
    # According to their API, a proper value for label should look like this:
    # "{\"label\":\"Done\"}"

    # Don't do anything with regular ol' string values
    if not isinstance(value, dict):
        return value

    return json.dumps(json.dumps(value))
