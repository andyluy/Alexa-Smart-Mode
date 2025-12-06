# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit [https://alexa.design/cookbook](https://alexa.design/cookbook) for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import requests  # Adicionado para fazer requisições HTTP à API da Perplexity
import logging
import ask_sdk_core.utils as ask_utils
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do arquivo .env

API_KEY = os.getenv("API_KEY")  # Pega a chave da API Perplexity do ambiente
url = "https://api.perplexity.ai/chat/completions" # Define o endpoint da Perplexity

# === Inserção da função pedir à API Perplexity ===
def perguntar_perplexity(mensagem_usuario):
    """Envia a pergunta para a API da Perplexity e retorna a resposta da IA."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar",  # Ou experimente "sonar-medium-online" para respostas mais rápidas
        "messages": [
            {"role": "user", "content": mensagem_usuario}
        ]
    }
    try:
        # Timeout ajustado para não ultrapassar o limite da Alexa (8 seg)
        response = requests.post(url, headers=headers, json=payload, timeout=7)
        response.raise_for_status() # Garante que erros HTTP sejam tratados
        resp_json = response.json()
        resposta = resp_json["choices"][0]["message"]["content"]
        # Sanitiza resposta para garantir que não é None ou string vazia
        if not isinstance(resposta, str):
            resposta = str(resposta)
        resposta = resposta.strip().replace('\n', ' ')
        # Limita resposta para evitar exceder tempo do speech da Alexa
        if not resposta:
            resposta = "Desculpe, não consegui encontrar uma resposta."
        # Opcional: limita para X caracteres se desejar máxima agilidade
        resposta = resposta[:800]
        return resposta
    except Exception as e:
        logger.error(f"Erro na chamada à Perplexity: {e}", exc_info=True)
        return "Desculpe, tive um problema para responder agora. Tente novamente."

# === Fim da inserção ===

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bem vindo ao modo inteligente. A partir de agora, você pode começar suas perguntas ou pedidos com 'me' 'diga' e eu vou pensar com atenção para responder de forma inteligente."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CapturaNomeIntentHandler(AbstractRequestHandler):
    """Handler for Captura nome Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CapturaNomeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        nomeusuario = handler_input.request_envelope.request.intent.slots["nomeusuario"].value
        speak_output = f"{nomeusuario} é um nome bonito. Muito prazer {nomeusuario}! Bem vindo ao Gamelab UERJ"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, não consegui entender bem, poderia repetir a pergunta começando com me diga?"
        reprompt = "Desculpe nao ouvi direito, podria repetir começando com me diga?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpa, eu tropecei nos fios aqui, pode tentar de novo ?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
        

class PerplexityChatIntentHandler(AbstractRequestHandler):
    """Handler para qualquer pergunta: manda para a Perplexity e retorna resposta"""

    def can_handle(self, handler_input):
        # Sempre trata IntentRequest, exceto intenções padrão (Help, Cancel etc)
        intent_name = ask_utils.get_intent_name(handler_input)
        default_intents = [
            "AMAZON.HelpIntent", "AMAZON.CancelIntent", "AMAZON.StopIntent",
            "AMAZON.FallbackIntent", "LaunchRequest", "CapturaNomeIntent"
        ]
        return ask_utils.is_request_type("IntentRequest")(handler_input) and intent_name not in default_intents

    def handle(self, handler_input):
        # Pega o texto da pergunta do usuário (em Alexa, normalmente via slot ou transcrição livre da intenção)
        try:
            # Tenta pegar texto via slot chamado 'mensagem'
            mensagem_usuario = handler_input.request_envelope.request.intent.slots.get("mensagem").value + "Responda apenas com texto simples, sem caracteres de markdown, sem referências ou citações. Mantenha a resposta clara e objetiva, com no máximo 600 caracteres, para que possa ser lida diretamente pela Alexa como resposta ao usuário"
        except Exception:
            # Se não houver slot 'mensagem', tenta recuperar pelo nome da intenção ou uma fallback
            mensagem_usuario = ask_utils.get_intent_name(handler_input)

        # Chama a IA da Perplexity
        resposta_ia = perguntar_perplexity(mensagem_usuario)
        resposta_ia = resposta_ia[:800]

        # Retorna resposta da IA ao usuário
        return (
            handler_input.response_builder
                .speak(resposta_ia)
                .ask("Se quiser perguntar outra coisa, pode falar.")
                .response
        )



# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CapturaNomeIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(PerplexityChatIntentHandler())  # Adicionado para responder com Perplexity
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
