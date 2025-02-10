import re

def analyze_query(query):
    """
    Analyze the user's query to determine which agents are needed.
    Returns a dictionary indicating whether each agent should be used.
    """
    query_lower = query.lower()
    agents_to_use = {
        'document': False,
        'web_search': False,
        'calculator': False
    }

    # Determine if document retrieval is needed
    if any(keyword in query_lower for keyword in ['zoe', 'diagnoses', 'medical history', 'records', 'report']):
        agents_to_use['document'] = True

    # Determine if web search is needed
    if any(keyword in query_lower for keyword in ['news', 'current events', 'latest', 'update']):
        agents_to_use['web_search'] = True

    # Determine if calculation is needed
    if 'calculate' in query_lower or re.search(r'\d+[\s]*[+\-*/][\s]*\d+', query):
        agents_to_use['calculator'] = True

    return agents_to_use