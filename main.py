import sys
from operations.conversing import ConversationalChatBot
from utilities.cost_estimating import CostEstimator


if __name__ == '__main__':

    prompt = "What is a healthy breakfast?"

    # caller = CompletionCaller(prompt=prompt, max_tokens=128, frequency_penalty=2)
    # caller.make_call()
    # response = caller.get_response()  
    # print(response)

    # chat_caller = ChatCaller(
    #     messages=[
    #         {
    #             'role': 'user',
    #             'content': 'What is the fastest animal on Earth?'
    #         }
    #     ],
    #     max_tokens=128
    # )
    # chat_caller.make_call()
    # response = chat_caller.get_response()
    # print(response)

    chatbot = ConversationalChatBot(personality='scientific')
    chatbot.start()

    cost_estimator = CostEstimator(
        model_name='gpt-3.5-turbo', 
        text=prompt,
        price_per_one_m_tokens=3.00)
    cost_estimator.make_estimation()
    cost_estimate = cost_estimator.get_cost_estimate()
    print(cost_estimate)

    sys.exit(0)
