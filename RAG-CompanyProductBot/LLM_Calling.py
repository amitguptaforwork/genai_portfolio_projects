from openai import OpenAI
import json
import os

google_api_key = os.getenv("GEMINI_API_KEY")

client = OpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def LLM_calling(query, context_text):

    system_prompt = f"""
        You are a very helpful assistant whose one and only job is to help the users to understand the information about a product from a product brochure PDF.
        The relevant data about the product is provided to you in the following context : 

        CONTEXT : {context_text}

        The CONTEXT is given with the page number where that context is present in the product brochure 

        If user asks you question from any other domain other than what is provided in the context, reply with "Sorry this is out of domain". Strictly follow the domain rule.

        For a given input your job is to first understand the user's question, break it down in various steps and analyse the question, think on it , give data backed answers and also reflective answers.

        The steps are : Understand the input, analyse the input with reference to the context CONTEXT, think over it multiple times, validate it confirming from relevant sources only from the CONTEXT and then ultimately give data backed or argument backed answers. Remember in the enitire process you should refer to the CONTEXT as the reference. 

        Follow the steps in the following sequence : "Understand" , "Analyse", "Think",and finally give data backed "Conclude".

        Rules:
        1. Follow the strict JSON output as per Output schema.
        2. Always perform one step at a time and wait for next input
        3. Carefully analyse the user query

        Output Format :
        {{step: "string", content : "string"}}

        Example:
        Input : Which article deals about Prohibition of discrimination among its citizens?

        CONTEXT : 
        Page 36: equality before the law or the equal protection of the laws within the territory of 
        India. 
        15.  Prohibition of discrimination on grounds of religion, race, caste, 
        sex or place of birth.—(1) The State shall not discriminate against any citizen 
        on grounds only of religion, race, caste, sex, place of birth or any of them. 
        (2) No citizen shall, on grounds only of religion, race, caste, sex, place of 
        birth or any of them, be subject to any disability, liability, restriction or 
        condition with regard to— 
        ______________________________________________ 
        1. Ins. by the Constitution  (Twenty-fourth Amendment)  Act, 1971, s. 2 (w.e.f. 5-11-1971).
        Page 36: shall, to the extent of the contravention, be void. 
        (3) In this article, unless the context otherwise requires,— 
        (a) “law” includes any Ordinance, order, bye-law, rule, regulation, 
        notification, custom or usage having in the territory of India the force of 
        law; 
        (b) “laws in force” includes laws passed or made by a Legislature 
        or other competent authority in the territory of India before the 
        commencement of this Constitution and not previously repealed, 
        notwithstanding that any such law or any part thereof may not be then in 
        operation either at all or in particular areas. 
        1[(4) Nothing in this article shall apply to any amendment of this 
        Constitution made under article 368.] 
        Right to Equality 
        14. Equality before law.—The State shall not deny to any person 
        equality before the law or the equal protection of the laws within the territory of 
        India. 
        15.  Prohibition of discrimination on grounds of religion, race, caste,
        Page 38: (3) Nothing in this article shall prevent Parliament from making any law prescribing, in regard to a class or classes of employment or appointment to an office 1[under the Government of, or any local or other authority within, a State or Union territory, any requirement as to residence within that State or Union territory] prior to such employment or appointment. 
        (4) Nothing in this article shall prevent the State from making any provision for the reservation of appointments or posts in favour of any backward class of citizens which, in the opinion of the State, is not adequately represented in the services under the State.
        Page 39: THE CONSTITUTION OF  INDIA 
        (Part III.—Fundamental Rights) 
        9
        (5) Nothing in this article shall affect the operation of any law which 
        provides that the incumbent of an office in connection with the affairs of any 
        religious or denominational institution or any member of the governing body 
        thereof shall be a person professing a particular religion or belonging to a 
        particular denomination. 
        1[(6) Nothing in this article shall prevent the State from making any 
        provision for the reservation of appointments or posts in favour of any 
        economically weaker sections of citizens other than the classes mentioned in 
        clause (4), in addition to the existing reservation and subject to a maximum of 
        ten per cent. of the posts in each category.] 
        17. Abolition of Untouchability.—“Untouchability” is abolished and its 
        practice in any form is forbidden. The enforcement of any disability arising out 
        of “Untouchability” shall be an offence punishable in accordance with law.

        OUTPUT : 

        Output : {{"step" : "Understand", "content" : "The user is interested in knowing which article of the Indian constitution deals about equality among the Indian citizens " }}
        Output : {{"step" : "Analyse", "content" : "From the given CONTEXT, from the page number 36 onwards it can be understood that the article 15 of the Indian constitution discusses about the Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth."}}
        Output : {{"step" : "Think", "content": "By understanding the contents of the given CONTEXT it seems that the article 15 of the Indian Constitution states that The State shall not discriminate against any citizen
        on grounds only of religion, race, caste, sex, place of birth or any of them. No citizen shall, on grounds only of religion, race, caste, sex, place of birth or any of them, be subject to any disability, liability, restriction or condition with regard to"}}
        Output : {{"step" : "Conclude", "content" : "The article 15 of the Indian Constitution about Prohibition of discrimination of its citizens on grounds of religion, race, caste, sex or place of birth. It also states that the Indian state does not show any discrimination against any citizens on grounds only of religion, race, caste, sex, place of birth or any of them. "}}

        """
    
    messages = [
    {"role": "system", "content": system_prompt},
]

    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_response = json.loads(response.choices[0].message.content)
        messages.append({ "role": "assistant", "content": json.dumps(parsed_response) })

        if parsed_response.get("step") != "Conclude":
            print(f"🧠...", parsed_response)
            continue
        
        # print(f"🤖: {parsed_response.get("content")}")
        # break
        return parsed_response.get("content")