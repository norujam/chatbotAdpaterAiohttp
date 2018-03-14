import dialogflow, configparser, logging
from chatbot.chatLogObjectMap import ChatLogObjectMap
import logging

config = configparser.ConfigParser()
config.read('config.properties')


async def detect_intent_texts(texts):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    try:
        project_id = config['googleApi']['projectId']
        session_id = config['googleApi']['sessionId']
        language_code = "ko"
        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(project_id, session_id)

        text_input = dialogflow.types.TextInput(text=texts[0], language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)
        # logging.debug("call action="+response.query_result.action)
        dict_result = dict()
        dict_result["text"] = texts
        dict_result["action"] = response.query_result.action
        dict_result["main_message"] = response.query_result.fulfillment_messages[0].text.text[0]

        if any(response.query_result.action.find(s) > -1 for s in ['outer_retrieve', 'outer_response']):
            parameters = response.query_result.parameters
            dict_result["parameters"] = {}
            for i in parameters.keys():
                dict_result["parameters"][i] = parameters[i]

            # logging.debug(dict_result)
            await ChatLogObjectMap.insert_log(dict_result)
    except Exception as err:
        logging.error(err)
        raise err

    return dict_result
